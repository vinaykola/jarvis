from py2neo import neo4j
from py2neo import node,rel

characters_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

filename = './output1.csv'

nodes = []
edges = []

with open(filename) as fil:
    for line in fil:
        n1,n2,pol = line.rstrip().split('\t')
        print n1,n2,pol
        nodes.append(n1)
        nodes.append(n2)
        edges.append((n1,n2,pol))
        edges.append((n2,n1,pol))

nodes = list(set(nodes))
print nodes
        
