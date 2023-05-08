# Class to represent a graph
import math

class Graph:
    def __init__(self, *args):
        # self.graph = defaultdict(list) #dictionary containing adjacency List
        self.graph = {}
        for i in range(args[0]):
            self.graph[i] = []
        self.V = args[0]  # No. of vertices
        self.edges = {} # for the edges (added 04/21)

        if len(args) > 1:
            self.id = args[1] # we were given an ID parameter

    def __str__(self):
        """
        :return: the contents of the graph and id number
        """
        s = ""
        for i in range(self.V):
            s += str(i) + ":" + str(self.graph[i]) + "\n"
        return "graph id: " + str(self.id) + "\n" + s

    def getNumberVerticies(self):
        return self.V

    def hasAdjacentVertex(self, v):
        """
        :param v: Vertex in this graph
        :return: TRUE if the vertex is a source of a request
        """
        if (v == -1):
            return False
        else:
            return len(self.graph[v]) != 0

    def getAdjacentVertex(self, v):
        """
        :param v: Vertex in this graph
        :return: A vertex u where there is an edge from v to u
        """
        return self.graph[v][0]

    def addVertex(self, v):
        self.graph[v] = []

    def addEdgeWithDeadline(self, u, v, deadline):
        # function to add an edge to graph
        self.graph[u - 1].append(v - 1)
        self.edges[u,v] = deadline
        # print(self.graph)

    def addEdge(self, u, v):
        # function to add an edge to graph
        self.graph[u - 1].append(v - 1)
        self.edges[u,v] = math.inf
        # print(self.graph)

    def getDeadline(self, u, v):     
        return self.edges[u,v] 
    
    def deleteEdge(self, u, v):
        # function to delete an edge from graph
        self.graph[u].remove(v)

        # remove edge from edges as well
        del self.edges[u,v]
        
    def copy(self):
        return self.graph.copy()

    