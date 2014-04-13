from py2neo import neo4j
from neo4jrestclient import client
from neo4jrestclient.client import GraphDatabase
#from neo4j import GraphDatabase
#from py2neo import neo4jrestclient
#from neo4jrestclient.client import GraphDatabase
db1 = GraphDatabase("http://localhost:7474/db/data/")
q = '''START customer=node(*) MATCH customer-[r]->m RETURN customer,r,m LIMIT 5'''
results = db1.query(q,returns=(client.Node, unicode, client.Relationship))		
print len(results)
for i in xrange(len(results)):
	for word in results[i]:
		word.
		print word.properties
                   