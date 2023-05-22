import copy
from tqdm import tqdm
import csv
import math
from Graph import Graph
import GraphGenerator
import glob
import itertools
import random

def OLDfindRidesServed(graph, requestOrder, timeLimit):
    """
    This function will calculate the number of rides able to be served when following a particular schedule
    :param requestOrder: A list of edges (pairs of vertices) in the order that they should be served
    :param timeLimit: The time limit the server has to serve the ride requests
    :return: The number of rides served in the given time limit, when serving in the given order
    """
    i = 0
    t = 1
    ridesServed = 0
    if (timeLimit == 0):
        return 0
    
    # WHILE (time hasn't expired, and there are still edges left)
    while (t < timeLimit and i < len(requestOrder) - 1):
        # I am thinking I can check to make sure the deadline is respected before I do anything else, and this should be enough
        if (t > graph.getDeadline(requestOrder[i][0]+1, requestOrder[i][1]+1)):
            return -math.inf # give -infinty value when a deadline is violated

        # IF (the end location of one request is the same as the next requests start location)
        if (requestOrder[i][1] == requestOrder[i + 1][0]):
            print(requestOrder[i][1])
            ridesServed += 1  # increment the number of rides served the same ammount as the time
            t += 1
        # ELIF (the server must travel to the start of the next request, but runs out of time to complete that request)
        elif (t == timeLimit - 1):
            t += 1
        # ELSE (the server had to travel without serving a request)
        else:
            # travel to beginning of next request and serve it. Increment the time 1 unit more than the rides served
            ridesServed += 1
            t += 2
        print("Iteration: " + str(i) + "\nridesServed: " + str(ridesServed))
        print("timelimit: " + str(timeLimit))
        i += 1

    return ridesServed


def OLDpermuteRidesServed(graph, possibleRequests, i, timeLimit, ridesServed):
    """
    Recursively Add the rides served of each possible permutation of requests to the array.
    :param possibleRequests: List of all edges (pairs of vertices/rides)
    :param i: The index of the request to be switched in the ordering
    :param timeLimit: Time limit for serving requests
    :param ridesServed: Array of all possible rides served
    :return: Array of all possible rides served given permutations
    """
    # IF (the last edge in the list has been reached
    if i == len(possibleRequests):  # get out of recursion
        # Add the rides served gotten from the particular permutation/order of requests
        ridesServed.append(findRidesServed(graph, possibleRequests, timeLimit))
    else:
        for j in range(i, len(possibleRequests)):
            # Switch the ordering of the list of edges
            possibleRequests[i], possibleRequests[j] = possibleRequests[j], possibleRequests[i]

            permuteRidesServed(graph, possibleRequests, i+1, timeLimit, ridesServed)

            # switch the edge back to its original place in the order for next loop
            possibleRequests[i], possibleRequests[j] = possibleRequests[j], possibleRequests[i]
    return ridesServed


def OLDopt(graph, timeLimit):
    """
    Algorithm to find the Max possible number of rides served for a given graph and time limit
    :param graph: Describes the Start and end point of each request to be served
    :param timeLimit: Time allotted to serve requests
    :return: Max possible number of rides served in the given amount of time
    """
    # list of every possible pair of vertices
    possibleEdges = []
    ridesServed = []

    # create list of every possible pair of vertices
    for i in range(graph.V):
        for j in graph.graph[i]:
            possibleEdges.append((i, j))

    # Find the number of rides that can be served for each possible permutation/ordering of requests
    ridesServed = permuteRidesServed(graph, possibleEdges, 0, timeLimit, ridesServed)

    if (len(possibleEdges) == 0):
        return 0
    else:
        print(ridesServed)
        return max(ridesServed)



#########################################################



#########################################################

def findRidesServed(graph, requestOrder, timeLimit):
    """
    This function will calculate the number of rides able to be served when following a particular order of requests
    :param graph: The structure used to represent the requests
    :param requestOrder: A possible list of edges (pairs of vertices) in the order that they should be served
    :param timeLimit: The time limit the server has to serve the ride requests
    :return: The number of rides served in the given time limit, when serving in the given order
    """
    currentRequest = 0 # variable responsible for keeping track of the requests. Must not exceed size of requestOrder 
    currentTime = 1 # variable responsible for keeping track of time. Must not exceed timeLimit
    ridesServed = 0 # variable responsible for keeping track of the number of requests served for this permutation of request orders

    if (timeLimit == 0): return 0 # if the time limit is zero, then we can go ahead and return 0, since we know there are no requests that can be served with this time limit
    
    # We want to see how many requests can be served before the timeLimit is reached or before we serve all requests
    while (currentTime <= timeLimit and currentRequest < len(requestOrder)):
        # make sure the current deadline is respected
        if (currentTime <= graph.getDeadline(requestOrder[currentRequest][0], requestOrder[currentRequest][1])):
            ridesServed += 1 # immediately serve the request
        # if the next request is not continuous with the current request, then a jump needs to be made, so currentTime needs to be incremented to reflect this     
        if ((currentRequest < len(requestOrder) - 1) and (not requestOrder[currentRequest][1] == requestOrder[currentRequest+1][0])):
            currentTime += 1 # we have to make a jump since the next request is not connected

        currentTime += 1 # at this point, either a request was served, or we could not serve the request. The currentTime needs to be incremented by 1 to reflect this
        currentRequest += 1 # update to reflect that regardless of if we served the current request, we need to move to the next request. 
                  
    return ridesServed # return the number of rides that could be served for this specific ordering of requests

def opt(graph, timeLimit):
    """
    Algorithm to find the Max possible number of rides served for a given graph and time limit by using all possible permutations of request orderings
    :param graph: The graph structure being used to represent the requests
    :param timeLimit: The max amount of time that can be used to serve requests
    :return: Max number of rides that can be served out of every possible permutation
    """
    permutationsOfRequests = list(itertools.permutations(graph.edges, graph.getNumberOfRequests())) # We can use the underlying edges collection to find all possible permutations of request orderings 
    ridesServed = [] # collection of every possible number of rides we can serve
    
    for requestOrder in permutationsOfRequests: # We need to find the number of requests that can be served for every permutation of request orderings  
        ridesServed.append(findRidesServed(graph, requestOrder, timeLimit)) # Adding a new possible number of rides that can be served

    if (len(permutationsOfRequests) == 0): # if there are no permutations, then the list will be empty and we return 0
        return 0
    else:
        return max(ridesServed) # return the max possible number of rides that can be served to give the optimal solution    

def runTestCases(testFolder):
    """
    This function provides a way to run test cases from a specific directory. The visual of each graph is saved as a png file and shown to the user.
    :param testFolder: Describes the root folder where the test cases are.
    """
    for file in glob.glob(testFolder + "\\test*.txt"): # find every file in the specified folder that is a test file (test#.txt)
        print("Running: " + file)
        graphInfo = GraphGenerator.generateGraphFromFile(file)
        graph = graphInfo[0] # the graph is at index 0
        timeLimit = graphInfo[1] # the timeLimit is at index 1
        print("opt: " + str(opt(graphInfo[0], graphInfo[1])))
        Graph.visualizeGraph(graph, file + "Visual.png") # showing visual to the user, also saves as a png image to the folder

if __name__ == '__main__':    
    # To run the test cases, the lines until the next empty line need to be uncommented.
    #testFolder = "TestCases"
    #runTestCases(testFolder)
    #file = testFolder + "\\test1.txt"
    #graphInfo = GraphGenerator.generateGraphFromFile(file)
    #Graph.visualizeGraph(graphInfo[0], file + "Visual.png")
    #print("opt: " + str(opt(graphInfo[0], graphInfo[1])))
    
    # Running random graphs with opt to verify that it works
    for n in range(20):
        g = GraphGenerator.createRandomGraphWithDeadlines(4, random.randint(1, 7), n, random.random(), 0.8, 1, 8)
        timeLimit = random.randint(0,15)
        print("opt: " + str(opt(g, timeLimit)) + " with timeLimit: " + str(timeLimit))
        Graph.visualizeGraph(g, "randomGenerator4VerticesTest" + str(n) + ".png")