#import copy
#from tqdm import tqdm
import csv
import math
from Graph import Graph
import GraphGenerator
import glob
import itertools
import random

def findRidesServed(graph, requestOrder, timeLimit, currentOptimalRidesServed, paths, timeRecord):
    """
    This function will calculate the number of rides able to be served when following a particular order of requests
    :param graph: The structure used to represent the requests
    :param requestOrder: A possible list of edges (pairs of vertices) in the order that they should be served
    :param timeLimit: The time limit the server has to serve the ride requests
    :return: A set containing the number of rides served in the given time limit and the path taken, when serving in the given order
    """
    currentRequest = 0 # variable responsible for keeping track of the requests. Must not exceed size of requestOrder 
    currentTime = 2 # variable responsible for keeping track of time. Must not exceed timeLimit. Starts at two because that is the first time we are able to serve requests
    currentRidesServed = 0 # variable responsible for keeping track of the number of requests served for this permutation of request orders
    pathTaken = []
    timeFootprint = []
    if (timeLimit == 0): return 0 # if the time limit is zero, then we can go ahead and return 0, since we know there are no requests that can be served with this time limit
    #print("HERE")
    #print(requestOrder)
    # We want to see how many requests can be served before the timeLimit is reached or before we serve all requests
    while (currentTime <= timeLimit and currentRequest < len(requestOrder)):
        # make sure the current deadline is respected
        if (graph.getReleaseTime(requestOrder[currentRequest][0], requestOrder[currentRequest][1]) <= currentTime <= graph.getDeadline(requestOrder[currentRequest][0], requestOrder[currentRequest][1])):
            currentRidesServed += 1 # immediately serve the request
            pathTaken.append(requestOrder[currentRequest])
            timeFootprint.append(currentTime)
        # if the next request is not continuous with the current request, then a jump needs to be made, so currentTime needs to be incremented to reflect this     
            if ((currentRequest < len(requestOrder) - 1) and (not requestOrder[currentRequest][1] == requestOrder[currentRequest+1][0])):
                currentTime += 1 # we have to make a jump since the next request is not connected
                if (currentTime < timeLimit): timeFootprint.append('x')
            currentRequest += 1 # update to reflect that regardless of if we served the current request, we need to move to the next request. 
        

        currentTime += 1 # at this point, either a request was served, or we could not serve the request. The currentTime needs to be incremented by 1 to reflect this

    if currentRidesServed > currentOptimalRidesServed:
        if len(timeRecord) > 0: # something already exists and needs to be deleted
            del timeRecord[0] # delete existing sub-optimal solution
            del paths[0] # delete existing sub-optimal solution 
        
        timeRecord.append(timeFootprint)
        paths.append(pathTaken)
        return currentRidesServed              
    
    else: return currentOptimalRidesServed # return the number of rides that could be served for this specific ordering of requests



def divide_chunks(iterable, chunk_size):
    # Divide the iterable into smaller chunks
    iterator = iter(iterable)
    while True:
        chunk = list(itertools.islice(iterator, chunk_size))
        if not chunk:
            return
        yield chunk

def opt(graph, timeLimit):
    """
    Algorithm to find the Max possible number of rides served for a given graph and time limit by using all possible permutations of request orderings
    :param graph: The graph structure being used to represent the requests
    :param timeLimit: The max amount of time that can be used to serve requests
    :return: Max number of rides that can be served out of every possible permutation
    """
    permutationsOfRequests = itertools.permutations(graph.edges, graph.getNumberOfRequests())
    ridesServed = [] # collection of every possible number of rides we can serve
    paths = []
    timeRecord = []
    chunk_size = 100000
    
    for chunk in divide_chunks(permutationsOfRequests, chunk_size):
        print(chunk)
        for requestOrder in chunk:
            #print(requestOrder)
            #print("+++++++++++++++++")
            #print(chunk)
            #print(itertools.chain.from_iterable(chunk))
            ridesServed.append(findRidesServed(graph, requestOrder, timeLimit, paths, timeRecord))
            #ridesServed.append(findRidesServed(graph, chunk, timeLimit, paths, timeRecord))

    optimalSolution = max(ridesServed)
    optimalIndex = ridesServed.index(optimalSolution)
    return optimalSolution, timeRecord[optimalIndex], paths[optimalIndex]


def optOriginal(graph, timeLimit):
    """
    Algorithm to find the Max possible number of rides served for a given graph and time limit by using all possible permutations of request orderings
    :param graph: The graph structure being used to represent the requests
    :param timeLimit: The max amount of time that can be used to serve requests
    :return: Max number of rides that can be served out of every possible permutation
    """
    
    
    
    permutationsOfRequests = itertools.permutations(graph.edges, graph.getNumberOfRequests()) # We can use the underlying edges collection to find all possible permutations of request orderings 
    #smallerPermutationsOfRequests = itertools.islice(permutationsOfRequests, 100000)
    ridesServed = 0 # collection of current best number of rides served
    paths = [] # collection of current best path taken
    timeRecord = [] # collection of current best time record
    factorial = math.factorial(graph.getNumberOfRequests())
    for requestOrder in itertools.islice(permutationsOfRequests, factorial): # We need to find the number of requests that can be served for every permutation of request orderings  
        ridesServed = findRidesServed(graph, next(permutationsOfRequests), timeLimit, ridesServed, paths, timeRecord) # Adding a new possible number of rides that can be served

    #if (len(permutationsOfRequests) == 0): # if there are no permutations, then the list will be empty and we return 0
     #   return 0
    #else:
        #findPathOfRidesServed(permutationsOfRequests.index(max(ridesServed))) # this function will print the path taken by OPT in order to help with troubleshooting. 
        #print(ridesServed)
        #print(formatPathServed(ridesServed[ridesServed[0].index(max(ridesServed)[0])][1]))
    
    #optimalSolution = max(ridesServed)
    #print(timeRecord[ridesServed.index(optimalSolution)])
    #print(paths[ridesServed.index(optimalSolution)])
    return ridesServed, timeRecord[0], paths[0] # return the max possible number of rides that can be served to give the optimal solution

def updateRequests(currentTime, requests, windowSize):
    """
    EDF helper function used to update the available requests that can be served by ensuring that requests from a collection are only added to availableRequests if the release time and deadlines are respected.
    :param currentTime: The variable used to represent the currentTime in the EDF Algorithm instance
    :param requests: Collection of possible requests as keys and their deadlines as the values
    :param windowSize: The number of time units we are able to look ahead if there are no available requests at current time unit
    :return: availableRequests, a collection of all requests that are able to be served at currentTime
    """
    availableRequests = [] # collection of requests that will be returned
    for r in requests: # go through every possible request
        releaseTime = requests[r][0] # the first value is the release time
        deadline = requests[r][1] # the second value is the deadline 
        
        if releaseTime <= currentTime + windowSize - 2 <= deadline: # we can look ahead using the window size if need be. Since the window size is default of 2, this also makes sure we do not look ahead if we do not need to (windowsize - 2 would be 0 in this case) 
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
    currentTime = 2 # current time starts at 2 because it is assumed the first time unit will be used to move to any initial location, therefore 2 can be the earliest time a request can be served
    ridesServed = 0 # number of rides that have been served
    requests = dict(sorted(graph.edges.items(), key=lambda x: x[1][1])) # all edges that are in a given graph sorted initially by earliest deadline since we want to serve earlier deadlines first if possible
    availableRequests = [] # available requests that we are able to serve, must be updated at the beginning of every iteration, and if a request is served
    requestsServed = [] # a collection to keep track of every request that was served and in what order it was served (mainly used for debugging purposes)
    timeServed = [] # a collection to keep track of what time the requests were actually served

    while currentTime <= timeLimit and len(requests) + len(availableRequests) > 0 and windowSize < timeLimit: # the algorithm ends when the time limit is reached
      
        availableRequests = updateRequests(currentTime, requests, windowSize) # the available requests needs to be updated at the start of every iteration before we serve any rides
        
        if len(availableRequests) > 0: # if there are requests we can serve, we should serve them
            if windowSize > 2: # if the window size is larger than the default value (2), then that means the window increased
                currentTime += windowSize - 2 # the current time needs to be increased by the size of the window -2 since the default value of the window is 2
                windowSize = 2 # this will reset the windowSize if it was ever updated. It is important that after a request is served, the window size is set back to 2
            
            ridesServed += 1 # serve the request 
            requestsServed.append(availableRequests[0]) # the first index of available requests is the one served since the request collection was sorted based on deadlines 
            currentRequest = availableRequests[0] # used to keep track of the current request before it is deleted 
            del availableRequests[0] # delete the request that was just served
            del requests[currentRequest] # delete the request from the request collection to make sure it is not possible served again
            timeServed.append(currentTime)
            currentTime += 1 # increment the current time to reflect we have served a request
            availableRequests = updateRequests(currentTime, requests, windowSize) # serving a request means we must update the available requests, this is due to the current time changing (previously existing requests may be unservable)
            if len(availableRequests) > 0 and not currentRequest[1] == availableRequests[0][0]: # check if a jump needs to be made
                currentTime+=1 # a jump will be required, so we must increment the current time by one time unit to reflect this
                timeServed.append('x')
        else: # there are no available requests, we may have to increase the window size to be able to serve requests
            if windowSize < timeLimit: # only increase the window size if the current window size is smaller than the time limit
                windowSize += 1 # increase the window size
                timeServed.append('x')
                
    print(timeServed)
    print("REQUESTS SERVED: " + str(requestsServed)) # nice debugging way to see which requests were served before the final solution is returned            
    return ridesServed, timeServed, requestsServed # return the number of requests that were served by the EDF algorithm


def runTestCases(testFolder):
    """
    This function provides a way to run test cases from a specific directory. The visual of each graph is saved as a png file and shown to the user.
    :param testFolder: Describes the root folder where the test cases are.
    """
    with open(testFolder + "Report.csv", 'w', newline='') as report: # create a csv report of the results. This is where any flagged test cases will be reported
        writer = csv.writer(report) # create the writer for the csv file
        fields = ["flag", "testcase", "OPT", "EDF"] # fields of what will be written to the csv
        writer.writerow(fields) # writing the first row to csv file - contains all the fields
    
        for file in glob.glob(testFolder + "\\test*.txt"): # find every file in the specified folder that is a test file (test#.txt)
            print("Running: " + file) # print statement to let the user know which file test case is currently running
            graphInfo = GraphGenerator.generateGraphFromFile(file) # function to generate the graph from the specified file
            graph = graphInfo[0] # the graph is at index 0
            timeLimit = Graph.getTimeLimit(graph, graphInfo[1]) # the timeLimit is at index 1
            #print(timeLimit)
            Graph.visualizeGraph(graph, timeLimit, file) # save visual of the graph prior to any algorithms being run
            optInfo = optOriginal(graph, timeLimit) # optInfo contains everything returned by opt algorithm
            print("opt: " + str(optInfo[0])+ " with timeLimit: " + str(timeLimit)) # display opt result to console
            Graph.visualizeGraphSolution(graph, timeLimit, optInfo[1], optInfo[2], "OPT" , file) # create visual of opt result and store it in test suite directory
            edfInfo = edf(graph, timeLimit) # edge info contains everything returned by edf algorithm
            print("edf: " + str(edfInfo[0])+ " with timeLimit: " + str(timeLimit)) # display edf result to console
            Graph.visualizeGraphSolution(graph, timeLimit, edfInfo[1], edfInfo[2], "EDF" , file) # create visual of edf result and store it in test suite directory
            if edfInfo[0] == 2*optInfo[0]: # need to report when edf solution is equal to 2*opt solution
                writer.writerow(["|EDF| = 2*|OPT|", file, optInfo[0], edfInfo[0]])
    
            if edfInfo[0] != optInfo[0]: # need to report when the two solutions are not the same
                writer.writerow(["|EDF| differs from |OPT|", file, optInfo[0], edfInfo[0]])
    
            if edfInfo[0] > optInfo[0]: # need to report when edf does better than opt (this should never happen)
                writer.writerow(["|EDF| > |OPT|", file, optInfo[0], edfInfo[0]])
    
            if 2*edfInfo[0] < optInfo[0]: # need to report when edf does has a solution more than twice as less than opt (should also never happen)
                writer.writerow(["|EDF| < 2*|OPT|", file, optInfo[0], edfInfo[0]])
        

if __name__ == '__main__':    
    # To run the test cases, the lines until the next empty line need to be uncommented.
    #testFolder = "TestCases"
    testFolder = "TestCases\\Archived Test Cases"
    runTestCases(testFolder)
    #testFolder = "TestCases"
    #runTestCases(testFolder)
    
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

        