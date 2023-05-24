#import copy
#from tqdm import tqdm
#import csv
#import math
from Graph import Graph
import GraphGenerator
import glob
import itertools
import random

def findRidesServedOPT(graph, requestOrder, timeLimit, paths, timeRecord):
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
    pathTaken = ""
    timeFootprint = []
    if (timeLimit == 0): return 0 # if the time limit is zero, then we can go ahead and return 0, since we know there are no requests that can be served with this time limit
    
    # We want to see how many requests can be served before the timeLimit is reached or before we serve all requests
    while (currentTime <= timeLimit and currentRequest < len(requestOrder)):
        # make sure the current deadline is respected
        if (currentTime <= graph.getDeadline(requestOrder[currentRequest][0], requestOrder[currentRequest][1])):
            ridesServed += 1 # immediately serve the request
            pathTaken += str(requestOrder[currentRequest][0]) + "-" + str(requestOrder[currentRequest][1]) + "\n"
            timeFootprint.append(currentTime)
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
        ridesServed.append(findRidesServedOPT(graph, requestOrder, timeLimit, paths, timeRecord)) # Adding a new possible number of rides that can be served

    if (len(permutationsOfRequests) == 0): # if there are no permutations, then the list will be empty and we return 0
        return 0
    else:
        #findPathOfRidesServed(permutationsOfRequests.index(max(ridesServed))) # this function will print the path taken by OPT in order to help with troubleshooting. 
        #print(ridesServed)
        #print(formatPathServed(ridesServed[ridesServed[0].index(max(ridesServed)[0])][1]))
        print(timeRecord[ridesServed.index(max(ridesServed))])
        print(paths[ridesServed.index(max(ridesServed))])
        return max(ridesServed) # return the max possible number of rides that can be served to give the optimal solution
            
def updateRequests(graph, requests, availableRequests, currentTime, windowSize, timeLimit):
    
    # remove all existing requests that cannot be served in availableRequests
    #print(len(availableRequests))
    #print(len(availableRequests)-1)
    i = len(availableRequests)-1
    while (i > 0):
        #print("Currenttime: " + str(currentTime))
        #print("iteration: " + str(i))
        if currentTime > graph.getDeadline(availableRequests[i][0], availableRequests[i][1]):
            del availableRequests[i]
        i -= 1
    
    # remove all requests that cannot be served (violated deadlines) from requests
    releaseTime = 0 # for now all have release times of 0 until edf is working
    delete = set() # requests that are violated or that are added to available requests are deleted from requests since they will either be served or end up becoming violated
    for request in requests:
        if currentTime > requests[request]: 
            delete.add(request) # violated deadline, remove from after
        
        # add requests to availableRequests if they can be served (respecting arrival time and deadline and windowsize)
        if releaseTime <= currentTime <= requests[request]:
            availableRequests.append(request)
            delete.add(request) 

    #print(delete)
    delete = list(delete)
    for d in range(len(delete)):
        del requests[delete[d]]

    # every request we add needs to be deleted from requests
    #return 0

def edf(graph, timeLimit):
    windowSize = 2 # amount of time units we are able to look ahead
    currentTime = 1 # the current time is 1 to imply moving from an origin point and moving to the first request within the time [0,1]
    availableRequests = [] # collection of requests that can be served, must be updated after every iteration
    #requests = graph.edges # collection of every request (requests that are served or cannot be served are removed from here)
    requests = dict(sorted(graph.edges.items(), key=lambda x: x[1]))
    #print(requests)
    #print(sortedRequests)
    # need to make the initial population of requests in available requests
    print("Possible Requests to Serve: " + str(availableRequests))
    updateRequests(graph, requests, availableRequests, currentTime, windowSize, timeLimit)
    print("Possible Requests to Serve: " + str(availableRequests))

    ridesServed = 0 # number of rides we have served
    # continue looping until either we reach the time limit, we serve all requests, or window equals the timelimit (may not be important)
    previousRequest = (0,0) # starts off at "origin point" because we know it can never be a valid request location
    #previousRequest = availableRequests[0] # by default make the previousRequest the first item in availableRequests
    requestsServed = []
    while (currentTime <= timeLimit and (len(requests) > 0 or len(availableRequests) > 0)):
        # check if there are available requests
        if len(availableRequests) > 0:
            ridesServed += 1 # serve the request
            print("SERVED REQUEST: " + str(availableRequests[0]) + " AT TIME: " + str(currentTime))
            requestsServed.append(availableRequests[0])
            #currentTime += 1 # increment the time
            # a jump was made if the previous request's end coordinate is not the same as the start of the next request
            if previousRequest == (0,0) and (not previousRequest[1] == availableRequests[0][0]):
                currentTime += 1
                print("JUMP AT TIME: " + str(currentTime))

            del availableRequests[0] # remove the request from availableRequests
            #print("Possible Requests to Serve: " + str(availableRequests))

        # else, there were no available requests
        else: 
            # check if windowSize < timeLimit
            if windowSize < timeLimit:
                windowSize +=1 # increment the windowSize
                #currentTime +=1 # if it cannot serve and needs to increase window size, this means a time unit must have elapsed???
        currentTime+=1        
        updateRequests(graph, requests, availableRequests, currentTime, windowSize, timeLimit) # regardless update availableRequests here
        print("Possible Requests to Serve: " + str(availableRequests))

        # increment one timeunit here????           
    print("Requests Served: " + str(requestsServed))
    return ridesServed

def runTestCases(testFolder):
    """
    This function provides a way to run test cases from a specific directory. The visual of each graph is saved as a png file and shown to the user.
    :param testFolder: Describes the root folder where the test cases are.
    """
    #for file in glob.glob(testFolder + "\\test*.txt"): # find every file in the specified folder that is a test file (test#.txt)
    for file in glob.glob(testFolder + "\\test1.txt"): # find every file in the specified folder that is a test file (test#.txt)
        print("Running: " + file)
        graphInfo = GraphGenerator.generateGraphFromFile(file)
        graph = graphInfo[0] # the graph is at index 0
        timeLimit = graphInfo[1] # the timeLimit is at index 1
        #print("opt: " + str(opt(graph, timeLimit))+ " with timeLimit: " + str(timeLimit))
        print("edf: " + str(edf(graph, timeLimit))+ " with timeLimit: " + str(timeLimit))
        Graph.visualizeGraph(graph, file + "Visual.png") # showing visual to the user, also saves as a png image to the folder

if __name__ == '__main__':    
    # To run the test cases, the lines until the next empty line need to be uncommented.
    testFolder = "TestCases"
    runTestCases(testFolder)
    
    # Running random graphs with opt to verify that it works
    #for n in range(20):
        #g = GraphGenerator.createRandomGraphWithDeadlines(4, random.randint(1, 7), n, random.random(), 0.8, 1, 8)
        #timeLimit = random.randint(0,15)
        #print("opt: " + str(opt(g, timeLimit)) + " with timeLimit: " + str(timeLimit))
        #Graph.visualizeGraph(g, "randomGenerator4VerticesTest" + str(n) + ".png")
    #graphs = GraphGenerator.generateRequestGraphsWithDeadlines(4, 0.8, 1, 7, 5)
    #for g in graphs:
    #    Graph.visualizeGraph(g, "randomRequestGeneratorWith4Vertices5CopiesTest" + str(g.id) + ".png")
        #g = GraphGenerator.createRandomGraphWithDeadlines(4, random.randint(1, 7), 0, .6, 0.8, 1, 5)
        #timeLimit = random.randint(0,15)
        #print("opt: " + str(edf(g, timeLimit)) + " with timeLimit: " + str(timeLimit))
        #Graph.visualizeGraph(g, "randomRequestGeneratorWithInfiniteTest" + str(g.id) + ".png")

        