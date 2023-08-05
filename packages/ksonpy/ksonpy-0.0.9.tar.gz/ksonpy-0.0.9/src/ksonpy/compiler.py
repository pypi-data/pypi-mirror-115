import json

from db import KSONDB
from helper import DB_IMPORT_TYPE_RULES
from parser import KSONParser, KSONAlias, KSONSQLWrapper
from ref import KSONReference


class KSONCompiler:
    def __init__(self, verbose=False):
        self.parser = KSONParser()
        self.parse_tree = None
        self.reference_links = dict()

        self.verbose = verbose

        self.db = KSONDB()

    def set_reference(self, key, value):
        # This sets the reference but ALSO imports to our SQLite DB if possible.

        self.reference_links[key] = value

    def mangle_col_name(self, col):
        return ''.join(col.split())

    def import_into_db(self, table_name, value):
        if self.verbose:
            print(f"Trying to import {table_name}")
        if table_name in self.db.db_links:
            return  # A dupe key?
        # Import into database
        if isinstance(value, list) and len(value):
            keys = dict()  # Determine key types
            skip_keys = set()
            if isinstance(value[0], dict):
                # A list of dicts
                table = []
                for row in value:
                    row_contents = {}
                    if not isinstance(row, dict):
                        # Can't import
                        return
                    for (k, v) in row.items():
                        k = self.mangle_col_name(k)
                        if k in skip_keys:
                            continue
                        if v is None:
                            row_contents[k] = None  # Doesn't affect type inference
                            continue
                        if not type(v) in DB_IMPORT_TYPE_RULES:
                            skip_keys.add(k)
                            continue

                        rule = DB_IMPORT_TYPE_RULES[type(v)]
                        if k not in keys or keys[k] in rule['upgrade']:
                            keys[k] = rule['rule']
                            row_contents[k] = v
                        elif keys[k] == rule['rule']:
                            row_contents[k] = v
                        elif keys[k] in rule['accept']:
                            row_contents[k] = v  # We won't downgrade
                        else:
                            skip_keys.add(k)
                            continue

                    table.append(row_contents)
                for key in skip_keys:
                    if key in keys:
                        del keys[key]
                if len(keys) == 0:
                    return  # We can't import because there are no valid keys
                if self.verbose:
                    if self.verbose:
                        print(f"{table_name} has {len(table)} usable rows and {len(keys)} columns")
                # We want to import "table" at "key"
                try:
                    self.db.create_table(table_name, keys, verbose=self.verbose)
                    self.db.populate_table(table_name, table)
                    self.db.db_links[table_name] = table
                except Exception as e:
                    if self.verbose:
                        print(f"Error importing table {table_name}:", e)
                    pass

            elif type(value[0]) in DB_IMPORT_TYPE_RULES:
                # A flat array. We can import with the TABLE_NAME$KEY rule.
                col_name = table_name.split('$')[-1]
                table_shim = [{col_name: v} for v in value]
                return self.import_into_db(table_name, table_shim)
            elif isinstance(value[0], list):
                # We don't really have a good mechanism for importing or referring to lists of lists,
                # so we recurse no farther
                pass
        elif isinstance(value, dict):
            # A dictionary. We can try to import each column individually
            for k, v in value.items():
                self.import_into_db(f'{table_name}${k}', v)
        elif isinstance(value, int):
            self.db.substitution_codes[table_name] = value
        elif isinstance(value, float):
            self.db.substitution_codes[table_name] = value
        elif isinstance(value, str):
            self.db.substitution_codes[table_name] = f'"{value}"'  # TODO: Check for possible issues with escaping here
        else:
            return

    def compile(self, root=None):
        '''
        Convert references into objects. TODO: Resolve references in parallel
        TODO: Allow cacheing references
        '''
        if root is None:
            root = self.parse_tree

        if isinstance(root, KSONReference):
            # Need to get the contents of this reference
            root.resolve()
        elif isinstance(root, KSONAlias):
            target = root.obj
            if root.alias in self.reference_links:
                raise ValueError("Duplicate alias: " + root.alias)
            self.compile(root.obj)
            # If the alias is to a reference, we need to resolve that reference *first* and then point to it.
            if isinstance(root.obj, KSONReference):
                target = root.obj.ref_contents
            self.set_reference(root.alias, target)
            self.import_into_db(f'${root.alias}', target)
        elif isinstance(root, KSONSQLWrapper):
            # We want to execute
            root.set_execution_context(self.db)
            root.execute()
        elif isinstance(root, list):
            for el in root:
                self.compile(el)
        elif isinstance(root, dict):
            for el in root.values():
                self.compile(el)
        else:
            # Nothing to do
            pass

    def to_json(self, indent=None):
        assert (self.parse_tree is not None)
        self.compile()

        if self.verbose:
            print("Links:", list(self.db.db_links.keys()))

        def json_encode_custom(obj):
            try:
                return obj.to_json()
            except:
                return obj.__dict__

        return json.dumps(self.parse_tree, default=json_encode_custom, indent=indent)

    def run(self, program: str, indent=None):
        if self.parse_tree is not None:
            raise ValueError("You cannot reuse a compiler object for a new program")
        self.parse_tree = self.parser.decode(program)
        return self.to_json(indent=indent)


if __name__ == '__main__':
    # Some test cases
    # KSONCompiler().run('''
    # {
    #     "comments": "This is a KSON document containing a list of countries.",
    #     "country_list": <<https://raw.githubusercontent.com/umpirsky/country-list/master/data/en_US/country.csv|csv>> as countries
    # }
    # ''', indent=None)

    # Test SQL
    # Some test cases
    # out = KSONCompiler().run('''
    # {
    #     "comments": "This is a KSON document containing a list of chess grandmasters.",
    #     "constant": 3.5 as ThreeFive,
    #     "gm_list": <<!https://api.chess.com/pub/titled/GM>> as gms,
    #     "gms_asc": ```select players, $ThreeFive as ranking from "$gms$players" order by players asc```
    # }
    # ''', indent=None)

    # Some test cases
    # out = KSONCompiler().run('''
    # {
    #     "comments": "This is a KSON document containing information about world population data.",
    #     "source": <<!https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2019_TotalPopulationBySex.csv|csv>> as pop,
    #     "topLocations": ```select * from "$pop" where Location != 'World' order by PopTotal desc limit 10;```
    # }
    # ''', indent=None)

    # Some test cases
    # out = KSONCompiler().run('''
    # {
    #     "comments": "This is a KSON document containing information about your IP address.",
    #     "source": <<!https://api.ipify.org/?format=json>> as ip,
    #     "ipAddress": ```select $ip$ip limit 1;```
    # }
    # ''', indent=None)

    # Some test cases
    # out = KSONCompiler(verbose=False).run('''
    # {
    #     "description": "This is a KSON document containing information about global GDP.",
    #     "source": <<!https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv>> as gdp,
    #     "top5GDPs": ```select * from "$gdp" where year in (select max(year) from "$gdp") order by value asc limit 5;```
    # }
    # ''', indent=2)

    out = KSONCompiler(verbose=False).run('''
        {
            "description": "This is a KSON document which cross-references two data sources to compute per capita GDP.",
            /* Data source 1 is a CSV file */
            "sourceGDP": <<!https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv>> as gdp,
            /* Data source 2 is a JSON file. While KSON attempts to infer the data type automatically, you can also specify it
             explicitly with a `|<type>` after the URL as shown here: */
            "sourcePopulation": <<!https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-population.json|json>> as pop,
            "gdpAndPopulation": ```
                    select p.country, g.year, g.value gdp, p.population, g.value/p.population perCapita
                    from "$gdp" g left join "$pop" p on g.countryName = p.country
                     where year in (select max(year) from "$gdp")
                     order by g.value/p.population desc
                     limit 5;
                 ```
        }
    ''', indent=2)

    print(out)
