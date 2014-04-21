'''
Updated api to retrieve data from the neo4j GraphDatabase
'''

from py2neo import neo4j
from neo4jrestclient import client
from neo4jrestclient.client import GraphDatabase
from collections import defaultdict
import json
import ast

#Utility method - Not to be used in the api
def getRelType(unicodeString):
	temp = defaultdict()
	for word1 in unicodeString.split(","):
		if word1.startswith(' u\'type'):
			return word1.split(":")[1].split("\'")[1]


#Returns all nodes and all their relations in the graph in neo4j
#Parameter - none
#Return - dictionary - (startnode,endnode) - relationship type
def getAllNodesAndRelations():
	db1 = GraphDatabase("http://localhost:7474/db/data/")
	q = '''START n=node(*) MATCH n-[r]->m RETURN n,r,m'''
	results = db1.query(q,returns=(client.Node, unicode, client.Relationship))
	print len(results)
	graph = defaultdict()
	startnode = []
	endnode = []
	rel = []
	for i in xrange(len(results)):
		for word in results[i]:
			if word.__class__.__name__ == 'unicode':
				json1_str = str(word)
				rel.append(getRelType(json1_str))
			if word.__class__.__name__ == 'Node':
				startnode.append(str(word.properties['name']))
			if word.__class__.__name__ == 'Relationship':
				endnode.append(str(word.properties['name']))

	for i in xrange(len(startnode)):
		graph[(startnode[i],endnode[i])] = rel[i]

	for word in graph:
		print word,graph[word]

	return graph

#Returns all nodes present in the neo4j graph
#Parameter - none
#Returns  - list of all the nodes
def getAllNodes():
	db1 = GraphDatabase("http://localhost:7474/db/data/")
	q = '''START n=node(*) RETURN n LIMIT 5'''
	results = db1.query(q,returns=client.Node)
	nodes = []
	print len(results)
	for i in xrange(len(results)):
		for word in results[i]:
			nodes.append(str(word.properties['name']))
	return nodes

#Returns all friends of a particular comic character
#Parameter - name of the character
#Returns - all the friends as a list
def getFriends(name):
	db1 = GraphDatabase("http://localhost:7474/db/data/")
	q = '''MATCH (n { name: \''''+name+'''\'})-[r]->m WHERE type(r) = 'FRIEND' RETURN n,r,m'''
	results = db1.query(q,returns=(client.Node, unicode, client.Relationship))
	endnode = []
	for i in xrange(len(results)):
		for word in results[i]:
			if word.__class__.__name__ == 'Relationship':
				endnode.append(str(word.properties['name']))

	print endnode
	return endnode

#Returns all foes of a particular comic character
#Parameter - name of the character
#Returns - all the foes as a list
def getFoes(name):
	db1 = GraphDatabase("http://localhost:7474/db/data/")
	q = '''MATCH (n { name: \''''+name+'''\'})-[r]->m WHERE type(r) = 'FOE' RETURN n,r,m'''
	results = db1.query(q,returns=(client.Node, unicode, client.Relationship))
	endnode = []
	for i in xrange(len(results)):
		for word in results[i]:
			if word.__class__.__name__ == 'Relationship':
				endnode.append(str(word.properties['name']))

	print endnode
	return endnode

#Returns all nodes connected by a particular relationship type
#Parameter - type of the relationship (friend or foe - case insensitive)
#Returns - list of tuples of nodes connected by that relationship type
def getAllRelationshipsOfType(type):
	db1 = GraphDatabase("http://localhost:7474/db/data/")
	q = '''START n=node(*) MATCH n-[r]->m WHERE type(r) = \''''+type.upper()+'''\'RETURN n,r,m'''
	results = db1.query(q,returns=(client.Node, unicode, client.Relationship))
	print len(results)
	nodes = []
	startnode = []
	endnode = []
	for i in xrange(len(results)):
		for word in results[i]:
			if word.__class__.__name__ == 'Node':
				startnode.append(str(word.properties['name']))
			if word.__class__.__name__ == 'Relationship':
				endnode.append(str(word.properties['name']))

	for i in xrange(len(startnode)):
		nodes.append((startnode[i],endnode[i]))

	for i in xrange(len(nodes)):
		print nodes[i]
	return nodes

#Returns relationship of a pair of characters
#Parameter - names of each character
#Returns - type of the relationship as a string.
def getRelationship(name1,name2):
	db1 = GraphDatabase("http://localhost:7474/db/data/")
	q = '''MATCH (n { name: \''''+name1+'''\'})-[r]->(m { name: \''''+name2+'''\'}) RETURN n,r,m'''
	results = db1.query(q,returns=(client.Node, unicode, client.Relationship))
	rel = []
	for i in xrange(len(results)):
		for word in results[i]:
			if word.__class__.__name__ == 'unicode':
				json1_str = str(word)
				rel.append(getRelType(json1_str))
				break

	if(len(rel)>=1):
		print rel[0]
		return rel[0]
	return 0

#Returns all nodes connected to a particular node upto a certain depth
#Parameter - name of the character, depth of the relationship
#Returns - all the characters connected to that character at that depth as a list.
def getAllNodesOfDepth(name,num):
	db1 = GraphDatabase("http://localhost:7474/db/data/")
	q = '''MATCH p = (n { name: \''''+name+'''\'})-[r*'''+str(num)+''']->m RETURN p,r'''
	results = db1.query(q,returns=(unicode,unicode))
	graph = []
	endnode = []
	startnode = []
        endnode = []
	midnode = []
	rel = []
	for i in xrange(len(results)):
		for word in results[i]:
			if word.__class__.__name__ == 'unicode':
				json1_str = str(word)
				if json1_str.startswith('['):                    #get relationships
					a = getRelType(json1_str)
					b = getRelType(json1_str.split("}, {")[1])
					rel.append((a,b))
				else:                                           #get nodes
					json1_str = json1_str.replace('u','')
					dictstr = ast.literal_eval(json1_str)
					for word2 in dictstr:
						if word2 == 'start':
							startn = client.Node(dictstr[word2])
							startnode.append(str(startn.properties['name']))
						if word2 == 'end':
							endn = client.Node(dictstr[word2])
							endnode.append(str(endn.properties['name']))
						if word2 == 'nodes':
							midn = client.Node(dictstr[word2][1])
							midnode.append(str(midn.properties['name']))
	for i in xrange(len(startnode)):
		graph.append([startnode[i],rel[i][0],midnode[i],rel[i][1],endnode[i]])
	for word in graph:
		print word
	return graph

def updateRelationshipType(name,propertytochange,newvalue):
	db1 = GraphDatabase("http://localhost:7474/db/data/")
	q = '''MATCH (n {name: \''''+name+'''\'}) SET n.'''+propertytochange+''' = \''''+newvalue+'''\' RETURN n'''
	results = db1.query(q)

#Usage
'''
getFriends('superman')
getFoes('superman')
getAllRelationshipsOfType('friend')
getRelationship('superman','wonder woman')
'''
getAllNodesOfDepth('superman',2)
