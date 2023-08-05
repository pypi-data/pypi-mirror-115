import requests, json


class KSONReference:
    def __init__(self, pointer, ref_format=None, suppress=False):
        self.pointer = pointer
        self.resolved = False
        self._raw = None
        self.ref_format = ref_format
        self.ref_contents = None
        self.suppress = suppress

    def __str__(self):
        return f'<<{self.pointer}>>'

    def guess_format(self):
        assert (self._raw is not None)

        if self.pointer.endswith('.json'):
            return 'json'
        if self.pointer.endswith('.kson'):
            return 'kson'
        elif self.pointer.endswith('.csv'):
            return 'csv'

        # Is it JSON?
        try:
            json.loads(self._raw)
            return 'json'
        except Exception as e:
            pass

        # Or maybe it's KSON?
        try:
            from parser import KSONParser
            KSONParser().decode(self._raw)
            return 'kson'
        except ValueError:
            pass

        # CSVs are kind of hard to guess, so default to assuming it's a string
        return 'string'

    def resolve(self):
        if self.ref_contents is not None:
            return  # Already resolved

        if self.pointer.startswith('http://') or self.pointer.startswith('https://'):
            try:
                self._raw = requests.get(self.pointer).text

            except Exception as e:
                print(e)
                raise ValueError("Unable to GET URL " + self.pointer)
        else:
            # Assume it is a file
            try:
                with open(self.pointer) as f:
                    self._raw = f.read()
            except Exception as e:
                print(e)
                raise ValueError("Unable to open local file " + self.pointer)

        self.ref_contents = self.read_contents()

    def read_contents(self):
        assert (self._raw is not None)
        if self.ref_format is None:
            self.ref_format = self.guess_format()

        if self.ref_format == 'json':
            return json.loads(self._raw)
        elif self.ref_format == 'kson':
            from compiler import KSONCompiler
            return KSONCompiler().run(self._raw)
        elif self.ref_format == 'csv':
            import csv
            from io import StringIO

            buff = StringIO(self._raw)
            reader = csv.DictReader(buff)

            def attempt_to_num(v):
                maybe_num = v and len(v) > 0 and (v[0].isdigit() or v[0] == '-')
                maybe_float =  v and '.' in v
                if maybe_num:
                    if maybe_float:
                        try:
                            return float(v)
                        except ValueError:
                            pass
                    else:
                        try:
                            return int(v)
                        except:
                            pass
                return v

            arr_of_dicts = [{k: attempt_to_num(v) for k, v in row.items()}
                            for row in reader]

            return arr_of_dicts

            # Invert for better importing
            # dict_of_arrs = {}
            # for row in arr_of_dicts:
            #     for (key, value) in row.items():
            #         if not key in dict_of_arrs:
            #             dict_of_arrs[key] = []
            #         dict_of_arrs[key].append(value)
            #
            # return dict_of_arrs
        else:
            # Assume a string
            return self._raw

    def to_json(self):
        if self.ref_contents and not self.suppress:
            return self.ref_contents
        else:
            return self.pointer
