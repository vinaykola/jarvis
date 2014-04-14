from py2neo import neo4j
from py2neo import node,rel
from py2neo import neo4j
from collections import defaultdict

filename = './output1.csv'

nodes = []
char_to_node_mapping = {}
edges = []

num = 0
with open(filename) as fil:
    for line in fil:
        n1,n2,pol = line.rstrip().split('\t')
        pol = int(pol)
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
nodes = {node1['name']:node1 for node1 in nodes}.values() 


# Generate mapping from character names to node numbers
for i,node2 in enumerate(nodes):
    char_to_node_mapping[node2['name']] = i

neo4j_edges = []

# Put edges in the correct format for neo4j
for n1,n2,pol in edges:
    try:
        if pol == 1:
            neo4j_edges.append((char_to_node_mapping[n1],"FRIEND",char_to_node_mapping[n2]))
        else:
            neo4j_edges.append((char_to_node_mapping[n1],"FOE",char_to_node_mapping[n2]))
    except:
        print "error"

#print "neo4j edges"
#for word in neo4j_edges:
 #   print word

neo4j._add_header('X-Stream', 'true;format=pretty')
characters_db1 = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
characters_db1.clear()

for word in nodes:
    temp = batch.create(node(word))
    listOfNodeReferences[num] = temp
    num+=1
for word in neo4j_edges:
    batch.create(rel(listOfNodeReferences[word[0]], word[1], listOfNodeReferences[word[2]]))


results = batch.submit()
file1 = open("output.txt","w")
a = list()
for word in results:
    file1.write(str(word['name']) + "\n")
  
print "Completed"


