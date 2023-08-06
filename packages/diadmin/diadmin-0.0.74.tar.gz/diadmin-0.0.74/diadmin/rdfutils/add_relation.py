import os
from rdflib import Graph, Namespace

#file = 'tmp/datasets_DDL_instances.ttl'
file = 'tmp/datasets_HANA_DQM.ttl'
g = Graph()
g.parse(file)

dimd = Namespace("https://www.sap.com/products/data-intelligence#")
g.bind("dimd", dimd)

# Add References
columns_query = "SELECT DISTINCT ?column WHERE { ?column rdf:type dimd:Column .}"
qres = g.query(columns_query)
columns = list()
for row in qres:
    columns.append((row.column, row.column.split('/')[-1]))

print(columns)

for i in range(0, len(columns)):
    for j in range(i + 1, len(columns)):
        if columns[i][1] == columns[j][1]:
            g.add((columns[i][0], dimd.Reference, columns[j][0]))
            g.add((columns[j][0], dimd.Reference, columns[i][0]))

root_filename, suffix = os.path.splitext(file)
out_file = root_filename + "_addons.ttl"
print(f'Write file to: {out_file}')
with open(out_file, 'w') as fp:
    fp.write(g.serialize())
