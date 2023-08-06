
import logging

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS


#
# MAIN
#
def main():

    logging.basicConfig(level=logging.INFO)

    g = Graph()

    # Name spaces
    di_url = 'https://www.sap.com/products/data-intelligence#'
    ndi = Namespace(di_url)
    g.namespace_manager.bind('di', URIRef(ndi))

    host = 'https://vsystem.ingress.dh-1svpfuea.dhaas-live.shoot.live.k8s-hana.ondemand.com/default'
    instance = Namespace(host)
    g.bind('instance', URIRef(instance))

    di_metadata_explorer = URIRef(di_url[:-1]+'metadata_explorer')
    metadata_explorer1 = URIRef(host[:-1] + 'metadata_explorer')
    metadata_explorer2 = instance['metadata_explorer']
    g.add((metadata_explorer1, RDF.type, di_metadata_explorer))
    g.add((metadata_explorer2, RDF.type, di_metadata_explorer))


if __name__ == '__main__':
    main()
