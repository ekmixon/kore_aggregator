import py2neo
import socket


def initiate_refresh(refresh, conf):
    if not refresh:
        print "[!] Wiping Database"
        return

    try:
        setup(conf).delete_all()
    except socket.error:
        setup(conf).delete_all()


def setup(configuration):
    neo4j = configuration.neo4j
    graph = py2neo.Graph(bolt=True, host=neo4j.server, user=neo4j.user, password=neo4j.password)

    try:
        graph.data("MATCH (a) RETURN a LIMIT 1")
    except py2neo.database.status.Unauthorized:
        print "[!] Failed to connection to {} using '{}' : '{}'".format(neo4j.server, neo4j.user, neo4j.password)
        return None
    else:
        print "[*] Connected, returning graph object"
        graph.conf = configuration
        return graph

