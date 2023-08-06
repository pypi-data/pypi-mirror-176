#
#  SPDX-FileCopyrightText: 2022 Thorsten Hapke <thorsten.hapke@sap.com>
#
#  SPDX-License-Identifier: Apache-2.0
#


import logging
import argparse
import json
from os import getcwd, path, listdir

from rdflib import Graph
from tabulate import tabulate


def query(graph, statement):
    #logging.info(f"Query: {statement}")
    query_result = graph.query(statement)
    if len(query_result.vars) > 1:
        results = [{v: r[v] for v in query_result.vars} for r in query_result]
        str_results = tabulate([[v for v in r.values()]for r in results],headers=query_result.vars)
    else:
        var = query_result.vars[0]
        results = set([r[var] for r in query_result])
        str_results = tabulate([[r] for r in results], headers=query_result.vars)
    return results, str_results

def main():
    logging.basicConfig(level=logging.DEBUG)
    #
    # command line args
    #
    description = "SPARQL command on rdf-files."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('resource', help='Resource file')
    parser.add_argument('query', help='SPARQL query of file with SPARQL query ')
    args = parser.parse_args()

    # Read Resources
    g = Graph()
    g.parse(args.resource)
    #print(g.serialize(format='ttl'))

    resource = path.basename(args.resource)

    # Read Queries
    if args.query[-5:].lower() == '.json':
        with open(args.query) as fp:
            queries = json.load(fp)
    else:
        queries = {resource: [args.query]}

    for q in queries[resource]:
        results, str_result = query(g, q)
        print(f"\nQuery: {q}")
        print(str_result)


if __name__ == '__main__':
    main()
