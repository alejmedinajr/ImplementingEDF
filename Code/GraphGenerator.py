import itertools
import random
import math

from Graph import Graph

def generateRandomEdgeAttributes(p, min, max):
    '''
    This function generates a random deadline in the range [min, max] if a randomly generated value is less than or equal to the p parameter value
    :param p: The threshold value used to have a p percent of requests in a graph
    :param min: The minimum value of a possible deadline
    :param max: The maximum value of a possible deadline
    :return: A randomly generated deadline if the random value does not exceed p, otherwise returns 0
    '''
    isRequest = random.random() <= p # for generating random deadlines, we only want p percent of deadlines (p is parameterized)
    if (isRequest):
        # first randomly generate the release time
        release = random.randint(0, max/2) # to ensure that the release time does not equal the deadline otherwise the request will never be able to be served 
        deadline = random.randint(release+1, max)
        return release, deadline # return the release and deadline of the request
    else: return 0,0 # no random deadline, return 0 to signify this is not a request

def createRandomGraphWithoutDeadlines(numberOfNodes, numberOfEdges, id):
    '''
    This function generates a single random graph with a given number of nodes and edges. Each edge is assigned an infinite deadline.
    :param numberOfNodes: The number of nodes the randomly generated graph will have
    :param numberOfEdges: The number of edges the randomly generated graph will have
    :param id: The id that the newly generated graph will have
    :return: A randomly generated graph with a specified number of nodes and edges
    '''
    e = 0 # counter for number of edges
    graph = Graph(numberOfNodes, id) # new graph object that will be returned
    while e < (numberOfEdges): # only want to add the specified edges
        u = random.randint(1, numberOfNodes) # randomly select starting vertex
        v = random.randint(1, numberOfNodes) # randomly select ending vertex
        while u == v: # if u and v are the same vertex, we need to keep randomly selecting a random vertex until we get a unique ending vertex
            v = random.randint(1, numberOfNodes)

        graph.addEdgeWithDeadline(u, v, math.inf) # all edges will have infinite deadlines
        e += 1 # increase the counter for number of edges since we added a new edge

    return graph # return the randomly generated graph

def createRandomGraphWithDeadlines(numberOfNodes, numberOfEdges, id, f, p, min, max):
    '''
    This function generates a single random graph with a given number of nodes and edges. Each edge is may be assigned a deadline with a value [min, max].
    :param numberOfNodes: The number of nodes the randomly generated graph will have
    :param numberOfEdges: The number of edges the randomly generated graph will have
    :param id: The id that the newly generated graph will have
    :param f: The frequency of bidirectional edges. If f = 0, no bidirectional edges will be allowed, otherwise the value of f represents the frequency of bidirectional edges.
    :param p: The percent of edges that will have deadlines (we only want a p percent of edges to be requests)
    :param min: The minimum value that a deadline could be
    :param max: The maximum value that a deadline could be
    :return: A randomly generated graph with a specified number of nodes and edges
    '''
    e = 0 # counter for number of edges
    graph = Graph(numberOfNodes, id) # new graph object that will be returned
    while e < (numberOfEdges): # only want to add the specified edges
        u = random.randint(1, numberOfNodes) # randomly select starting vertex
        v = random.randint(1, numberOfNodes) # randomly select ending vertex
        while u == v: # if u and v are the same vertex, we need to keep randomly selecting a random vertex until we get a unique ending vertex
            v = random.randint(1, numberOfNodes)

        if ((f == 0) and (not graph.containsEdge(v, u))) or ((f > 0) and (f >= random.random())): # conditions to add an edge depending on value of f.
            edgeAttributes = generateRandomEdgeAttributes(p, min, max)
            graph.addEdgeWithReleaseTimeAndDeadline(u, v, edgeAttributes[0], edgeAttributes[1]) # randomly generate release time and deadline
            if (graph.getDeadline(u,v) == 0): # if the edge is not a request, then we want to remove it from the graph and list of edges, but we do not want to undo the increment to the edge counter
                graph.deleteEdge(u,v) # delete the edge from the graph since it is not a request
            e += 1 # increase the counter for number of edges since we added a new edge

    return graph # return the randomly generated graph

def generateRequestGraphsWithoutDeadlines(numberOfNodes):
    '''
    This function generates all possible directed graphs with a given number of nodes. All possible permutations of edges are considered, and each edge is assigned an infinite deadline.
    :param numberOfNodes: The number of nodes each graph will have
    :return: A collection of all the possible graphs with n vertices where n is the numberOfNodes
    '''
    locations = [] # a collection of possible locations of nodes in a graph
    lengths = [] # a collection of all of the lengths between any two vertices in a graph

    for i in range(numberOfNodes): # find possible locations of nodes in the graph
        locations.append(i + 1)
    
    possibleRequests = list(itertools.permutations(locations, 2)) # find all the permutations of 2 of these locations to get all the possible edges
    possibleEdgePermutations = [] # collection to store every combination of edges in the graph
    for i in range(2 * numberOfNodes): # find all the permutations/combinations of all of these edges to get the possible graphs.
        possibleEdgePermutations.append(list(itertools.combinations(possibleRequests, i + 1)))
        lengths.append(len(list(itertools.combinations(possibleRequests, i + 1))))
    
    possibleRequestGraphs = [] # collection of graphs that will be returned
    
    id = 0
    for i in range(numberOfNodes * 2):  # total number of edges
        for j in range(lengths[i]):
            graph = Graph(numberOfNodes, id) # new graph
            for k in range(i + 1):
                graph.addEdgeWithDeadline(possibleEdgePermutations[i][j][k][0], possibleEdgePermutations[i][j][k][1], math.inf) # add an edge with an infinite deadline (representing no deadline)
            possibleRequestGraphs.append(graph) # add the newly created graph to our collection of graphs
            id += 1 # incrementing the graph ID for the next graph

    return possibleRequestGraphs # return the list of generated graphs


def generateRequestGraphsWithDeadlines(numberOfNodes, p, min, max, copies):
    '''
    This function generates all possible directed graphs with a given number of nodes. All possible permutations of edges are considered, and each edge is assigned a random deadline.
    :param numberOfNodes: The number of nodes each graph will have
    :param p: Percent of edges we want to have deadlines (not every edge should be a request)
    :param min: The minimum value that will be used for randomly generating a request's deadline
    :param max: The maximum value that will be used for randomly genrating a request's deadline
    :param copies: The number of copies of each graph that is desired (this allows the same graph to have different random deadlines)
    :return: A collection of all the possible graphs with n vertices where n is the numberOfNodes
    '''
    locations = [] # a collection of possible locations of nodes in a graph
    lengths = [] # a collection of all of the lengths between any two vertices in a graph
    
    for i in range(numberOfNodes): # find possible locations of nodes in the graph
        locations.append(i + 1)

    possibleRequests = list(itertools.permutations(locations, 2)) # find all the permutations of 2 of these locations to get all the possible edges
    possibleEdgePermutations = [] # collection to store every combination of edges in the graph
    for i in range(2 * numberOfNodes): # find all the permutations/combinations of all of these edges to get the possible graphs.
        possibleEdgePermutations.append(list(itertools.combinations(possibleRequests, i + 1)))
        lengths.append(len(list(itertools.combinations(possibleRequests, i + 1))))
    
    possibleRequestGraphs = [] # collection of graphs that will be returned
    
    id = 0
    for i in range(numberOfNodes * 2):  # total number of edges
        for j in range(lengths[i]):
            for n in range(copies): # we want to make a parameterized amount of copies for each graph created 
                graph = Graph(numberOfNodes, id) # new graph
                for k in range(i + 1):
                    edgeAttributes = generateRandomEdgeAttributes(p, min, max)
                    graph.addEdgeWithReleaseTimeAndDeadline(possibleEdgePermutations[i][j][k][0], possibleEdgePermutations[i][j][k][1], edgeAttributes[0], edgeAttributes[1]) # add randomly generated release time and deadline
                possibleRequestGraphs.append(graph) # add the newly created graph to our collection of graphs
                id += 1 # incrementing the graph ID for the next graph
            n += 1 # increment the variable to reflect we created +1 copy of the current graph

    return possibleRequestGraphs # return the list of generated graphs

def generateGraphFromFile(graphInstanceFile):
    '''
    This function reads a file to generate a graph. The first line of the file specifies the number of vertices, and each subsequent line specifies an edge and its associated deadline.
    :param graphInstanceFile: Specific file instance of graph to generate
    :return: Graph representation based on the graph instance file
    '''

    try:
        print(graphInstanceFile)
        f = open(graphInstanceFile.strip(), 'r')
        timeLimit = math.inf # by default, there will be an infinite value, unless specified differently in the input file
        g = Graph(int(f.readline().strip())) # the first line of input will be our vertices parameter for the graph 
        finished = False
        while (not finished):
            line = f.readline()

            if not line:
                return g, timeLimit # we are done with the graph (no more input lines)
            
            else: 
                try:
                    edgeInfo = line.split(' ')
                    if len(edgeInfo) == 4:
                        g.addEdgeWithReleaseTimeAndDeadline(int(edgeInfo[0]), int(edgeInfo[1]), int(edgeInfo[2]), int(edgeInfo[3])) # 0 = starting vertex, 1 = ending vertex, 2 = release time, 3 = deadline

                    elif len(edgeInfo) == 3: 
                        g.addEdgeWithDeadline(int(edgeInfo[0]), int(edgeInfo[1]), int(edgeInfo[2])) # 0 = starting vertex, 1 = ending vertex, 2 = deadline
                    
                    else: 
                        g.addEdge(int(edgeInfo[0]), int(edgeInfo[1]))
                except:
                    try:
                        timeLimit = int(line) # we were given a timelimit input
                    except:
                        timeLimit = math.inf # we were not given a timelimit input value, use default value
        f.close() # done reading file, good practice to close it
        return g, timeLimit # return the newly generated graph
    
    except: # if there was a problem with the file, raise an exception
        raise Exception("Double check the file name you typed: " + graphInstanceFile)