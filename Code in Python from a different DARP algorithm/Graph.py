# Class to represent a graph
class Graph:
    def __init__(self, numVertices, j):
        # self.graph = defaultdict(list) #dictionary containing adjacency List
        self.graph = {}
        for i in range(numVertices):
            self.graph[i] = []
        self.V = numVertices  # No. of vertices
        self.id = j

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

    def addEdge(self, u, v):
        # function to add an edge to graph

        self.graph[u - 1].append(v - 1)
        # print(self.graph)

    def deleteEdge(self, u, v):
        # function to delete an edge from graph
        self.graph[u].remove(v)

    def copy(self):
        return self.graph.copy()

    def isCyclicUtil(self, v, visited, recStack):
        """
        Mark the given vertex as visited and add to the recursion stack
        :param v: Vertex in this graph
        :param visited: List of visited vertices
        :param recStack: Recursion Stack
        :return:
        """
        visited[v] = True
        recStack[v] = True

        # Recur for all neighbors
        # if any neighbor is visited and in recStack then graph is cyclic
        for neighbor in self.graph[v]:
            if visited[neighbor] == False:
                if self.isCyclicUtil(neighbor, visited, recStack) == True:
                    return True
            elif recStack[neighbor] == True:
                return True

        # The node needs to be popped from
        # recursion stack before function ends
        recStack[v] = False
        return False

    def isCyclic(self):
        """
        :return: TRUE if the graph is cyclic
        """
        visited = [False] * self.V
        recStack = [False] * self.V
        for node in range(self.V):
            if visited[node] == False:
                if self.isCyclicUtil(node, visited, recStack) == True:
                    return True
        return False

    # A recursive function used by topologicalSort
    def topologicalSortUtil(self, v, visited, stack):

        # Mark the current node as visited.
        visited[v] = True

        # FOR all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if visited[i] == False:
                self.topologicalSortUtil(i, visited, stack)

        # Push current vertex to stack which stores result
        stack.insert(0, v)

    def topologicalSort(self):
        """
        Topologically sorts the graph.  Only works properly for a directed acyclic graph.
        If the graph is not acyclic
        then the sorting is somewhat arbitrary.
        Uses the recursive topologicalSortUtil()
        :return: Array of vertices in order
        """
        # Mark all the vertices as not visited
        visited = [False] * self.V
        stack = []

        # Sort starting from all vertices one by one
        for i in range(self.V):
            if visited[i] == False:
                # Call the recursive helper function
                self.topologicalSortUtil(i, visited, stack)

        # Return contents of the stack (vertices in topological order)
        return stack

    def findLongestPath(self):
        """
        Description of this function can be found googling "longest path in a directed acyclic graph"
        :return: List of the vertices of the longest Path in this graph (in the order they are traversed)
        """
        # this function only works for a directed acyclic graph
        sortedGraph = self.topologicalSort()

        maxPath = []
        # for every node in the graph find the longest path to all other nodes
        for k in range(self.V):
            distance = [-99999999 for j in range(self.V)]  # initialize distances to all nodes to be large negative
            longestPath = [[] for j in range(self.V)]
            distance[k] = 0  # initialize distance of start node to 0
            longestPath[k] = [k]

            for i in range(self.V):
                v = sortedGraph[i]  # sortedGraph[i] is the ith vertex in the topological ordering
                for j in self.graph[v]:
                    # print("Adjacent vertex", j)
                    if v == j:
                        pass
                    else:
                        # if (distance[j]==distance[v]+1): #This is the tiebreaking rule to create randomness in the way ties are broken
                        #     r = randint(0,1)
                        #     if (r == 0): #50/50 chance to keep the path that leads to j or switch it out
                        #         longestPath[j] = list(longestPath[v])
                        #         longestPath[j].append(j)
                        # print("dist",j,"=",distance[j], " and dist",v,"=",distance[v])
                        if (distance[j] < distance[v] + 1):
                            distance[j] = distance[v] + 1
                            # print(longestPath,i,j)
                            # print("before j: ",longestPath[j])
                            # print("before v: ",longestPath[v])
                            longestPath[j] = list(longestPath[v])
                            longestPath[j].append(j)
                            # print("longest path j: ",longestPath[j])
                            # print("longest path v: ",longestPath[v])
                        # if (len(maxPath)==distance[j]):#This is the tiebreaking rule to create randomness in the way ties are broken
                        #     print("length max path: ", len(maxPath))
                        #     print("dist[j]", distance[j])
                        #     r = randint(0,1)
                        #     if (r == 0): #50/50 chance to keep the max path or switch it out
                        #         maxPath = list(longestPath[j])
                        #         print("max path swapped", maxPath)
                        if (len(maxPath) - 1 < distance[j]):
                            #  print(longestPath[j])
                            # print(j,longestPath)
                            # print("before: ",maxPath)
                            maxPath = list(longestPath[j])
                # print("MAX PATH: ", maxPath)
        return maxPath
