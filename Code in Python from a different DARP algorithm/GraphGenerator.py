import itertools
import random

from Graph import Graph

def createRandomGraph(numberOfVertices, numberOfEdges, ID):
    i = 0
    g = Graph(numberOfVertices, ID)
    while i < (numberOfEdges):
        u = random.randint(1, numberOfVertices)
        v = random.randint(1, numberOfVertices)
        while u == v:
            v = random.randint(1, numberOfVertices)

        g.addEdge(u, v)
        i += 1

    # for i in range(numberOfVertices):
    #     if not g.hasVertex(i):
    #         g.addVertex(i)
    return g

def generateRequestGraphs(numberOfNodes):
    '''This method will create every possible directed graph with the given number of nodes'''

    locations = []
    lengths = []
    # first just get a list of numbers for the locations
    for i in range(numberOfNodes):
        locations.append(i + 1)
    # find all the permutations of 2 of these locations to get all the possible edges
    possibleRequests = list(itertools.permutations(locations, 2))
    possibleEdgePermutations = []
    # find all the permutations/combinations of all of these edges to get the possible graphs.
    for i in range(2 * numberOfNodes):
        possibleEdgePermutations.append(list(itertools.combinations(possibleRequests, i + 1)))
        lengths.append(len(list(itertools.combinations(possibleRequests, i + 1))))
    # turn this list of tuples into graph objects
    # print(possibleEdgePermutations)
    # a= factorial(numberOfNodes)/ factorial(numberOfNodes-2)
    # #print(a)
    # b=0
    # for i in range(numberOfNodes):
    #     c=a-(i+1)
    #     b+= factorial(a)/(factorial(i+1)*factorial(a-(i+1)))
    # print(lengths)
    possibleRequestGraphs = []
    # for j in range(int(b)):
    #    possibleRequestGraphs.append(Graph(numberOfNodes,j))
    # print(possibleRequestGraphs)
    # print(possibleEdgePermutations)
    c = 0
    for i in range(numberOfNodes * 2):  # total number of edges
        for j in range(lengths[i]):
            graph = Graph(numberOfNodes, c)
            # for k in range(int(b)):
            # print(possibleRequestGraphs[k])
            #######################################################################################################################################
            # print("outside loop: \n",possibleRequestGraphs[j])
            for k in range(i + 1):
                # print("Start vertex index ",i," ",j, " ", k," ", 0, ". Start vertex: ",possibleEdgePermutations[i][j][k][0])
                # print("destination index ",i," ",j, " ", k," ", 1, ". Destination vertex : ",possibleEdgePermutations[i][j][k][1])
                # print("Graph we are adding this edge to: \n ", possibleRequestGraphs[j])
                # print("Make sure the index of the request graph we add the edge to is correct j,k values: ",j,",",k)
                # print("Graph before adding the edge: \n ", possibleRequestGraphs[j+1])
                graph.addEdge(possibleEdgePermutations[i][j][k][0], possibleEdgePermutations[i][j][k][1])
            possibleRequestGraphs.append(graph)
            c += 1
            # print("Graph after adding the edge: \n ", possibleRequestGraphs[j+1])

            # print("possibleRequestGraph: ",j, "\n",possibleRequestGraphs[i])

    return possibleRequestGraphs