# Class to represent a graph
import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


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
        :prints a visualization of the graph
        """
        s = ""
        #for i in range(self.edges):
        #    s += str(i) + ":" + str(self.graph[i]) + "\n"
        #return "graph id: " + str(self.id) + "\n" + str(self.edges)
    
    def visualizeGraph(self, saveTo):
        """
        This function uses networkx and matplot to create an image vizualization of the directed graph
        :param saveTo: The file where the png graph will be saved to
        """
        G = nx.DiGraph() # create a nx directed graph for vizualization
        for i in self.edges: # add each edge of the graph to the nx graph 
            # only add an edge if it has a deadline value that is not zero
            if (self.edges[i] != 0):
                G.add_edge(i[0],i[1], deadline=self.edges[i])

        # computes the layout using the Fruchterman-Reingold algorithm
        pos = nx.spring_layout(G)

        # draw the graph
        nx.draw(G, pos=pos, with_labels=True)
        deadlines = nx.get_edge_attributes(G,'deadline') # save the deadlines in a collection
        nx.draw_networkx_edge_labels(G,pos,edge_labels=deadlines) # include the deadlines on the graph
        plt.savefig(saveTo) # save the vizualization to a png file
        plt.show() # show the graph
        
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

    