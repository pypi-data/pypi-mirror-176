#
#  SPDX-FileCopyrightText: 2022 Thorsten Hapke <thorsten.hapke@sap.com>
#
#  SPDX-License-Identifier: Apache-2.0
#

import logging
import argparse
import re
import os

from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD



def get_bracket_content(string) -> (str, str):
    start = re.search(r"\(", string).start()+1
    brackets_counter = 1
    # print(f"Content bracket: {string[start:]}")
    for i, c in enumerate(string[start:]):
        if c == ')':
            if brackets_counter == 0:
                break
            else:
                brackets_counter -= 1
        if c == '(':
            brackets_counter += 1
    # print(f"Return: {string[:start-1]}, {string[start+1:i + start]}")
    return string[:start-1], string[start+1:i + start]


#
# Split string but consider brackets '()'
#
def split(string, sep=',') -> list:
    parts = list()
    brackets_counter = 0
    start_part = 0
    for i, c in enumerate(string):
        match c:
            case '(': brackets_counter += 1
            case ')': brackets_counter -= 1
            case ',':
                if brackets_counter == 0:
                    parts.append(string[start_part:i])
                    start_part = i + 1
    if brackets_counter == 0 and string[-1] == ')':
        parts.append(string[start_part:])

    return parts


def read_sqlfile(file) -> list:
    with open(file) as fp:
        sql_statements = fp.read()

    sql_statements = sql_statements.split('\n\n')

    tables = list()
    for sql_statement in sql_statements:

        sql_statement = sql_statement.strip()
        create_search = re.search("CREATE", sql_statement)
        if not create_search or create_search.start() > 0:
            raise ValueError("Wrong create format")
        sql_statement = sql_statement.replace('\n', '').replace('\t', '')
        pre_bracket, content_bracket = get_bracket_content(sql_statement)

        # table name
        tags = pre_bracket.split(' ')
        table_name = tags[tags.index('TABLE')+1].strip('"')

        # table definition
        lines = split(content_bracket)
        columns = list()
        primary_keys = list()
        foreign_keys = list()
        for line in lines:
            if "PRIMARY KEY" in line:
                primary_keys = re.match(r".+\((.+)\)", line).group(1).split(',')
                primary_keys = [pk.strip().strip('"') for pk in primary_keys]
                continue
            if "FOREIGN KEY" in line:
                try:
                    b = re.match(r"FOREIGN KEY\((.+)\)\s*REFERENCES\s+(.+)\s+\((.+)\)", line)
                    foreign_keys.append({"foreign_key": b.group(1).strip('"'), "reference_table": b.group(2).strip('"'),
                                         "reference_column": b.group(3).strip('"')})
                except AttributeError as ae:
                    logging.error(f"Parse error: {line}: {ae}")
                continue
            not_null = True if re.search("NOT NULL", line, re.IGNORECASE) else False
            tags = line.split(' ')
            column_name = tags[0]
            data_type = tags[1]
            size = None
            frac_decimals = None
            if '(' in tags[1]:
                try:
                    if ',' in tags[1]:
                        b = re.match(r'(.+)\((\d+),(\d+)\)', tags[1])
                        data_type = b.group(1)
                        size = int(b.group(2))
                        frac_decimals = int(b.group(3))
                    else:
                        b = re.match(r'(.+)\((\d+)\)', tags[1])
                        data_type = b.group(1)
                        size = b.group(2)
                        frac_decimals = None
                except AttributeError:
                    logging.error(f"Parse error: {tags[1]}")
            if "COMMENT" in tags:
                comment = tags[tags.index('COMMENT')+1]
            columns.append({'name': column_name.strip('"').strip("'"), 'data_type': data_type, 'size': size,
                            'frac_decimals': frac_decimals, 'not_null': not_null, 'comment': comment.strip("'")})

        tables.append({'table_name': table_name, 'columns': columns, 'primary_keys': primary_keys,
                       'foreign_keys': foreign_keys})

    return tables


def main():
    #
    # command line args
    #
    description = "Creates rdf-file from CREATE statement."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('file', help='sql file')
    parser.add_argument('-o', '--output', help='Saves file in \'turtle\'-format with same basename', action='store_true')
    parser.add_argument('-d', '--database', help='Database host', default='https://xxx.hanacloud.ondemand.com')
    parser.add_argument('-s', '--schema', help='Schema', default='TEST_SCHEMA')

    args = parser.parse_args()

    db = args.database
    schema = args.schema

    logging.basicConfig(level=logging.INFO)

    # Read sql CREATE statements
    tables = read_sqlfile(args.file)

    # create Graph
    g = Graph()

    dimd = Namespace("https://www.sap.com/products/data-intelligence#")
    g.bind("dimd", dimd)
    table_cls = dimd.Table
    column_cls = dimd.Column
    column_rel = dimd.hasColumn
    hana_datatype_rel = dimd.hasHanaDataType
    field_size_rel = dimd.hasFieldSize
    frac_decimals_rel = dimd.hasFractionDecimals
    primary_key_rel = dimd.hasPrimaryKey
    reference = dimd.hasReference

    g.add((column_rel, RDFS.domain, table_cls))
    g.add((column_rel, RDFS.range, column_cls))
    g.add((primary_key_rel, RDFS.domain, table_cls))
    g.add((reference, RDFS.domain, column_cls))
    g.add((reference, RDFS.range, column_cls))

    #g.add((ndb[schema], RDF.type, dimd['DB_Schema']))

    for table in tables:
        table_uri = URIRef(f"{db}/{schema}/{table['table_name']}")
        #table_uri.n3(g.namespace_manager)
        g.add((table_uri, RDF.type, table_cls))
        for column in table['columns']:
            column_uri = URIRef(f"{db}/{schema}/{table['table_name']}/{column['name']}")
            g.add((column_uri, RDF.type, column_cls))
            g.add((table_uri, column_rel, column_uri))
            g.add((column_uri, hana_datatype_rel, dimd[column['data_type']]))
            if column['size']:
                g.add((column_uri, field_size_rel, Literal(column['size'])))
            if column['frac_decimals']:
                g.add((column_uri, frac_decimals_rel, Literal(column['frac_decimals'])))
        for pk in table['primary_keys']:
            column_uri = URIRef(f"{db}/{schema}/{table['table_name']}/{pk}")
            g.add((table_uri, primary_key_rel, column_uri))

        if table['primary_keys']:
            for pk in table['primary_keys']:
                column_uri = URIRef(f"{db}/{schema}/{table['table_name']}/{pk}")
                g.add((table_uri, primary_key_rel, column_uri))
        if table['foreign_keys']:
            for fk in table['foreign_keys']:
                from_column_uri = URIRef(f"{db}/{schema}/{table['table_name']}/{fk['foreign_key']}")
                to_column_uri = URIRef(f"{db}/{schema}/{fk['reference_table']}/{fk['reference_column']}")
                g.add((from_column_uri, reference, to_column_uri))

    print(f"Result:\n{g.serialize()}")
    if args.output:
        root_filename, suffix = os.path.splitext(args.file)
        output = root_filename + ".ttl"
        logging.info(f"Save file to: {output}")
        g.serialize(destination=output)


if __name__ == '__main__':
    main()

