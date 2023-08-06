#
#  SPDX-FileCopyrightText: 2022 Thorsten Hapke <thorsten.hapke@sap.com>
#
#  SPDX-License-Identifier: Apache-2.0
#

import logging
import argparse
import re
import os


from tabulate import tabulate
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD

from owlrl import RDFS_Semantics, DeductiveClosure

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def split_statement_token(raw_token, variables, namespaces):
    if raw_token in variables:
        return variables[raw_token]
    if any([x in raw_token for x in "([{"]):
        split_stmt = re.match(r'(\w*)[\[\{\(]*(\w*):(\w*)[\]\}\)]*', raw_token)
        token = {'variable': split_stmt.group(1), 'prefix': split_stmt.group(2), 'resource': split_stmt.group(3)}
    else:
        split_stmt = re.match(r'(\w*):(\w*)', raw_token)
        token = {'variable': None, 'prefix': split_stmt.group(1), 'resource': split_stmt.group(2)}

    if not token['prefix']:
        token['prefix'] = 'dft'
    namespaces.add(token['prefix'])
    if token['variable']:
        variables[token['variable']] = token
    return token


def read_mermaid(file):
    variables = dict()
    triplets = list()
    namespaces_names = set()
    with open(file) as fp:
        lines = filter(None, (line.rstrip() for line in fp))
        for line in lines:
            statement = re.match(r'(\S+)\s*\-\.*\-+\>*\s*(\S+)\s*\-\.*\-+\>*\s*(\S+)$', line.strip())
            subj = split_statement_token(statement.group(1).strip(), variables, namespaces_names)
            pred = split_statement_token(statement.group(2).strip(), variables, namespaces_names)
            obj = split_statement_token(statement.group(3).strip(), variables, namespaces_names)
            logging.debug(f'{subj} -- {pred} --> {obj}')
            triplets.append((subj, pred, obj))
            namespaces_names.add(subj['prefix'])
            namespaces_names.add(subj['prefix'])

    g = Graph()
    # namespaces
    namespaces = dict()
    for n in namespaces_names:
        match n:
            case 'rdf':
                namespaces[n] = RDF
                g.bind('rdf', RDF)
            case 'rdfs':
                namespaces[n] = RDFS
                g.bind('rdfs', RDFS)
            case 'xsd':
                namespaces[n] = XSD
                g.bind('xsd', XSD)
            case _:
                namespaces[n] = Namespace(URIRef(f"http://{n}.mmd#"))
                g.bind(n, namespaces[n])

    # triplets
    for t in triplets:
        logging.debug(f"{namespaces[t[0]['prefix']]} - {namespaces[t[0]['prefix']][t[0]['resource']]}")
        subj = namespaces[t[0]['prefix']][t[0]['resource']]
        pred = namespaces[t[1]['prefix']][t[1]['resource']]
        obj = namespaces[t[2]['prefix']][t[2]['resource']]
        g.add((subj, pred, obj))

    return g

def cstr(str, color):
    return f"{color}{str}{bcolors.ENDC}"


def query(graph, statement):
    query_result = graph.query(statement)
    if len(query_result.vars) > 1:
        results = [{v: r[v] for v in query_result.vars} for r in query_result]
        headers = [f"{bcolors.OKBLUE}{v}{bcolors.ENDC}" for v in query_result.vars]
        str_results = tabulate([[cstr(v, bcolors.OKBLUE) for v in r.values()]for r in results], headers=headers)
    else:
        var = query_result.vars[0]
        results = set([r[var] for r in query_result])
        headers = [f"{bcolors.OKBLUE}{v}{bcolors.ENDC}" for v in query_result.vars]
        str_results = tabulate([[cstr(r, bcolors.OKBLUE)] for r in results], headers=headers)
    return results, str_results


def main():
    #
    # command line args
    #
    description = "Mermaid formatted file to turtle-file."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('file', help='mermaid file')
    parser.add_argument('-s', '--sparql', help='sparql query')
    parser.add_argument('-o', '--output', help='Saves file in \'turtle\'-format with same basename', action='store_true')
    parser.add_argument('-d', '--debug', help='DEBUG logging level', action='store_true')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    root_filename, suffix = os.path.splitext(args.file)
    g = Graph()
    match suffix:
        case '.mmd':
            g = read_mermaid(args.file)
        case '.ttl':
            g.parse(args.resource)
        case _:
            logging.error(f"Unknown file-format: {suffix}")

    if args.output:
        output = root_filename + ".ttl"
        with open(output, 'w') as fp:
            fp.write(g.serialize())

    # Expand graph for RDFS semantics
    DeductiveClosure(RDFS_Semantics).expand(g)

    if args.sparql:
        results, str_result = query(g, args.sparql)
        print(f"\n{bcolors.HEADER}Query: {args.sparql}{bcolors.ENDC}\n")
        print(f"{str_result}\n")


if __name__ == '__main__':
    main()

