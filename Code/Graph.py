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
    
    def visualizeGraph(self, timelimit , saveTo):
        """
        This function uses networkx and matplot to create an image vizualization of the directed graph
        :param saveTo: The file where the png graph will be saved to
        """
        G = nx.DiGraph() # create a nx directed graph for vizualization
        
        for edge in self.edges: # add each edge of the graph to the nx graph 
            # only add an edge if it has a deadline value that is not zero
            if (self.edges[edge][1] != 0 and self.edges[edge][1] != 1):
                G.add_edge(edge[0],edge[1], deadline=str(self.edges[edge][0]) + "/-/" + str(self.edges[edge][1]))

        # computes the layout using the Fruchterman-Reingold algorithm
        pos = nx.spring_layout(G, k = 50, seed = 5) # k is the distance between the nodes, seed 5 is being used to avoid getting different graph visuals for the same graph instance, maybe this seed value could be parameterized
        ax = plt.gca()
        ax.set_title("Timelimit = " + str(timelimit))
        # draw the graph
        nx.draw(G, pos=pos, node_color='#00b4d9', with_labels=True, width=2, arrowsize=15)
        deadlines = nx.get_edge_attributes(G,'deadline') # save the deadlines in a collection
        nx.draw_networkx_edge_labels(G,pos=pos,edge_labels=deadlines, label_pos=0.35, font_size=10, alpha =0.8) # include the deadlines on the graph
        #plt.title('my random fig')
        plt.savefig(saveTo + "Visual.png") # save the vizualization to a png file
        #plt.show() # show the graph
        plt.clf()

    def visualizeGraphSolution(self, timelimit, timesServed, requestsServed, method, saveTo):
        """
        This function uses networkx and matplot to create an image vizualization of the directed graph
        :param saveTo: The file where the png graph will be saved to
        """
        G = nx.DiGraph() # create a nx directed graph for vizualization
        #timesServed = list(filter(lambda a: a != 'x', timesServed))
        for edge in self.edges: # add each edge of the graph to the nx graph 
            # only add an edge if it has a deadline value that is not zero
            if (self.edges[edge][1] != 0 and self.edges[edge][1] != 1):
                if edge in requestsServed:
                    # request was served
                    serviceTime = timesServed[requestsServed.index(edge)]
                    G.add_edge(edge[0],edge[1], deadline=str(self.edges[edge][0]) + "/"+ str(serviceTime) + "/" + str(self.edges[edge][1]))
                else:
                    G.add_edge(edge[0],edge[1], deadline=str(self.edges[edge][0]) + "/-/" + str(self.edges[edge][1]))

        # computes the layout using the Fruchterman-Reingold algorithm
        pos = nx.spring_layout(G, k = 50, seed = 5) # k is the distance between the nodes, seed 5 is being used to avoid getting different graph visuals for the same graph instance, maybe this seed value could be parameterized
        ax = plt.gca()
        ax.set_title("Timelimit = " + str(timelimit))
        # draw the graph
        nx.draw(G, pos=pos, node_color='#00b4d9', with_labels=True, width=2, arrowsize=15)
        deadlines = nx.get_edge_attributes(G,'deadline') # save the deadlines in a collection
        if method == "OPT":
            nx.draw_networkx_edges(G, pos, edgelist=requestsServed, arrowsize = 15, width=2, edge_color='red') # opt solution in red
        else: 
            nx.draw_networkx_edges(G, pos, edgelist=requestsServed, arrowsize = 15, width=2, edge_color='yellow') # edf solution in yellow

        nx.draw_networkx_edge_labels(G,pos=pos, edge_labels=deadlines, label_pos=0.35, font_size=10, alpha=0.8) # include the deadlines on the graph
        
        plt.savefig(saveTo + "VisualSolution" + str(method) + ".png") # save the vizualization to a png file
        plt.clf()
        #plt.show() # show the graph


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
        if deadline > 1: #deadline 0 or 1 can never be served
            self.edges[u,v] = 0, deadline
        # print(self.graph)

    def addEdgeWithReleaseTimeAndDeadline(self, u, v, releaseTime, deadline):
        # function to add an edge to graph
        self.graph[u - 1].append(v - 1)
        if deadline > 1: # deadline 0 or 1 can never be served
            self.edges[u,v] = releaseTime, deadline
        # print(self.graph)

    def addEdge(self, u, v):
        # function to add an edge to graph
        self.graph[u - 1].append(v - 1)
        self.edges[u,v] = math.inf
        # print(self.graph)

    def containsEdge(self, u, v):
        return (u,v) in self.edges
        
    def getDeadline(self, u, v):
        #print(self.edges)     
        return self.edges[u,v][1] 
    
    def getReleaseTime(self, u, v):
        #print(self.edges)     
        return self.edges[u,v][0] 
    
    def deleteEdge(self, u, v):
        # function to delete an edge from graph
        self.graph[u-1].remove(v-1)

        # remove edge from edges as well
        del self.edges[u,v]

    def getNumberOfRequests(self):
        return len(self.edges)

    def getTimeLimit(self, timelimit):
        maxDeadline = -math.inf
        for edge in self.edges:
            if self.edges[edge][1] > maxDeadline:
                maxDeadline = self.edges[edge][1]

        return min(maxDeadline, timelimit)

    def copy(self):
        return self.graph.copy()

    