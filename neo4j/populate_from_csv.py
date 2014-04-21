from py2neo import neo4j
from py2neo import node,rel
from py2neo import neo4j
from collections import defaultdict
import unpickle
from random import randint

filename = './output1.csv'

nodes = []
char_to_node_mapping = {}
edges = []

num = 0
'''
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
#    print word
'''
def insertIntoDb(filename1):
    print "Inserting into db"
    neo4j._add_header('X-Stream', 'true;format=pretty')
    characters_db1 = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
    characters_db1.clear()
    nodes = unpickle.unpickle(filename1)
    num = 0
    batch = neo4j.WriteBatch(characters_db1)
    listOfNodeReferences = defaultdict()
    temp = ""
    for word in nodes:
        dict1 = {}
       # print word
        print word['name']
        dict1['name'] = word['name']
        temp = batch.create(node(dict1))
        batch.set_property(temp, 'info_url',word['site_detail_url'])
        try:
            batch.set_property(temp, 'image',word['image']['thumb_url'])
        except:
            batch.set_property(temp, 'image','')
        listOfNodeReferences[num] = temp
        num+=1
    print "Inserted nodes"
    for i in xrange(70000):
        random1 = randint(0,len(listOfNodeReferences))
        random2 = randint(0,len(listOfNodeReferences))
        while random2==random1:
            random2 = randint(0,len(listOfNodeReferences))
        random3 = randint(1,5)
        try:
            temp = batch.create(rel(listOfNodeReferences[random2], 'Edge', listOfNodeReferences[random1]))
        except:
            continue
        batch.set_property(temp,'similarity',random3)
        break
    print "Inserted edges"
    results = batch.submit()
    return results
    '''
    file1 = open("output.txt","w")
    a = list()
    print results
    for word in results:
       # print word
        try:
            file1.write(str(word['name']) + "\n")
            print word['name']
            print word['gender']
        except:
            continue
    '''
insertIntoDb("heroes788_allfeatures_32000.pkl")

print "Completed"


