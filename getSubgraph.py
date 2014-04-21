
from py2neo import neo4j
from neo4jrestclient import client
from neo4jrestclient.client import GraphDatabase
from collections import defaultdict
import json
import pickle
import ast

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

def getRelType(unicodeString):
    temp = defaultdict()
    for word1 in unicodeString.split(","):
        if word1.startswith(' u\'type'):
            return word1.split(":")[1].split("\'")[1]
"""
def getAllNodesOfDepth(name,num):

    op={"nodes":[],"links":[]}
    db1 = GraphDatabase("http://localhost:7474/db/data/")
    q = '''MATCH p = (n { name: \''''+name+'''\'})-[r*'''+str(num)+''']->m RETURN p,r'''
    #results = db1.query(q,returns=(unicode,unicode))
    results=pickle.load(open('depth2results.pkl'))
    graph = []
    startnode = []
    endnode = []
    midnode = []
    rel = []
    print "got results"

    with open('depth1results.pkl','w') as fil:
        pickle.dump(results,fil)

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
    nodes=list(set(startnode+midnode+endnode))

    print "Pickling stuff..."
    with open('pklfiles/data.pkl','w') as pklf:
        pickle.dump(nodes,pklf)
        pickle.dump(startnode,pklf)
        pickle.dump(midnode,pklf)
        pickle.dump(endnode,pklf)
        pickle.dump(rel,pklf)

    print "Writing nodes to json..."
    for node in nodes:
        op["nodes"].append({"name":node})

    print "Total Nodes:", len(nodes)

    for i in xrange(len(startnode)):
        op["links"].append({"source":nodes.index(startnode[i]),"target":nodes.index(midnode[i]),"type":rel[i][0]})
        op["links"].append({"source":nodes.index(midnode[i]),"target":nodes.index(endnode[i]),"type":rel[i][1]})
        if i==10000:
            break
        #print op["links"][-1]
        #graph.append([startnode[i],rel[i][0],midnode[i],rel[i][1],endnode[i]])
    #for word in graph:
        #print word
    print "Total Edges:", len(op["links"])

    json.dump(op,open('jsonfiles/subgraphDepth1.json','w'))

"""

def process_nodes_edges():
    op={"nodes":[],"links":[]}
    with open('pklfiles/nodes_edges.pkl') as f:
        nodes=pickle.load(f)
        edges=list(pickle.load(f))
    friend_nodes=[]
    #for node in nodes:
        #op["nodes"].append({"name":node})
    op["nodes"].append({"name":nodes[3963]})
    friend_nodes.append(nodes[3963])
    print op["nodes"][-1]
    c=0
    for n1,n2,r in edges:
        if n1==3963 or n2==3963:
            if r=="FRIEND":
                if n1==3963:
                    friend_nodes.append(nodes[n2])
                    op["nodes"].append({"name":nodes[n2]})
                else:
                    op["nodes"].append({"name":nodes[n1]})
                    friend_nodes.append(nodes[n1])

                op["links"].append({"source":friend_nodes.index(nodes[n1]),"target":friend_nodes.index(nodes[n2]),"type":r})
                c+=1
    print c
    for n1,n2,r in edges:
        if nodes[n1] in friend_nodes and nodes[n2] in friend_nodes:
            """
            if r=="FRIEND":
                if n1==3963:
                    friend_nodes.append(nodes[n2])
                    op["nodes"].append({"name":nodes[n2]})
                else:
                    op["nodes"].append({"name":nodes[n1]})
                    friend_nodes.append(nodes[n1])
            """
            op["links"].append({"source":friend_nodes.index(nodes[n1]),"target":friend_nodes.index(nodes[n2]),"type":r})
            c+=1
            if c>1000:
                break
    print c
    json.dump(op,open('jsonfiles/sgd1-batman-friends-sg.json','w'))


def process_pickles():
    op={"nodes":[],"links":[]}

    results=pickle.load(open('depth2results.pkl'))    
    
    with open('pklfiles/data.pkl') as pklf:
        nodes=pickle.load(pklf)
        startnode=pickle.load(pklf)
        midnode=pickle.load(pklf)
        endnode=pickle.load(pklf)
        rel=pickle.load(pklf)
    print "Read stuff..."

    for node in nodes:
        op["nodes"].append({"name":node})
    edges=[]
    print "Total Nodes:", len(nodes)

    for i in xrange(len(startnode)):
        #op["links"].append({"source":nodes.index(startnode[i]),"target":nodes.index(midnode[i]),"type":rel[i][0]})
        #op["links"].append({"source":nodes.index(midnode[i]),"target":nodes.index(endnode[i]),"type":rel[i][1]})
        edges.append((nodes.index(startnode[i]),nodes.index(midnode[i]),rel[i][0]))
        edges.append((nodes.index(midnode[i]),nodes.index(endnode[i]),rel[i][1]))
        #print op["links"][-1]
        #graph.append([startnode[i],rel[i][0],midnode[i],rel[i][1],endnode[i]])
    #for word in graph:
        #print word
    print "Total Edges:", len(edges),len(set(edges))

    with open('pklfiles/nodes_edges.pkl','w') as nef:
        pickle.dump(nodes,nef)
        pickle.dump(set(edges),nef)
    return
    #json.dump(op,open('jsonfiles/subgraphDepth1.json','w'))






    print "i should not be here!"




    snodes=nodes[:500]
    if "batman" not in snodes:
        snodes.append("batman")
    for node in snodes:
        op["nodes"].append({"name":node})
    c=0
    edges=set()

    batman_id=snodes.index("batman")
    for i in xrange(len(startnode)):
        if (midnode[i] in snodes):
            start_idx=snodes.index(startnode[i])
            mid_idx=snodes.index(midnode[i])
            #print startnode[i],midnode[i],rel[i][0],start_idx,mid_idx
            if frozenset((start_idx,mid_idx)) not in edges and batman_id==start_idx:
                op["links"].append({"source":start_idx,"target":mid_idx,"type":rel[i][0]})
                edges.add(frozenset((start_idx,mid_idx)))
                print op["links"][-1],len(edges)
                raw_input('')


    for i in xrange(len(startnode)):
        if (startnode[i] in snodes) and (midnode[i] in snodes):
            start_idx=snodes.index(startnode[i])
            mid_idx=snodes.index(midnode[i])
            #print startnode[i],midnode[i],rel[i][0],start_idx,mid_idx
            if frozenset((start_idx,mid_idx)) not in edges:
                op["links"].append({"source":start_idx,"target":mid_idx,"type":rel[i][0]})
                edges.add(frozenset((start_idx,mid_idx)))
                print op["links"][-1],len(edges)
                raw_input('')
        if (endnode[i] in snodes) and (midnode[i] in snodes):
            mid_idx=snodes.index(midnode[i])
            end_idx=snodes.index(endnode[i])
            #print midnode[i],endnode[i],rel[i][1],mid_idx,end_idx
            if frozenset((mid_idx,end_idx)) not in edges:
                op["links"].append({"source":mid_idx,"target":end_idx,"type":rel[i][1]})
                edges.add(frozenset((mid_idx,end_idx)))
                print op["links"][-1],len(edges)
                raw_input('')


        if len(edges)>1000:
            print len(edges)
            break
        #print op["links"][-1]
        #graph.append([startnode[i],rel[i][0],midnode[i],rel[i][1],endnode[i]])
    #for word in graph:
        #print word
    print "Total Edges:", len(op["links"])
    json.dump(op,open('jsonfiles/sgd2-1k-better.json','w'))


process_nodes_edges()
#getSubgraph()
#getAllNodesOfDepth("batman",2)
#process_pickles()