import copy
from tqdm import tqdm
import csv
import math
from Graph import Graph
import GraphGenerator

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
        ridesServed = 0
    
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


if __name__ == '__main__':    
    
    h=Graph(9,5)
    h.addEdgeWithDeadline(1,2,5)
    h.addEdgeWithDeadline(2,3,5)
    h.addEdgeWithDeadline(3,4,4)
    h.addEdgeWithDeadline(4,5,5)
    h.addEdgeWithDeadline(1,6,0)
    h.addEdgeWithDeadline(6,7,4)
    h.addEdgeWithDeadline(7,8,0)
    h.addEdgeWithDeadline(8,9,4)
    print(h.id)
    print(h.edges)

    print("opt",opt(h,5))
    f=copy.deepcopy(h)

    test = "test1.txt"
    g = GraphGenerator.generateGraphFromFile(test)
    print(g.edges)

    print("opt",opt(g,5))
    f=copy.deepcopy(g)

    #z = GraphGenerator.generateRequestGraphsWithDeadlines(3, 0.7, 3, 7, 4)
    #print(*z,sep="\n")

    #w = GraphGenerator.generateRequestGraphsWithoutDeadlines(3)
    #print(*w,sep="\n")

    #z = GraphGenerator.createRandomGraphWithDeadlines(7, 13, 3, 0.8, 4, 9)
    #print(z)
    #f=copy.deepcopy(z)
    #print("opt",opt(z,11))


    #z = GraphGenerator.generateRequestGraphsWithDeadlines(3, 0.7, 3, 7, 4)
    #print(*z,sep="\n")

    #z = GraphGenerator.generateRequestGraphsWithDeadlines(3, 0.7, 3, 7, 4)
    #print(*z,sep="\n")
    Graph.vizualizeGraph(g, "exampleFromExpectations.png") # testing the newly added vizualization function in Graph
   