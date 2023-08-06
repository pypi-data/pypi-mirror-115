from ref import KSONReference
from db import KSONDB

'''
    A simple KSON decoder for a simple millenium
'''


class KSONAlias:
    def __init__(self, alias, obj):
        self.alias = alias
        self.obj = obj

    def to_json(self):
        return self.obj

class KSONSQLWrapper:
    def __init__(self, sql: str):
        self.sql = sql
        self.execution_context = None
        self.output = None

    def to_json(self):
        if self.output:
            return self.output
        else:
            return self.sql

    def set_execution_context(self, context: KSONDB):
        self.execution_context = context

    def execute(self):
        assert(self.execution_context is not None)
        if self.output is not None:
            return # No need to re-run
        self.output = self.execution_context.execute(self.sql)

class KSONParser:
    def __init__(self):
        '''
        Usage: KSONParser.decode(str)
        '''
        # State for a decoding
        self.__str = ''
        self.__index = 0

        # Some additional bookkeeping to help us print nice error messages
        self.__is_new_line = False
        self.__line = 0
        self.__col = 0

    '''
    Bookkeeping functions
    '''

    def _reset(self, s: str):
        # State for a decoding
        self.__str = s
        self.__index = 0

        # Some additional bookkeeping to help us print nice error messages
        self.__is_new_line = False
        self.__line = 0
        self.__col = 0

    def _err(self, message):
        message = message + f': line {self.__line} col {self.__col}'
        raise ValueError(message)

    '''
    Recursive descent helper functions
    '''

    def __is_done(self):
        return self.__index == len(self.__str)

    def __cur_sym(self, count=1):
        return self.__str[self.__index: self.__index + count] if len(self.__str) >= self.__index + count else None

    def __next_sym(self):
        if self.__is_done():
            self._err("Unexpected end of input")
        self.__index += 1

        if self.__is_new_line:
            self.__line += 1
            self.__col = 0
        else:
            self.__col += 1

        self.__is_new_line = self.__cur_sym() and self.__cur_sym() == '\n'

    def __require_sym(self, sym: str):
        for c in sym:
            if not self.__cur_sym() and self.__cur_sym() == c:
                self._err(f"Unexpected token '{self.__cur_sym()}', expected '{c}'")

            self.__next_sym()

    '''
    Recursive descent terminals
    '''

    def _parse_number(self):

        n_str = ''
        is_float = False

        # 1. Optionally accept a minus sign
        if self.__cur_sym() and self.__cur_sym() == '-':
            n_str += self.__cur_sym()
            self.__next_sym()

        # 2. Parse an integer with no more than 1 leading zero
        if not (self.__cur_sym() and self.__cur_sym().isdigit()):
            self._err("Expected digit")

        has_seen_zero = False
        has_seen_non_zero = True

        while self.__cur_sym() and self.__cur_sym().isdigit():
            if self.__cur_sym() == '0':
                if has_seen_zero and not has_seen_non_zero:
                    self._err("Numeric value cannot have multiple leading zeroes")
                has_seen_zero = True
            else:
                has_seen_non_zero = True
            n_str += self.__cur_sym()
            self.__next_sym()

        # 3. Optionally parse a decimal component
        if self.__cur_sym() == '.':
            n_str += self.__cur_sym()
            self.__next_sym()
            is_float = True
            if not (self.__cur_sym() and self.__cur_sym().isdigit()):
                self._err("Expected digit after decimal point")
            while self.__cur_sym() and self.__cur_sym().isdigit():
                n_str += self.__cur_sym()
                self.__next_sym()

        # 4. Optionally parse an exponent
        if self.__cur_sym() and self.__cur_sym().lower() == 'e':
            n_str += self.__cur_sym()
            self.__next_sym()
            is_float = True
            if self.__cur_sym() and self.__cur_sym() in '-+':
                n_str += self.__cur_sym()
                self.__next_sym()
            if not (self.__cur_sym() and self.__cur_sym().isdigit()):
                self._err("Expected digit after exponent")

            while self.__cur_sym() and self.__cur_sym().isdigit():
                n_str += self.__cur_sym()
                self.__next_sym()

        # 5. Convert to number and return
        if is_float:
            return float(n_str)
        else:
            return int(n_str)

    def _parse_string(self):
        self.__require_sym('"')
        s = ''
        while self.__cur_sym() != '"':
            if self.__cur_sym() == '\\':
                s += self._parse_escape_seq()
            else:
                s += self.__cur_sym()
                self.__next_sym()

        self.__require_sym('"')
        return s

    def _parse_escape_seq(self, custom=None):
        self.__require_sym('\\')
        c = self.__cur_sym()
        if custom is not None and c in custom:
            self.__next_sym()
            return c
        if c in '"\\/ntbrf':
            self.__next_sym()
            return eval('"\\' + c + '"')
        elif c == 'u':
            u = c
            self.__next_sym()
            u += self._parse_hex_char()
            u += self._parse_hex_char()
            u += self._parse_hex_char()
            u += self._parse_hex_char()
            return eval('"\\' + u + '"')
        else:
            self._err(f"Invalid control sequence: '\\{c}'")

    def _parse_hex_char(self):
        h = self.__cur_sym()
        if not (h and h in '0123456789abcdefABCDEF'):
            self._err(f"Invalid hex character: '{h}'")
        self.__next_sym()
        return h

    def _parse_array(self):
        self.__require_sym('[')
        self._parse_break()
        a = []
        while self.__cur_sym() != ']':
            el = self._parse_element()
            a.append(el)
            self._parse_break()
            if not (self.__cur_sym() and self.__cur_sym() in ',]'):
                self._err('Unexpected end of array')
            if self.__cur_sym() == ',':
                self.__next_sym()

        self.__require_sym(']')
        return a

    def _parse_dic(self):
        self.__require_sym('{')
        self._parse_break()
        d = {}
        while self.__cur_sym() != '}':
            key = self._parse_string()
            self._parse_break()
            self.__require_sym(':')
            value = self._parse_element()
            d[key] = value
            self._parse_break()
            if not (self.__cur_sym() and self.__cur_sym() in ',}'):
                self._err('Unexpected end of dictionary')
            if self.__cur_sym() == ',':
                self.__next_sym()
            self._parse_break()

        self.__require_sym('}')
        return d

    def _parse_whitespace(self):
        while self.__cur_sym() and self.__cur_sym().isspace():
            self.__next_sym()

    def _parse_break(self):
        self._parse_whitespace()
        if self.__cur_sym(2) == '/*':
            self._parse_comment()
        self._parse_whitespace()

    def _parse_comment(self):
        self.__require_sym('/*')
        while self.__cur_sym(2) != '*/':
            self.__next_sym()
        self.__require_sym('*/')

    def _parse_true(self):
        for c in 'true':
            self.__require_sym(c)
        return True

    def _parse_false(self):
        for c in 'false':
            self.__require_sym(c)
        return False

    def _parse_null(self):
        for c in 'null':
            self.__require_sym(c)
        return None

    def _parse_ref(self):
        self.__require_sym('<<')

        suppress = False
        if self.__cur_sym() == '!':
            suppress = True
            self.__next_sym()

        r = ''
        ref_format = None
        while self.__cur_sym() not in '>|':
            if self.__cur_sym() == '\\':
                r += self._parse_escape_seq(['>|'])
            else:
                r += self.__cur_sym()
                self.__next_sym()

        if self.__cur_sym() == '|':
            self.__next_sym()
            ref_format = ''
            while self.__cur_sym() != '>':
                ref_format += self.__cur_sym()
                self.__next_sym()

        self.__require_sym('>>')

        return KSONReference(r, ref_format, suppress=suppress)

    def _parse_sql(self):
        self.__require_sym('```')

        sql = ''

        while self.__cur_sym() and self.__cur_sym(3) != '```':
            sql += self.__cur_sym()
            self.__next_sym()

        self.__require_sym('```')

        return KSONSQLWrapper(sql)

    def _parse_alias(self):
        self.__require_sym('as')
        self._parse_break()
        if not (self.__cur_sym() and self.__cur_sym().isalnum() or self.__cur_sym() == '_'):
            self._err("Invalid identifier")
        ident = self.__cur_sym()
        self.__next_sym()
        while self.__cur_sym().isalnum() or self.__cur_sym() == '_':
            ident += self.__cur_sym()
            self.__next_sym()

        if not ident.isidentifier():
            self._err(
                f"Invalid alias '{ident}'. An alias must consist of alphanumeric characters or underscores, and cannot start with a number.")

        return ident

    def _parse_element(self):
        self._parse_break()
        c = self.__cur_sym()
        if not c:
            self._err("Expected data")
        r = None

        if c.isdigit() or c == '-':
            r = self._parse_number()
        elif c == '"':
            r = self._parse_string()
        elif c == '[':
            r = self._parse_array()
        elif c == '{':
            r = self._parse_dic()
        elif c == 't':
            r = self._parse_true()
        elif c == 'f':
            r = self._parse_false()
        elif c == 'n':
            r = self._parse_null()
        elif self.__cur_sym(2) == '<<':
            r = self._parse_ref()
        elif self.__cur_sym(3) == '```':
            r = self._parse_sql()
        else:
            self._err(f"Unexpected token: '{c}'")

        # Optionally parse an alias for this element
        self._parse_break()
        if self.__cur_sym(2) == 'as':
            alias = self._parse_alias()
            return KSONAlias(alias=alias, obj=r)

        return r

    '''
    Public API
    '''

    def decode(self, s: str):
        if not isinstance(s, str):
            raise ValueError("Expected string")

        self._reset(s)
        el = self._parse_element()
        self._parse_break()

        if not self.__is_done():
            self._err("Extra data")
        return el

