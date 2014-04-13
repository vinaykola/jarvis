from py2neo import neo4j
from py2neo import node,rel
from py2neo import neo4j
from collections import defaultdict

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

#print nodes[:10]
#print
#print neo4j_edges[:10]x

characters_db1 = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
characters_db1.clear()
batch = neo4j.WriteBatch(characters_db1)
listOfNodeReferences = defaultdict()
temp = ""
num = 0
#a1 = batch.create(node(name="Superman"))
#a2 = batch.create(node(name="Batman"))

#rel(a1, "PLAYS", a2),

for word in nodes:
    temp = batch.create(node(word))
    listOfNodeReferences[num] = temp
    num+=1

for word in neo4j_edges:
 #   print listOfNodeReferences[word[0]],word[1],listOfNodeReferences[word[2]]
    batch.create(rel(listOfNodeReferences[word[0]], word[1], listOfNodeReferences[word[2]]))

try:
    results = batch.submit()
except:
    print "Encountered exception"
file1 = open("output.txt","w")
file1.write(results)
for word in results:
    file1.write(word["name"])
print "Completed"


