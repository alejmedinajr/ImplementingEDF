import itertools
import random
import math

from Graph import Graph

def generateRandomDeadline(p, min, max):
    isRequest = random.random() <= p # for generating random deadlines, we only want p percent of deadlines (p is parameterized)
    if (isRequest): return random.randint(min, max) # want random deadline, random deadline value will be in range of (min, max)
    else: return 0 # no random deadline, return 0 to signify this is not a request

def createRandomGraphWithoutDeadlines(numberOfVertices, numberOfEdges, ID):
    i = 0
    g = Graph(numberOfVertices, ID)
    while i < (numberOfEdges):
        u = random.randint(1, numberOfVertices)
        v = random.randint(1, numberOfVertices)
        while u == v:
            v = random.randint(1, numberOfVertices)

        g.addEdgeWithDeadline(u, v, math.inf) # all edges will have infinite deadlines
        i += 1

    return g

def createRandomGraphWithDeadlines(numberOfVertices, numberOfEdges, ID, p, min, max):
    i = 0
    g = Graph(numberOfVertices, ID)
    while i < (numberOfEdges):
        u = random.randint(1, numberOfVertices)
        v = random.randint(1, numberOfVertices)
        while u == v:
            v = random.randint(1, numberOfVertices)

        g.addEdgeWithDeadline(u, v, generateRandomDeadline(p, min, max)) # all edges will have infinite deadlines
        i += 1

    return g

def generateRequestGraphsWithoutDeadlines(numberOfNodes):
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
    
    possibleRequestGraphs = []
    
    c = 0
    for i in range(numberOfNodes * 2):  # total number of edges
        for j in range(lengths[i]):
            graph = Graph(numberOfNodes, c)
            for k in range(i + 1):
                graph.addEdgeWithDeadline(possibleEdgePermutations[i][j][k][0], possibleEdgePermutations[i][j][k][1], math.inf)
            possibleRequestGraphs.append(graph)
            c += 1

    return possibleRequestGraphs


def generateRequestGraphsWithDeadlines(numberOfNodes, p, min, max, num):
    '''This method will create every possible directed graph with the given number of nodes'''

    locations = []
    lengths = []
    currentGraphsWithDeadlines = 0
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
    
    possibleRequestGraphs = []
    
    c = 0
    for i in range(numberOfNodes * 2):  # total number of edges
        for j in range(lengths[i]):
            graph = Graph(numberOfNodes, c)
            # we want the graph to have random deadlines
            if(random.random() >= 0.5 and currentGraphsWithDeadlines <= num):
                currentGraphsWithDeadlines +=1 # increase the number of graphs we have generated so far with deadlines
                for k in range(i + 1): # create the graph with random deadlines
                    graph.addEdgeWithDeadline(possibleEdgePermutations[i][j][k][0], possibleEdgePermutations[i][j][k][1], generateRandomDeadline(p, min, max))

            # either we created all of the number of graphs we want with deadlines or this is not a graph meant to have deadlines        
            else: 
                for k in range(i + 1): # create the graph with infite deadliens
                    graph.addEdgeWithDeadline(possibleEdgePermutations[i][j][k][0], possibleEdgePermutations[i][j][k][1], math.inf)
                    
            possibleRequestGraphs.append(graph) # add the newly created graph to our collection of graphs
            c += 1 # increase the id

    return possibleRequestGraphs

def generateGraphFromFile(graphInstanceFile):
    try:
        f = open(graphInstanceFile, 'r')
        # the first line of input will be our vertices parameter for the graph 
        g = Graph(int(f.readline().strip())) 
        finished = False
        while (not finished):
            line = f.readline()

            if not line:
                return g # we are done with the graph (no more input lines)
            
            else: 
                edgeInfo = line.split(' ')
                # 0 = starting vertex, 1 = ending vertex, 2 = deadline
                g.addEdgeWithDeadline(int(edgeInfo[0]), int(edgeInfo[1]), int(edgeInfo[2]))
        f.close() # done reading file, good practice to close it
        return g # return the newly generated graph
    
    except: # if there was a problem with the file, raise an exception
        raise Exception("Double check the file name you typed: " + graphInstanceFile)