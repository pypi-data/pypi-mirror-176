#
#  SPDX-FileCopyrightText: 2022 Thorsten Hapke <thorsten.hapke@sap.com>
#
#  SPDX-License-Identifier: Apache-2.0
#

import logging
import argparse
import string
import re
import os
from rdflib import Graph
from pprint import pprint
from difflib import SequenceMatcher


def main():
    #
    # command line args
    #
    description = "RDF to Mermaid"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('file', help='RDF-ttl file')
    parser.add_argument('-s', '--sparql', help='sparql query')
    parser.add_argument('-o', '--output', help='Saves file in \'turtle\'-format with same basename', action='store_true')
    parser.add_argument('-d', '--debug', help='DEBUG logging level', action='store_true')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    g = Graph()
    g.parse(args.file)

    term_map = dict()
    mmd_str = "```mermaid\nflowchart TD\n\n"
    counter = 0
    for subj, pred, obj in g:
        pm = pred.n3(g.namespace_manager)

        s = subj.n3(g.namespace_manager)
        if re.match(r'http[s]*:', subj):
            s = re.sub(r'https*:.+\.com\/', '', subj)
        if s not in term_map:
            term_map[s] = 'r'+str(counter)
            counter += 1
            sm = f"{term_map[s]}[{s}]"
        else:
            sm = term_map[s]

        o = obj.n3(g.namespace_manager)
        if re.match(r'https*:', obj):
            o = re.sub(r'https*:.+\.com\/', '', obj)
        if o not in term_map:
            term_map[o] = 'r'+str(counter)
            counter += 1
            om = f"{term_map[o]}[{o}]"
        else:
            om = term_map[o]

        mmd_str += f"    {sm} -- {pm} --> {om}\n"
    mmd_str += "\n```"

    root_filename, suffix = os.path.splitext(args.file)
    output = root_filename + ".mmd"
    logging.info(f"Save file to: {output}")
    with open(output, 'w') as fp:
        fp.write(mmd_str)

#
# Main Function Call
#
if __name__ == '__main__':
    main()

