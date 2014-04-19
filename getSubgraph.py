
from py2neo import neo4j
from neo4jrestclient import client
from neo4jrestclient.client import GraphDatabase
from collections import defaultdict
import json

def getSubgraph():
    op={"nodes":[],"links":[]}
    nodes=[]

    db1 = GraphDatabase("http://localhost:7474/")
    q1 = ' '.join(['MATCH n-[r]->m','WHERE n.name="batman"','RETURN n,r,m;'])
    q2 = ' '.join(['MATCH n-[r]->m WHERE n.name="batman"','WITH n,r,m MATCH q-[r2]->p','WHERE n-[r]->q AND n-[r]->p','RETURN q,r2,p limit 200;'])
    print "starting"
    results1=db1.query(q1,returns=(client.Node, client.Relationship, client.Node))
    print "HERE"
    for result in results1:
        n1=result[0].properties['name']
        n2=result[2].properties['name']
        try:
            i1=nodes.index(n1)
        except:
            nodes.append(n1)
            i1=nodes.index(n1)
            op["nodes"].append({"name":n1})
        try:
            i2=nodes.index(n2)
        except:
            nodes.append(n2)
            i2=nodes.index(n2)
            op["nodes"].append({"name":n2})
        
        r = result[1].type
        op["links"].append({"source":i1,"target":i2,"type":r})
        
    print op


    results2 = db1.query(q2,returns=(client.Node, client.Relationship, client.Node))
    print "THERE!"
    for result in results2:
        n1=result[0].properties['name']
        n2=result[2].properties['name']
        #try:
        i1=nodes.index(n1)
        """
        except:
            nodes.append(n1)
            i1=nodes.index(n1)
            op["nodes"].append({"name":n1})
        """    
        #try:
        i2=nodes.index(n2)
        """
        except:
            nodes.append(n2)
            i2=nodes.index(n2)
            op["nodes"].append({"name":n2})
        """
        r = result[1].type
        op["links"].append({"source":i1,"target":i2,"type":r})
        
    print op
    json.dump(op,open('subgraph.json','w'))

def getAllNodesOfDepth(name,num):
    op={"nodes":[],"links":[]}
    nodes=[]

    db1 = GraphDatabase("http://localhost:7474/db/data/")
    q = '''MATCH (n { name: \''''+name+'''\'})-[*'''+str(num)+''']->m RETURN n,r,m'''
    results = db1.query(q,returns=(client.Node, client.Relationship, client.Node))#, unicode, client.Relationship))

    for result in results:
        n1=result[0].properties['name']
        n2=result[2].properties['name']
        try:
            i1=nodes.index(n1)
        except:
            nodes.append(n1)
            i1=nodes.index(n1)
            op["nodes"].append({"name":n1})
        try:
            i2=nodes.index(n2)
        except:
            nodes.append(n2)
            i2=nodes.index(n2)
            op["nodes"].append({"name":n2})
        
        r = result[1].type
        op["links"].append({"source":i1,"target":i2,"type":r})
    json.dump(op,open('subgraph.json','w'))
    return op
    """
    endnode = []
    for i in xrange(len(results)):
        for word in results[i]:
            endnode.append(str(word.properties['name']))

    for i in xrange(len(endnode)):
        print endnode[i]
    return endnode
    """

#getSubgraph()
getAllNodesOfDepth("batman",2)