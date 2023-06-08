import math
from Graph import Graph
import itertools
import time

def findRidesServed(graph, requestOrder, timeLimit, currentOptimalRidesServed, paths, timeRecord):
    """
    This function will calculate the number of rides able to be served when following a particular order of requests
    :param graph: The structure used to represent the requests
    :param requestOrder: A possible list of edges (pairs of vertices) in the order that they should be served
    :param timeLimit: The time limit the server has to serve the ride requests
    :return: A set containing the number of rides served in the given time limit and the path taken, when serving in the given order
    """
    currentRequest = 0 # variable responsible for keeping track of the requests. Must not exceed size of requestOrder 
    currentTime = 1 # variable responsible for keeping track of time. Must not exceed timeLimit. Starts at two because that is the first time we are able to serve requests
    currentRidesServed = 0 # variable responsible for keeping track of the number of requests served for this permutation of request orders
    pathTaken = []
    timeFootprint = []
    #if (timeLimit == 0): return 0 # if the time limit is zero, then we can go ahead and return 0, since we know there are no requests that can be served with this time limit
    # We want to see how many requests can be served before the timeLimit is reached or before we serve all requests
    while (currentTime < timeLimit and currentRequest < len(requestOrder)):
        release = graph.getReleaseTime(requestOrder[currentRequest][0], requestOrder[currentRequest][1])
        deadline = graph.getDeadline(requestOrder[currentRequest][0], requestOrder[currentRequest][1])
        # make sure the current deadline is respected
        if (release <= currentTime < deadline):
            currentRidesServed += 1 # immediately serve the request
            pathTaken.append(requestOrder[currentRequest])
            timeFootprint.append(currentTime)
        # if the next request is not continuous with the current request, then a jump needs to be made, so currentTime needs to be incremented to reflect this     
            if ((currentRequest < len(requestOrder) - 1) and (not requestOrder[currentRequest][1] == requestOrder[currentRequest+1][0])):
                currentTime += 1 # we have to make a jump since the next request is not connected
            
            currentRequest += 1 # update to reflect that regardless of if we served the current request, we need to move to the next request.
            
        currentTime += 1 # at this point, either a request was served, or we could not serve the request. The currentTime needs to be incremented by 1 to reflect this

    if currentRidesServed > currentOptimalRidesServed[0]:
        del currentOptimalRidesServed[0]
        del timeRecord[0] # delete existing sub-optimal solution
        del paths[0] # delete existing sub-optimal solution 
    
        timeRecord.append(timeFootprint)
        paths.append(pathTaken)
        currentOptimalRidesServed.append(currentRidesServed)              

def opt(graph, timeLimit):
    """
    Algorithm to find the Max possible number of rides served for a given graph and time limit by using all possible permutations of request orderings
    :param graph: The graph structure being used to represent the requests
    :param timeLimit: The max amount of time that can be used to serve requests
    :return: Max number of rides that can be served out of every possible permutation
    """
    start = time.time()
    #permutationsOfRequests = itertools.permutations(graph.edges, graph.getNumberOfRequests()) # We can use the underlying edges collection to find all possible permutations of request orderings 
    ridesServed = [0] # collection of current best number of rides served
    paths = ['x'] # collection of current best path taken
    timeRecord = ['x'] # collection of current best time record
    factorial = math.factorial(graph.getNumberOfRequests())
    #for requestOrder in itertools.islice(permutationsOfRequests, factorial): # We need to find the number of requests that can be served for every permutation of request orderings  
    for requestOrder in itertools.permutations(graph.edges): # We need to find the number of requests that can be served for every permutation of request orderings  
        findRidesServed(graph, requestOrder, timeLimit, ridesServed, paths, timeRecord) # Adding a new possible number of rides that can be served

    end = time.time()
    timeTaken = end - start # time taken in seconds 
    return ridesServed[0], timeRecord[0], paths[0], timeTaken # return the max possible number of rides that can be served to give the optimal solution