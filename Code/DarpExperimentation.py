import copy
from tqdm import tqdm
import csv
import math
from Graph import Graph
import GraphGenerator
import glob

def findRidesServed(graph, requestOrder, timeLimit):
    """
    This function will calculate the number of rides able to be served when following a particular schedule
    :param requestOrder: A list of edges (pairs of vertices) in the order that they should be served
    :param timeLimit: The time limit the server has to serve the ride requests
    :return: The number of rides served in the given time limit, when serving in the given order
    """
    i = 0
    t = 1
    ridesServed = 1
    if (timeLimit == 0):
        return 0
    
    # WHILE (time hasn't expired, and there are still edges left)
    while (t < timeLimit and i < len(requestOrder) - 1):
        # I am thinking I can check to make sure the deadline is respected before I do anything else, and this should be enough
        if (t > graph.getDeadline(requestOrder[i][0]+1, requestOrder[i][1]+1)):
            return -math.inf # give -infinty value when a deadline is violated

        # IF (the end location of one request is the same as the next requests start location)
        if (requestOrder[i][1] == requestOrder[i + 1][0]):
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
        i += 1

    return ridesServed


def permuteRidesServed(graph, possibleRequests, i, timeLimit, ridesServed):
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


def opt(graph, timeLimit):
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
        return max(ridesServed)

def runTestCases(testFolder):
    """
    This function provides a way to run test cases from a specific directory. The visual of each graph is saved as a png file and shown to the user.
    :param testFolder: Describes the root folder where the test cases are.
    """
    for file in glob.glob(testFolder + "\\test*.txt"): # find every file in the specified folder that is a test file (test#.txt)
        graph = GraphGenerator.generateGraphFromFile(file) 
        print(graph.edges) # print the edges
        Graph.visualizeGraph(graph, file + "Visual.png") # showing visual to the user, also saves as a png image to the folder

if __name__ == '__main__':    
    testFolder = "TestCases"
    runTestCases(testFolder)