#
#  SPDX-FileCopyrightText: 2022 Thorsten Hapke <thorsten.hapke@sap.com>
#
#  SPDX-License-Identifier: Apache-2.0
#

import logging
import json
import os
from pprint import pprint

from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, XSD
from owlrl import RDFS_Semantics, DeductiveClosure

logging.basicConfig(level=logging.INFO)


def main():

    filename = 'tmp/datasets_HANA_DQM.json'
    with open(filename) as fp:
        datasets = json.load(fp)

    # create Graph
    g = Graph()
    di_url = 'https://www.sap.com/products/data-intelligence#'
    dimd = Namespace(f"{di_url}#")
    dilinto = Namespace(f"{di_url}/lineageTo")
    dilinfrom = Namespace(f"{di_url}/lineageFrom")
    g.bind("dimd", dimd)
    g.bind('dilinto', dilinto)
    g.bind('dilinfrom', dilinfrom)

    g.add((dimd.Table, RDFS.subClassOf, dimd.Dataset))
    g.add((dilinto.COMPUTATION_BLACKBOX, RDFS.domain, dimd.Dataset))
    g.add((dilinto.COMPUTATION_BLACKBOX, RDFS.range, dimd.Dataset))
    g.add((dilinfrom.COMPUTATION_BLACKBOX, RDFS.domain, dimd.Dataset))
    g.add((dilinfrom.COMPUTATION_BLACKBOX, RDFS.range, dimd.Dataset))

    # Base URL of instance
    dicatalog = 'https://vsystem.xxx.ondemand.com/default/catalog'

    for dataset in datasets:
        dataset_uri = URIRef(f"{dicatalog}/dataset/{dataset['metadata']['connectionId']}{dataset['metadata']['uri']}")
        dataset_type = dataset['metadata']['type'].capitalize()
        g.add((dataset_uri, RDF.type, dimd[dataset_type]))
        for column in dataset['columns']:
            column_uri = URIRef(dataset_uri+'/'+column['name'])
            g.add((dataset_uri, dimd.hasColumn, column_uri))
            g.add((column_uri, RDF.type, dimd.Column))
            g.add((column_uri, dimd.DataType, Literal(column['type'])))
            g.add((column_uri, dimd.TemplateDataType, Literal(column['templateType'])))
            if 'length' in column:
                g.add((column_uri, dimd.FieldLength, Literal(column['length'])))
        if 'tags' in dataset:
            if 'tagsOnDataset' in dataset['tags']:
                for dtag in dataset['tags']['tagsOnDataset']:
                    hierarchy_uri = f"{dicatalog}/hierarchy/{dtag['hierarchyName']}"
                    for tag in dtag['tags']:
                        tag_path = tag['tag']['path'].replace('.', '/')
                        tag_path = tag_path.replace(' ', '%20')
                        tag_uri = URIRef(f"{hierarchy_uri}/{tag_path}")
                        g.add((dataset_uri, dimd.hasTag, tag_uri))
            if 'tagsOnAttribute' in dataset['tags']:
                for atag in dataset['tags']['tagsOnAttribute']:
                    column_uri = URIRef(dataset_uri + '/' + atag['attributeQualifiedName'])
                    for tag in atag['tags']:
                        hierarchy_uri = f"{dicatalog}/hierarchy/{tag['hierarchyName']}"
                        for tag2 in tag['tags']:
                            tag_path = tag2['tag']['path'].replace('.', '/')
                            tag_path = tag_path.replace(' ', '%20')
                            tag_uri = URIRef(f"{hierarchy_uri}/{tag_path}")
                            g.add((column_uri, dimd.hasTag, tag_uri))
        if 'lineage' in dataset and isinstance(dataset['lineage'],dict):
            for pcn in dataset['lineage']['publicComputationNodes']:
                for transform in pcn['transforms']:
                    for computation in transform['datasetComputation']:
                        lineage_to = dilinto[computation['computationType']]
                        lineage_from = dilinfrom[computation['computationType']]
                        in_uris = [URIRef(f"{dicatalog}/dataset/{ind['externalDatasetRef']}")
                                   for ind in computation['inputDatasets']]
                        out_uris = [URIRef(f"{dicatalog}/dataset/{ind['externalDatasetRef']}")
                                    for ind in computation['outputDatasets']]
                        for i in in_uris:
                            for o in out_uris:
                                g.add((i, lineage_to, o))
                                g.add((o, lineage_from, i))


    # Add References
    columns_query = "SELECT DISTINCT ?column WHERE { ?column rdf:type dimd:Column .}"
    qres = g.query(columns_query)
    columns = list()
    for row in qres:
        columns.append((row.column, row.column.split('/')[-1]))

    for i in range(0, len(columns)):
        for j in range(i+1, len(columns)):
            if columns[i][1] == columns[j][1]:
                g.add((columns[i][0], dimd.Reference, columns[j][0]))
                g.add((columns[j][0], dimd.Reference, columns[i][0]))

    # Expand graph for RDFS semantics
    DeductiveClosure(RDFS_Semantics).expand(g)
    rdf_str = g.serialize()

    # print(f"Result:\n{g.serialize()}")
    root_filename, suffix = os.path.splitext(filename)
    output = root_filename + ".ttl"
    logging.info(f"Save file to: {output}")
    g.serialize(destination=output)


#
# Main Function Call
#
if __name__ == '__main__':
    main()
