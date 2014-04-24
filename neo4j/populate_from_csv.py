from py2neo import neo4j
from py2neo import node,rel
from py2neo import neo4j
from collections import defaultdict
import unpickle
from random import randint
import cPickle as pickle
import numpy as np

filename = './output1.csv'

nodes = []
char_to_node_mapping = {}
edges = []

num = 0

def unpickle(filename):
    f = open(filename,"rb") 
    heroes = pickle.load(f)
    return heroes

edges = unpickle('similarity_matrix_0_4000.pkl')
for num in range(4000,56000,4000):
    edges = np.vstack((a,unpickle('similarity_matrix_'+str(num)+'_'+str(num+4000)+'.pkl')))
nodes = unpickle('heroes788_allfeatures_56000.pkl')

print "obtained nodes and edges "

def insertIntoDb(filename1):
    print "Inserting into db"
    neo4j._add_header('X-Stream', 'true;format=pretty')
    characters_db1 = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
    characters_db1.clear()
    #nodes = unpickle.unpickle(filename1)
    num = 0
    batch = neo4j.WriteBatch(characters_db1)
    listOfNodeReferences = defaultdict()
    temp = ""
    #Nodes insertion
    try:
        for i in xrange(len(nodes)):
            dict1 = {}
            dict1['name'] = nodes[i]['name']
            temp = batch.create(node(dict1))
            
            batch.set_property(temp, 'gender',nodes[i]['gender'])
            try:
                batch.set_property(temp, 'image',nodes[i]['image']['thumb_url'])
            except:
                batch.set_property(temp, 'image','')
            batch.set_property(temp,'first_appeared_in_issue',nodes[i]['first_appeared_in_issue']['name'])
            batch.set_property(temp,'count_of_issue_appearances',nodes[i]['count_of_issue_appearances'])
            batch.set_property(temp,'publisher',nodes[i]['publisher']['name'])
            batch.set_property(temp,'creators',",".join([word[0] for word in nodes[i]['creators']]))

            listOfNodeReferences[i] = temp

        print "Inserted nodes"
        for i in xrange(len(edges)):
            for j in xrange(10):
                temp = batch.create(rel(listOfNodeReferences[i], 'Edge', listOfNodeReferences[edges[i]]))
        print "Inserted edges"
    except:
        print "interrupted"
    results = batch.submit()
    return results

insertIntoDb("heroes788_allfeatures_32000.pkl")

print "Completed"


