#
#  SPDX-FileCopyrightText: 2021 Thorsten Hapke <thorsten.hapke@sap.com>
#
#  SPDX-License-Identifier: Apache-2.0
#

import logging
import argparse
from urllib.parse import urljoin

import json
from os import path

import yaml
import csv
import pandas as pd

from diadmin.metadata_api import catalog, container, connection
from diadmin.utils.utils import add_defaultsuffix, mksubdir,get_system_id


def main() :
    logging.basicConfig(level=logging.INFO)

    #
    # command line args
    #
    description =  "Upload and download catalog items."
    achoices = ['hierarchies','connections','containers','tags','datasets','metadata','autotag']
    parser = argparse.ArgumentParser(description=description)
    help_config = 'Specifies config_demo.yaml file with the parameters: URL, TENANT, USER, PWD'
    parser.add_argument('type',choices=achoices, help = "Catalog type [connections,containers] only download..")
    parser.add_argument('item',help = "Content file. if \'*\' default values are used w/o suffix [hierachies,tags,connections,containers,autotag]")
    parser.add_argument('-d','--download', help='Exports hierarchies',action='store_true')
    parser.add_argument('-u','--upload', help='Imports hierarchies (json-file with or w/o suffix)',action='store_true')
    parser.add_argument('-r','--remove', help='Removes connection_id',action='store_true')
    parser.add_argument('-f','--hierarchies_file', help='Use downloaded hierarchy_maps.json file instead of downloading it freshly',action='store_true')
    parser.add_argument('-c','--config', help = help_config,default='config.yamls')
    parser.add_argument('-s','--synced', help='Use synced file hierarchies.json',action='store_true')
    args = parser.parse_args()

    config_file = 'config.yaml'
    if args.config:
        config_file = add_defaultsuffix(args.config,'yaml')
    with open(config_file) as yamls:
        params = yaml.safe_load(yamls)

    conn = {'url': urljoin(params['URL'] , '/app/datahub-app-metadata/api/v1'),
            'auth':(params['TENANT']+'\\'+ params['USER'],params['PWD'])}

    sysid = get_system_id(params['URL'],params['TENANT'])

    catalog_directory = mksubdir('.','catalogs')

    if args.download :
        if args.type == 'hierarchies':
            hfilter = None if args.item == '*' else args.item
            filename = 'hierarchies.json' if args.item == '*' else args.item+'.json'
            filename = path.join(catalog_directory,filename)
            logging.info(f"Download hierarchies to {filename}")
            hierarchies = catalog.download_hierarchies(conn,hierarchy_name=hfilter)
            logging.info(f"Save file {filename}")
            with open(filename,'w') as fp:
                json.dump(hierarchies,fp,indent=4)

        elif args.type == 'connections':
            connection_id = None if args.item in ['*','all'] else args.item
            filename = 'connections.json' if args.item == '*' else 'connections_'+args.item+'.json'
            filename = path.join('connections',filename)
            logging.info(f"Download connections {args.item} to: {filename}")
            connections = connection.get_connections(conn,connection_id = connection_id)
            with open(filename,'w') as fp:
                json.dump(connections,fp,indent=4)

        elif args.type == 'containers':
            cfilter = None if args.item == '*' else args.item
            filename = 'containers.json' if args.item == '*' else 'containers_filtered.json'
            filename = path.join('catalogs',filename)
            logging.info(f"Download containers to: {filename}")
            root = {'id': 'connectionRoot','name': 'Root','qualifiedName': '/','catalogObjectType': 'ROOT_FOLDER'}
            containers = dict()
            containers = container.get_containers(conn,containers,root, container_filter=cfilter)
            with open(filename,'w') as fp:
                json.dump(containers,fp,indent=4)

        elif args.type == 'tags':
            if args.item == '*' :
                logging.error("Dataset needs to be specified for downloading tags.")
                return -1
            #tags_file = path.basename(args.item).split('.')[0] + '_tags.json'
            tags_file = path.join(catalog_directory,'dataset_tags.json')
            #tags_file = path.join(catalog_directory,tags_file)
            if path.isfile(tags_file) :
                logging.info(f"Existing file: {tags_file}")
                with open(tags_file,'r') as fp:
                    tags = json.load(fp)
            else :
                tags = dict()
            logging.info(f"Download dataset tags of: {args.item}")
            dataset_attributes = container.get_dataset_tags(conn,args.item)
            tags[args.item] = container.reduce_dataset_attributes(dataset_attributes)

            logging.info(f"Dataset tags saved to: {tags_file}")
            with open(tags_file,'w') as fp:
                json.dump(tags,fp,indent=4)


    if args.upload :
        if args.type == 'hierarchies':
            if args.item == '*':
                logging.error("No filename given to upload: {args.item}")
                return -1
            hierarchy_filename = add_defaultsuffix(args.item,'json')
            with open(path.join('catalogs',hierarchy_filename),'r') as fp:
                new_hierarchies = json.load(fp)

            hierarchies = None
            if args.synced :
                with open(path.join('catalogs','hierarchies.json'),'r') as fp:
                    hierarchies = json.load(fp)

            hierarchies = catalog.upload_hierarchies(conn,new_hierarchies,hierarchies)
            with open(path.join('catalogs','hierarchies.json'),'w') as fp:
                json.dump(hierarchies,fp,indent=4)

        elif args.type == 'tags' :
            tags_file = 'dataset_tags.json' if args.item == '*' else args.item

            with open(path.join(catalog_directory,tags_file),'r') as fp:
                dataset_tags = json.load(fp)

            if args.synced :
                with open(path.join(catalog_directory,'hierarchies.json'),'r') as fp:
                    hierarchies = json.load(fp)
            else :
                hierarchies = catalog.download_hierarchies(conn,hierarchy_name=None)

            for ds,dsv in dataset_tags.items():
                for dst in dsv['dataset_tags']:
                    hierarchy_id = hierarchies[dst]['hierarchy_id']
                    tag_id = hierarchies[dst]['tag_id']
                    container.add_dataset_tag(conn,ds,hierarchy_id,tag_id)
                for attribute, ast in dsv['attribute_tags'].items():
                    hierarchy_id = hierarchies[ast]['hierarchy_id']
                    tag_id = hierarchies[ast]['tag_id']
                    container.add_dataset_attribute_tag(conn,ds,hierarchy_id,tag_id,attribute)

        elif args.type == 'connections' :
            # load metadata_dataset
            conn_file = add_defaultsuffix(args.item,'json')
            with open(path.join('connections',conn_file)) as fp :
                conn_data = json.load(fp)
            connection.upload_connection(conn,conn_data)

        elif args.type == 'datasets':
            dataset_file = add_defaultsuffix(args.item,'json')
            with open(path.join('metadata_datasets',dataset_file)) as fp :
                dataset_data = json.load(fp)
            task = connection.upload_dataset(conn,dataset_data)
            logging.info(f"Upload Dataset Metadata. Task ID: {task}")

        else :
            logging.error('Only \'hierarchies\' and \'tags\' can be uploaded')
            return -1

    if args.remove:
        if args.type == 'connections':
            connection.delete_connection(conn,args.item)
        else :
            logging.error("Remove only implemented for type: \'connections\'.")

    if args.type == 'metadata':
        df = container.export_catalog(conn)
        filename = path.join('catalogs','metadata_'+sysid+'.csv')
        df.to_csv(filename,index = False)

    elif  args.type == 'autotag':
        tagmap = list()
        autotagfile = add_defaultsuffix(args.item,'csv')
        with open(path.join('catalogs',autotagfile)) as fp:
            csvreader = csv.reader(fp)
            header = next(csvreader)
            for row in csvreader:
                if row[0][0] == '#':
                    continue
                tagmap.append(row)

        metadata_df = container.export_catalog(conn)
        container.auto_tag(conn,metadata_df,tagmap)




if __name__ == '__main__':
    main()