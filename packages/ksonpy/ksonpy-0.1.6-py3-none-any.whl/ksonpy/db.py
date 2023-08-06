class KSONDB:
    def __init__(self):
        # Import the sqlite3 module
        import sqlite3

        # Create database connection to an in-memory database
        self._dbcon = sqlite3.connect(":memory:")
        self._dbcon.row_factory = sqlite3.Row

        # Obtain a cursor object

        self._dbcur = self._dbcon.cursor()

        self._fields = dict()

        self.db_links = dict()
        self.substitution_codes = dict()

    def escape_colname(self, name: str):
        return f"'{name}'"

    def create_table(self, name: str, fields: dict, verbose=False):
        self._fields[name] = fields
        # print(name, fields)
        query = f"CREATE TABLE \"{name}\"({','.join(self.escape_colname(key) + ' ' + type for (key, type) in fields.items())});"
        if verbose:
            print(query)
        self._dbcur.execute(query)

    def populate_table(self, name: str, values: list):
        '''
        TODO: Optimize this routine, if possible
        :param name: The name of the table
        :param values: A list of dictionaries, where the key is the name of the column and the value is the
        :return:
        '''
        if len(values) == 0:
            return
        self._dbcur.executemany(
            f"INSERT INTO \"{name}\" ({','.join(self.escape_colname(n) for n in values[0].keys())}) "
            f"VALUES ({','.join((':' + v for v in values[0].keys()))});",
            (tuple(row.values()) for row in values))

    def execute(self, query: str):
        import re
        for (s, v) in self.substitution_codes.items():
            escaped = re.escape(s)
            # print(s, v, escaped)
            query = re.sub(rf"{escaped}\b", str(v), query) # TODO: fix potential name collisions with lookbehind here
        try:
            self._dbcur.execute(query)
        except Exception as e:
            print("Error executing query: ", query)
            raise e

        rows = self._dbcur.fetchall()

        out = [dict(r) for r in rows]
        if len(out) and len(out[0]) == 1:
            l = [list(r.values())[0] for r in out]
            if re.match(r"\blimit 1\b", query.lower()):
                return l[0]
            return l
        elif not len(out):
            return []
        return out
