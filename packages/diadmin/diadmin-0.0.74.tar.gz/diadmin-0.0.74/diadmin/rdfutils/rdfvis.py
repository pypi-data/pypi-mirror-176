#
#  SPDX-FileCopyrightText: 2022 Thorsten Hapke <thorsten.hapke@sap.com>
#
#  SPDX-License-Identifier: Apache-2.0
#

import logging
import argparse
import os
from pyvis.network import Network
from rdflib import Graph




#
#  Converts rgb to hex
#
def rgb2hex(rgb: tuple) -> str:
    return "#{:x}{:x}{:x}{:x}{:x}{:x}".format(divmod(rgb[0], 16)[0], divmod(rgb[0], 16)[1], divmod(rgb[1], 16)[0],
                                             divmod(rgb[1], 16)[1], divmod(rgb[2], 16)[0], divmod(rgb[2], 16)[1])

#
#  MAIN function
#
def main():
    #
    # command line args
    #
    description = "Visualize"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('file', help='RDF-ttl file')
    parser.add_argument('-d', '--debug', help='DEBUG logging level', action=argparse.BooleanOptionalAction)
    parser.add_argument('-l', '--lineage', help='Show lineages', action=argparse.BooleanOptionalAction)
    parser.add_argument('-r', '--reference', help='Show References', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # PARAMETERS
    orange = rgb2hex((237, 171, 42))  #orange_rgb = '#EDAB25'  # (237,171,42)
    orange_light = '#FDCF67'  # (253, 207, 103)
    purple_light = '#DE6BEF'
    purple = rgb2hex((222, 107, 232))
    green = rgb2hex((75, 175, 46))
    width = 2

    g = Graph()
    logging.info(f"Read RDF-file: {args.file}")
    g.parse(args.file)
    file2 = 'tmp/datasets_DDL_instances.ttl'
    logging.info(f"Read RDF-file: {file2}")
    g.parse(file2)

    pg = Network(height='100%', width='100%', bgcolor='black', font_color='white')

    if not args.lineage and not args.reference:
        logging.info('Add datasets and columns only')
        # Datasets and Columns
        query = "SELECT DISTINCT ?dataset ?column WHERE { ?dataset dimd:hasColumn ?column .}"
        results = g.query(query)
        for row in results:
            pg.add_node(row.dataset, label=row.column.split('/')[-1], color='white')
            pg.add_node(row.column, label=row.column.split('/')[-1], color=orange)
            pg.add_edge(row.dataset, row.column, label='', color=orange_light)
    else:
        # Datasets
        logging.info('Add datasets')
        query = "SELECT DISTINCT ?dataset WHERE { ?dataset a dimd:Dataset .}"
        results = g.query(query)
        for row in results:
            pg.add_node(row.dataset, label=row.dataset.split('/')[-1], color='white')

        # Datasets and Columns
        logging.info('Add columns')
        query = "SELECT DISTINCT ?dataset ?column WHERE { ?dataset dimd:hasColumn ?column .}"
        results = g.query(query)
        for row in results:
            pg.add_node(row.column, label=row.column.split('/')[-1], color=orange)
            try:
                pg.add_edge(row.dataset, row.column, label='',  color=orange_light, width=width)
            except AssertionError as ae:
                logging.error(f"Error adding edge: {row.dataset} -> {row.column} ({ae})")

        # Lineage
        if args.lineage:
            logging.info('Add lineage connections')
            query = "SELECT DISTINCT ?dataset1 ?dataset2 WHERE { ?dataset1 dimd:Lineage ?dataset2 .}"
            results = g.query(query)
            for row in results:
                try:
                    pg.add_edge(row.dataset1, row.dataset2, label='lineage', color=purple, width=width)
                except AssertionError as ae:
                    logging.error(f"Adding lineage error: {ae}")

        # References
        if args.reference:
            logging.info('Add column references')
            query = "SELECT ?column1 ?column2 WHERE { ?column1 dimd:Reference ?column2 .}"
            results = g.query(query)
            for row in results:
                pg.add_edge(row.column1, row.column2, label='', color=green, width=width)

    logging.info(f"Number of nodes: {len(pg.nodes)}")

    root_filename, suffix = os.path.splitext(args.file)
    output = root_filename + ".html"
    logging.info(f"Save file to: {output}")

    pg.show_buttons(filter_=['physics'])
    pg.show(output)


#
# Main Function Call
#
if __name__ == '__main__':
    main()
