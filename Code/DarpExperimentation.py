#import copy
#from tqdm import tqdm
#import csv
#import math
from Graph import Graph
import GraphGenerator
import glob
import itertools
import random

def findRidesServed(graph, requestOrder, timeLimit, paths, timeRecord):
    """
    This function will calculate the number of rides able to be served when following a particular order of requests
    :param graph: The structure used to represent the requests
    :param requestOrder: A possible list of edges (pairs of vertices) in the order that they should be served
    :param timeLimit: The time limit the server has to serve the ride requests
    :return: A set containing the number of rides served in the given time limit and the path taken, when serving in the given order
    """
    currentRequest = 0 # variable responsible for keeping track of the requests. Must not exceed size of requestOrder 
    currentTime = 1 # variable responsible for keeping track of time. Must not exceed timeLimit
    ridesServed = 0 # variable responsible for keeping track of the number of requests served for this permutation of request orders
    pathTaken = []
    timeFootprint = []
    if (timeLimit == 0): return 0 # if the time limit is zero, then we can go ahead and return 0, since we know there are no requests that can be served with this time limit
    
    # We want to see how many requests can be served before the timeLimit is reached or before we serve all requests
    while (currentTime < timeLimit and currentRequest < len(requestOrder)):
        # make sure the current deadline is respected
        if (graph.getReleaseTime(requestOrder[currentRequest][0], requestOrder[currentRequest][1]) <= currentTime < graph.getDeadline(requestOrder[currentRequest][0], requestOrder[currentRequest][1])):
            ridesServed += 1 # immediately serve the request
            pathTaken.append(requestOrder[currentRequest])
            timeFootprint.append(currentTime + 1)
        # if the next request is not continuous with the current request, then a jump needs to be made, so currentTime needs to be incremented to reflect this     
        if ((currentRequest < len(requestOrder) - 1) and (not requestOrder[currentRequest][1] == requestOrder[currentRequest+1][0])):
            currentTime += 1 # we have to make a jump since the next request is not connected
            if (currentTime < timeLimit): timeFootprint.append('x')
        
        currentTime += 1 # at this point, either a request was served, or we could not serve the request. The currentTime needs to be incremented by 1 to reflect this
        currentRequest += 1 # update to reflect that regardless of if we served the current request, we need to move to the next request. 
                  
    timeRecord.append(timeFootprint)
    paths.append(pathTaken)              
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
    paths = []
    timeRecord = []
    for requestOrder in permutationsOfRequests: # We need to find the number of requests that can be served for every permutation of request orderings  
        ridesServed.append(findRidesServed(graph, requestOrder, timeLimit, paths, timeRecord)) # Adding a new possible number of rides that can be served

    if (len(permutationsOfRequests) == 0): # if there are no permutations, then the list will be empty and we return 0
        return 0
    else:
        #findPathOfRidesServed(permutationsOfRequests.index(max(ridesServed))) # this function will print the path taken by OPT in order to help with troubleshooting. 
        #print(ridesServed)
        #print(formatPathServed(ridesServed[ridesServed[0].index(max(ridesServed)[0])][1]))
    
        optimalSolution = max(ridesServed)
        print(timeRecord[ridesServed.index(optimalSolution)])
        print(paths[ridesServed.index(optimalSolution)])
        return optimalSolution, timeRecord[ridesServed.index(optimalSolution)], paths[ridesServed.index(optimalSolution)] # return the max possible number of rides that can be served to give the optimal solution

def updateRequests(currentTime, requests):
    """
    EDF helper function used to update the available requests that can be served by ensuring that requests from a collection are only added to availableRequests if the release time and deadlines are respected.
    :param currentTime: The variable used to represent the currentTime in the EDF Algorithm instance
    :param requests: Collection of possible requests as keys and their deadlines as the values
    :return: availableRequests, a collection of all requests that are able to be served at currentTime
    """
    availableRequests = [] # collection of requests that will be returned
    for r in requests: # go through every possible request
        releaseTime = requests[r][0] # the first value is the release time
        deadline = requests[r][1] # the second value is the deadline 
        #print(str(currentTime) + ":" + str(deadline))
            
        if releaseTime <= currentTime < deadline: # a request must have a relase time that is at least the current time and a deadline that is no greater than the current time
            availableRequests.append(r) # a new request can be added to the collection of available requests
    return availableRequests # return the collection of available requests
    
def edf(graph, timeLimit):
    """
    This algorithm is used to find the max number of rides that can be served if requests are served based on earliest deadline first within a given timelimit.
    :param graph: The graph used to represent the problem, the graph contains all requests and deadlines
    :param timeLimit: The maximum amount of time units the algorithm is allowed to serve rides for
    :return: The maximum number of rides that can be served based on the EDF algorithm
    """
    windowSize = 2 # the amount of time units we can look forward
    currentTime = 1 # current time starts at 1 because it is assumed the first time unit will be used to move to any initial location
    ridesServed = 0 # number of rides that have been served
    requests = dict(sorted(graph.edges.items(), key=lambda x: x[1])) # all edges that are in a given graph sorted initially by earliest deadline since we want to serve earlier deadlines first if possible
    availableRequests = [] # available requests that we are able to serve, must be updated at the beginning of every iteration, and if a request is served
    requestsServed = [] # a collection to keep track of every request that was served and in what order it was served (mainly used for debugging purposes)
    timeServed = [] # a collection to keep track of what time the requests were actually served
    while currentTime <= timeLimit: # the algorithm ends when the time limit is reached
        availableRequests = updateRequests(currentTime, requests) # the available requests needs to be updated at the start of every iteration before we serve any rides

        if len(availableRequests) > 0: # if there are requests we can serve, we should serve them
            ridesServed += 1 # serve the request 
            requestsServed.append(availableRequests[0]) # the first index of available requests is the one served since the request collection was sorted based on deadlines 
            currentRequest = availableRequests[0] # used to keep track of the current request before it is deleted 
            del availableRequests[0] # delete the request that was just served
            del requests[currentRequest] # delete the request from the request collection to make sure it is not possible served again
            currentTime += 1 # increment the current time to reflect we have served a request
            windowSize = 2 # this will reset the windowSize if it was ever updated. It is important that after a request is served, the window size is set back to 2
            timeServed.append(currentTime)
            availableRequests = updateRequests(currentTime, requests) # serving a request means we must update the available requests, this is due to the current time changing (previously existing requests may be unservable)
            if len(availableRequests) > 0 and not currentRequest[1] == availableRequests[0][0]: # check if a jump needs to be made
                currentTime+=1 # a jump will be required, so we must increment the current time by one time unit to reflect this
                timeServed.append('x')

        else: # there are no available requests, we may have to increase the window size to be able to serve requests
            if windowSize < timeLimit: # only increase the window size if the current window size is smaller than the time limit
                windowSize += 1 # increase the window size
                currentTime += 1 # the action of increasing the window size still requires us to increase the current time by one unit since a time unit elapsed (we were just not able to serve anything)
                timeServed.append('x')
    
    print(timeServed)
    print("REQUESTS SERVED: " + str(requestsServed)) # nice debugging way to see which requests were served before the final solution is returned            
    return ridesServed, timeServed, requestsServed # return the number of requests that were served by the EDF algorithm

def runTestCases(testFolder):
    """
    This function provides a way to run test cases from a specific directory. The visual of each graph is saved as a png file and shown to the user.
    :param testFolder: Describes the root folder where the test cases are.
    """
    for file in glob.glob(testFolder + "\\test*.txt"): # find every file in the specified folder that is a test file (test#.txt)
    #for file in glob.glob(testFolder + "\\test1.txt"): # find every file in the specified folder that is a test file (test#.txt)
        print("Running: " + file)
        graphInfo = GraphGenerator.generateGraphFromFile(file)
        graph = graphInfo[0] # the graph is at index 0
        timeLimit = Graph.getTimeLimit(graph, graphInfo[1]) # the timeLimit is at index 1
        Graph.visualizeGraph(graph, timeLimit, file) # showing visual to the user, also saves as a png image to the folder
        optInfo = opt(graph, timeLimit)
        print("opt: " + str(optInfo[0])+ " with timeLimit: " + str(timeLimit))
        Graph.visualizeGraphSolution(graph, timeLimit, optInfo[1], optInfo[2], "OPT" , file)
        edfInfo = edf(graph, timeLimit)
        print("edf: " + str(edfInfo[0])+ " with timeLimit: " + str(timeLimit))
        Graph.visualizeGraphSolution(graph, timeLimit, edfInfo[1], edfInfo[2], "EDF" , file)


if __name__ == '__main__':    
    # To run the test cases, the lines until the next empty line need to be uncommented.
    testFolder = "TestCases"
    runTestCases(testFolder)
    
    # Running random graphs with opt to verify that it works
    #for n in range(20):
    #    g = GraphGenerator.createRandomGraphWithDeadlines(4, random.randint(1, 7), n, random.random(), 0.8, 1, 8)
    #    timeLimit = random.randint(0,15)
        #print("opt: " + str(opt(g, timeLimit)) + " with timeLimit: " + str(timeLimit))
    #    Graph.visualizeGraph(g, "randomGenerator4VerticesTest" + str(n) + ".png")
    #graphs = GraphGenerator.generateRequestGraphsWithDeadlines(4, 0.8, 1, 7, 5)
    #for g in graphs:
    #    Graph.visualizeGraph(g, "randomRequestGeneratorWith4Vertices5CopiesTest" + str(g.id) + ".png")
        #g = GraphGenerator.createRandomGraphWithDeadlines(4, random.randint(1, 7), 0, .6, 0.8, 1, 5)
        #timeLimit = random.randint(0,15)
        #print("opt: " + str(edf(g, timeLimit)) + " with timeLimit: " + str(timeLimit))
        #Graph.visualizeGraph(g, "randomRequestGeneratorWithInfiniteTest" + str(g.id) + ".png")

        