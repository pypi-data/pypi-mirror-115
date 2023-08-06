# KSON: JSON with SQL and Networking

> Of course it's a good idea: what makes you ask?

KSON is a superset of JSON with the following features:

- Remote document references (so you can embed a JSON, KSON, or CSV file available at a public URL or file path)
- Embedded SQL: Write queries against other objects in your JSON file (including references and deeply nested objects)
  with the full power of SQLite and have the queries evaluate to JSON
- Use comments (`/* ... */`) and global named references (`"foo": "bar" as myRef`).
- Compiles to JSON: Run `kson file.kson` (see installation instructions below) and boom! you have JSON.

KSON combines the portability of the top data exchange formats (JSON, CSV) with the expressiveness of the leading data
querying language
(SQL), and the flexibility of dynamic embedded references. This project is pre-release and we welcome bug reports
and any other feedback.

## Installation

Run

```bash
python3 -m pip install ksonpy
```

This will create a global executable `kson` which you can run on
`.kson` files to produce `.json` output:

```bash
kson file.kson [--indent <integer>]
```

or pipe to a file:

```bash
kson file.kson > file.json
```

## Examples

You can find examples in the `examples/` directory.

- [examples/gdp.kson](examples/gdp.kson): Demonstrates how you can query an external data source (in this case, CSV file
  on GitHub.)
- [examples/join-gdp-and-population.kson](examples/join-gdp-and-population.kson): Fetch data from _two_ data sources (
  GDP by country and population by country) and perform a join to see GDP per capita.
- [examples/nested-references.kson](examples/nested-references.kson): Often external JSON data buries the important data
  in a nested structure. We can dereference arbitrarily deep into it.

## Grammar and Semantics

All of the [JSON grammar](https://www.json.org/json-en.html) is supported. In addition:

- A *reference* is denoted by `<<url>>`, where `url` is any non-empty string of characters that can be requested over
  the network or the local filesystem. By default, a reference will be compiled to its full contents in the generated
  JSON. To avoid that, you can write a reference like this:  `<<!url>>`, with an exclamation point. Now the reference
  will compile to to just `url`.
    - By default, a reference will attempt to automatically discover whether it's formatted as a JSON, CSV, or KSON,
      falling back to a string constant. You can provide a type hint like so: `<<url|json>>`, `<<url|csv>>`, etc.
    - If a URL cannot be resolved, an error will be thrown and JSON generation will fail.
    - To be precise, a remote JSON file will be compiled to its exact contents; a remote CSV file will be compiled to a
      list of dictionaries, where a best-effort attempt is made to convert numeric values to integers and/or floats; and
      a KSON file will be just treated as more KSON (although the namespace of aliases must remain globally unique, as
      discussed below.)
- An *alias* can be added after any token - a string, an array, a dictionary, and especially after a reference. Suppose
  you have a token `token` (perhaps `token` is `"hello world"`, or `123`, or `<<https://json.org>>`) -- then you may
  also write the token as `token as myAliasName`, eg `123 as myNumber`, `<<https://json.org>> as someRef`.
    - Aliases must be globally unique (as a consequence, it would be a syntax error for a kson file with aliases to
      reference itself).
    - The alias can be referenced in SQL queries by prepending with `$`; for example, an alias `someRef` can be
      addressed as `$someRef`.
    - However, not all aliases will be pointing at something useful for a SQL query; we can only write queries against
      scalar values (strings and numbers) or against tables. A table can be constructed from a list of dictionaries
      pointing to scalars with consistent types. We can also coerce a list of scalars to a table by constructing a table
      with a single column whose name is the alias for the list.
    - We will recurse on nested dictionary structures until we find a scalar or table value. For instance, suppose that
      you reference a remote document as in Fig. 1, aliased as `doc`, and you wish to query the list of scalars `baz`.
      Then in your SQL query, you can call `select * from "$doc$foo$bar$baz"`. (As an aside, **quotes are generally
      required**
      around the SQL alias references to parse properly.)
    - **You must define an alias before it is used in a SQL query**, so typically references will be placed toward the
      top of a file.

```json
{
  "foo": {
    "bar": {
      "baz": [
        1,
        2,
        3,
        4
      ]
    },
    "someValue": 42
  }
}
```

Fig. 1

- A SQL query is delimited by triple backticks (\`\`\`) before and after. SQL queries can contain aliases to objects in
  your document, as described above. The SQL queries are executed by an in-memory sqlite engine.
    - The output of a SQL query is usually returned as a list of dictionaries, but there are two exceptions. If only one
      column is in the output, a list of scalars will be returned instead. If there is only one column and, in addition,
      you use the directive `limit 1` in your query, then the result will be returned as a single scalar value.

## Tests

You can run the tests by cloning the repository and then:

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest tests
```

In all candidness, there are likely many edge cases, so if you find one, it would be greatly appreciated if you would make a bug
report and we can add a regression test.

## FAQ

### How does this work?

It's pretty simple, actually: First we [parse the KSON file](https://en.wikipedia.org/wiki/Recursive_descent_parser).
Where JSON has arrays and dictionaries, we throw in a few extra types - refs, aliases, and SQL queries.

To compile the file, we traverse the tree, making network requests, building appropriately-named SQLite tables, and
performing SQL queries as we go, eventually collapsing the whole business to JSON.

Some constraints of this approach are that we make network requests in serial, and that you must define an alias before
any SQL queries which use it.

### What's the motivation for this project?

For reasons which are best elided, I had to write an enormous number of JSON parsers in a short period of time, and then
got some additional ideas about the format. It's called "KSON" because k comes after j, get it? :-)
