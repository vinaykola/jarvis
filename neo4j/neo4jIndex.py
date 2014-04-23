from py2neo import neo4j
import csv
uri = "http://localhost:7474/db/data/"
graph_db = neo4j.GraphDatabaseService(uri)
print graph_db.get_indexes(neo4j.Node)