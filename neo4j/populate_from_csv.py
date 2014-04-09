from py2neo import neo4j
from py2neo import node,rel

characters_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

filename = './output1.csv'

nodes = []
char_to_node_mapping = {}
edges = []

with open(filename) as fil:
    for line in fil:
        n1,n2,pol = line.rstrip().split('\t')
        
        # Put nodes in the format for neo4j
        node1 = {}
        node1['name'] = n1
        nodes.append(node1)

        node2 = {}
        node2['name'] = n2
        nodes.append(node2)

        edges.append((n1,n2,pol))
        edges.append((n2,n1,pol))
        
        
# Make the list of nodes unique
nodes = {node['name']:node for node in nodes}.values() 

# Generate mapping from character names to node numbers
for i,node in enumerate(nodes):
    char_to_node_mapping[node['name']] = i

neo4j_edges = []

# Put edges in the correct format for neo4j
for n1,n2,pol in edges:

    try:
        if pol == 1:
            neo4j_edges.append((char_to_node_mapping[n1],"FRIEND",char_to_node_mapping[n2]))
        else:
            neo4j_edges.append((char_to_node_mapping[n1],"FOE",char_to_node_mapping[n2]))
    except:
        print n1,n2,pol

#print nodes[:10]
#print
#print neo4j_edges[:10]
