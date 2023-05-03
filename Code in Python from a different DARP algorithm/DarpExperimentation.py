import copy
import matplotlib.pyplot as plt
from tqdm import tqdm
import csv
from GraphGenerator import createRandomGraph

def findProfit(requestOrder, timeLimit):
    """
    This function will calculate the number of rides able to be served when following a particular schedule
    :param requestOrder: A list of edges (pairs of vertices) in the order that they should be served
    :param timeLimit: The time limit the server has to serve the ride requests
    :return: The number of rides served in the given time limit, when serving in the given order
    """
    i = 0
    t = 1
    profit = 1
    if (timeLimit == 0):
        profit = 0
    # print("request order: ", requestOrder)
    # WHILE (time hasn't expired, and there are still edges left)
    while (t < timeLimit and i < len(requestOrder) - 1):
        # IF (the end location of one request is the same as the next requests start location)
        if (requestOrder[i][1] == requestOrder[i + 1][0]):
            profit += 1  # increment the profit the same ammount as the time
            t += 1
        # ELIF (the server must travel to the start of the next request, but runs out of time to complete that request)
        elif (t == timeLimit - 1):
            t += 1
        # ELSE (the server had to travel without serving a request)
        else:
            # travel to beginning of next request and serve it. Increment the time 1 unit more than the profit
            profit += 1
            t += 2
        i += 1
    # print("PROFIT: ", profit)
    return profit


def permuteProfits(possibleRequests, i, timeLimit, profits):
    """
    Recursively Add the profit of each possible permutation of requests to the array. (profit = #rides served)
    :param possibleRequests: List of all edges (pairs of vertices/rides)
    :param i: The index of the request to be switched in the ordering
    :param timeLimit: Time limit for serving requests
    :param profits: Array of all possible profits
    :return: Array of all possible profits given permutations
    """
    # IF (the last edge in the list has been reached
    if i == len(possibleRequests):  # get out of recursion
        # Add the profit gotten from the particular permutation/order of requests
        profits.append(findProfit(possibleRequests, timeLimit))
    else:
        for j in range(i, len(possibleRequests)):
            # Switch the ordering of the list of edges
            possibleRequests[i], possibleRequests[j] = possibleRequests[j], possibleRequests[i]

            permuteProfits(possibleRequests, i+1, timeLimit,profits)

            # switch the edge back to its original place in the order for next loop
            possibleRequests[i], possibleRequests[j] = possibleRequests[j], possibleRequests[i]
    return profits


def opt(graph, timeLimit):
    """
    Algorithm to find the Max possible profit/ num rides served for a given graph and time limit
    :param graph: Describes the Start and end point of each request to be served
    :param timeLimit: Time allotted to serve requests
    :return: Max possible number of rides served in the given amount of time
    """
    # list of every possible pair of vertices
    possibleEdges = []
    profits = []

    # create list of every possible pair of vertices
    for i in range(graph.V):
        for j in graph.graph[i]:
            possibleEdges.append((i, j))

    # Find the profit for each possible permutation/ordering of requests
    profits = permuteProfits(possibleEdges, 0, timeLimit, profits)

    if (len(possibleEdges) == 0):
        return 0
    else:
        return max(profits)


def longestTrailAlgorithm(graph, timeLimit):
    """
    This algorithm serves the longest available trail of rides, with arbitrary tie breaks
    :param graph: Describes the Start and end point of each request to be served
    :param timeLimit: Time allotted to serve requests
    :return: Number of rides served by this algorithm in the given amount of time
    """
    profit = 0
    t = 0
    deletedEdges = []

    # WHILE (There is still time left)
    while (t < timeLimit):
        # find the longest path in the remaining graph
        longestPath = graph.findLongestPath()

        # IF (Serving the entire longest trail will cause the server to go over the time limit)
        if (t + len(longestPath) - 1 > timeLimit):
            # -1 because len longestPath gives the number of vertices in the path not the number of edges
            # Serve requests until time has run out
            profit += timeLimit - t
            t += len(longestPath)
        # ELIF (Can serve all requests in the longest path
        elif (len(longestPath) != 0):
            profit += len(longestPath) - 1
            t += len(longestPath)
        else:
            t += 1

        # Keep track of the edges that were removed when trying to find the longest path
        if (len(longestPath) != 0):
            for i in range(len(longestPath) - 1):
                deletedEdges.append((longestPath[i], longestPath[i + 1]))
                graph.deleteEdge(longestPath[i], longestPath[i + 1])
    # This will add the edges back in a different order, but it is really the same graph
    for edge in deletedEdges:
        graph.addEdge(edge[0] + 1, edge[1] + 1)
    return profit


def twoChainAlgorithm(graph, timeLimit):
    """
    Algorithm to find the Max possible profit/ num rides served for a given graph and time limit
    :param graph: Describes the Start and end point of each request to be served
    :param timeLimit: Time allotted to serve requests
    :return: Number of rides served by 2 chain in the given amount of time
    """
    t = 0
    profit = 0
    currentVertex = -1
    currentAdjacentVertex = -1

    # here we check if there are any chains of two, if so we set
    # the current vertex to the beginning of one of these chains
    for vertex in graph.graph:
        for adjacentVertex in graph.graph[vertex]:
            if graph.hasAdjacentVertex(adjacentVertex):
                currentVertex = vertex
                currentAdjacentVertex = adjacentVertex

    # IF (there were no chains of 2 found)
    if (currentVertex == -1):
        # Look for any available request to serve
        for vertex in graph.graph:
            if graph.hasAdjacentVertex(vertex):
                currentVertex = vertex
                currentAdjacentVertex = graph.getAdjacentVertex(vertex)

    # IF (there are no edges in the graph)
    if (currentVertex == -1):
        return

    while (t < timeLimit):
        # IF (t=0, then serve the edge found above)
        if (t == 0):
            graph.deleteEdge(currentVertex, currentAdjacentVertex)
            currentVertex = currentAdjacentVertex
            t = t + 1
            profit = profit + 1
        # ELIF (There is a request starting at the current vertex, serve it)
        elif graph.hasAdjacentVertex(currentVertex):
            temp = graph.getAdjacentVertex(currentVertex)
            graph.deleteEdge(currentVertex, graph.getAdjacentVertex(currentVertex))
            currentVertex = temp
            t = t + 1
            profit = profit + 1
        # ELIF (There are at least 2 time units left) THEN (we have to choose another vertex to move to)
        elif (timeLimit - t >= 2):
            # print("PAUSE")

            # here we check if there are any chains of two, if so we set
            # the current vertex to the beginning of one of these chains
            currentVertex = -1
            for vertex in graph.graph:
                # print("vertex",vertex)
                for adjacentVertex in graph.graph[vertex]:
                    # print("adjacent vertex", adjacentVertex)
                    if graph.hasAdjacentVertex(adjacentVertex):
                        # print("There is a 2chain: ", vertex, adjacentVertex, graph.getAdjacentVertex(adjacentVertex))
                        currentVertex = vertex
                        currentAdjacentVertex = adjacentVertex

            # IF (no 2 chains were found) THEN look for any request to serve
            if (currentVertex == -1):
                for vertex in graph.graph:
                    if graph.hasAdjacentVertex(vertex):
                        currentVertex = vertex
                        currentAdjacentVertex = graph.getAdjacentVertex(vertex)

            # IF (there was a request to serve) THEN serve it and remove from the graph
            if (currentVertex != -1):
                graph.deleteEdge(currentVertex, currentAdjacentVertex)
                currentVertex = currentAdjacentVertex
                profit = profit + 1
            t = t + 2
        # ELSE (there are no requests to serve)  THEN let time pass
        else:
            t = t + 1
    return profit


if __name__ == '__main__':
    # #possibleRequestGraphs = generateRequestGraphs(5)#parameter is the number of nodes

    # # for graph in possibleRequestGraphs:
    # #     print(graph)
    # #print(list(possibleRequestGraphs))
    # #CREATE RANDOM GRAPHS
    # #2*numberOfVertices**2 This is the max number of edges
    # ################################################

    avgLtfCyclic = []
    avgLtfACyclic = []
    avgLtfRequests = []
    avgTwoChainRequests = []
    avgTwoChainCyclic = []
    avgTwoChainACyclic = []
    avgOptRequests = []
    ratioCyclicGraphs = []

    ### Parameters to play with ###
    # The number of graphs to have created and the algorithms tested on for each specified graph size (size=# requests)
    numGraphsPerSize = 10
    numberOfVertices = 100
    minNumEdges = 40
    maxNumEdges = 150
    numEdges = []
    worstCase = 1
    ID = 0
    T = 50

    # An attempt to write data out to csv :
    # c = csv.writer(open("Data.csv", "w"))
    # c.writerow(["NumEdges", "numVertices", "LTFACyclic", "LTFCyclic", "twoChainACyclic", "twoChainCyclic"])

    # FOR (Each number of edges in the range specified)
    # Note tqdm is just a way to make a progress bar appear since the loop will take a while to complete.
    for j in tqdm(range(minNumEdges, maxNumEdges)):

        # LTF = Longest Trail First, Init counters used to 0
        ltfTotal = 0
        ltfCyclicTotal = 0
        ltfACyclicTotal = 0
        longestAlgACyclic = 0
        longestAlg = 0

        twoChainTotal = 0
        twoChainCyclicTotal = 0
        twoChainACyclicTotal = 0
        twoChainCyclic = 0
        twoChainACyclic = 0

        optTotal = 0

        numGraphs = 0
        numACyclicGraphs = 0
        numCyclicGraphs = 0
        totalNumGraphs = 0


        # WHILE (The specified number of graphs havent been tested (ACyclic or Cyclic)
        # This condition could be played around with.  This ensures the same number of cyclic and acyclic graphs used
        while (numACyclicGraphs < numGraphsPerSize or numCyclicGraphs < numGraphsPerSize):
            # Create a random graph with specified num verticies, num edges, and id
            g = createRandomGraph(numberOfVertices, j, ID)
            # create copy to be altered
            f = copy.deepcopy(g)
            ID += 1
            # twoChain = twoChainAlgorithm(f,T)
            # twoChainTotal += twoChain
            totalNumGraphs += 1

            # IF (graph is cyclic)
            if (g.isCyclic()):
                # IF ( We haven't tested the specified number of cyclic graphs yet )
                if (numCyclicGraphs < numGraphsPerSize):
                    # Run each algorithm
                    twoChainCyclic = twoChainAlgorithm(f, T)
                    longestAlg = longestTrailAlgorithm(g, T)

                    # Add the results to the totals
                    ltfTotal += longestAlg
                    ltfCyclicTotal += longestAlg

                    twoChainTotal += twoChainCyclic
                    twoChainCyclicTotal += twoChainCyclic
                    numCyclicGraphs += 1
                    numGraphs += 1
            # ELIF (graph is Acyclic)
            elif (not g.isCyclic()):
                # IF ( We haven't tested the specified number of Acyclic graphs yet )
                if (numACyclicGraphs < numGraphsPerSize):
                    twoChainACyclic = twoChainAlgorithm(f, T)
                    longestAlgACyclic = longestTrailAlgorithm(g, T)

                    ltfTotal += longestAlgACyclic
                    ltfACyclicTotal += longestAlgACyclic

                    twoChainTotal += twoChainACyclic
                    twoChainACyclicTotal += twoChainACyclic
                    numACyclicGraphs += 1
                    numGraphs += 1
                    # Keep track of the worst case graph.
                    # If we run this enough and we never find a graph with a worse ratio than that
                    if (twoChainACyclic / longestAlgACyclic < worstCase):
                        worstCase = twoChainACyclic / longestAlgACyclic
                        worstCaseGraph = g
            # Write data out to csv
            # c.writerow([j, numberOfVertices, longestAlgACyclic, longestAlg, twoChainACyclic, twoChainCyclic])
            twoChainACyclic = 0
            longestAlgACyclic = 0
            twoChainCyclic = 0
            longestAlg = 0

        # Take note of the average of each alg for each size graph
        avgLtfRequests.append(ltfTotal / (numGraphs))
        avgLtfCyclic.append(ltfCyclicTotal / (numCyclicGraphs))
        avgLtfACyclic.append(ltfACyclicTotal / (numACyclicGraphs))
        avgTwoChainRequests.append(twoChainTotal / numGraphs)
        avgTwoChainCyclic.append(twoChainCyclicTotal / (numCyclicGraphs))
        avgTwoChainACyclic.append(twoChainACyclicTotal / (numACyclicGraphs))
        # avgOptRequests.append(optTotal/numGraphs)
        ratioCyclicGraphs.append(numCyclicGraphs / totalNumGraphs)
        numEdges.append(round(j / numberOfVertices, 3))

    print("WORST CASE : ")
    print(worstCase)

    # Plot the data
    plt.figure(1)
    plt.plot(numEdges, avgLtfCyclic, label='LTF Cyclic')
    plt.plot(numEdges, avgLtfACyclic, label='LTF ACyclic')
    plt.plot(numEdges, avgLtfRequests, label='LTF')
    plt.plot(numEdges, avgTwoChainRequests, label='2 Chain')
    plt.plot(numEdges, avgTwoChainCyclic, label='2 Chain Cyclic')
    plt.plot(numEdges, avgTwoChainACyclic, label='2 Chain ACyclic')
    plt.legend()
    plt.xlabel("Requests/locations in Input Graph")
    plt.ylabel("Average number of requests served")

    # What other than the time limit could we use for this upper bound line??
    plt.axhline(y=T, xmin=0, xmax=1.5, linewidth=2, color='k')

    plt.show()
    # plt.savefig()

    # The following block adds a table of averages to the top of the graph
    ##################################
    # ratio= np.divide(avgTwoChainRequests,avgLtfRequests)
    # colLabels = []
    # ATCR = [] #average two chain requests rounded for table
    # ALTFR = [] #average ltf requests rounded for table
    # R = []
    # i=0

    # only want a certain number of elements in table so you can read it
    # while (i< len(avgTwoChainRequests)):
    #     if (i%30==0):
    #         ALTFR.append(round(avgLtfRequests[i],3))
    #         ATCR.append(round(avgTwoChainRequests[i],3))
    #         R.append(round(ratio[i],3))
    #     i+=1

    # tableData = np.array([ATCR,ALTFR,R])

    # rowLabels = ( 'Two Chain', 'LTF', 'Ratio')

    # table = plt.table(cellText=tableData,rowLabels = rowLabels, loc='top')
    # plt.show()
    # plt.figure(2)
    # #plt.plot(numEdges, ratioCyclicGraphs, label = 'Ratio of Cyclic Graphs')
    # plt.legend()
    # plt.xlabel("Requests in Input Graph")
    # plt.ylabel("Ratio of Cyclic Graphs")

    # plt.table(cellText = avgTwoChainRequests)
    # Show the plot
    ##################################



# TEST TOP SORT- Works for cycles? When is an incorrect answer given?
# T=7
# g=Graph(8,0)
# g.addEdge(1,2)
# g.addEdge(2,3)
# g.addEdge(3,1)
# g.addEdge(4,2)
# print(g)
# print(g.topologicalSort())
# print(longestTrailAlgorithm(g,4))




# x = np.linspace(0, 2, 100)
# plt.plot(x, x, label='linear')
# plt.plot(x, x**2, label='quadratic')
# plt.plot(x, x**3, label='cubic')
# plt.xlabel('x label')
# plt.ylabel('y label')
# plt.title("Simple Plot")
# plt.legend()
# plt.show()
###################################################
#    T=7
#    g=Graph(8,0)
#    g.addEdge(1,2)
#    g.addEdge(4,5)
#    g.addEdge(5,1)
#    g.addEdge(5,2)
#    g.addEdge(5,7)
#    g.addEdge(6,4)
#    g.addEdge(6,5)
#    g.addEdge(6,7)
#    #twoChainAlgorithm(g, 7)

#    # print(g.isAdjacent(0))
#    # print(g.getAdjacentVertex(0))

# # print("opt",opt(g,T))
#    f=copy.deepcopy(g)
#    print("Longest Chain", longestTrailAlgorithm(g,T))
#    print("profit",twoChainAlgorithm(f, 7))


# g.addEdge(3,1)
# g.addEdge(4,1)
# g.addEdge(4,2)
# g.addEdge(7,8)
# g.addEdge(2,7)


# numberOfVertices = 10
# for k in range(2*numberOfVertices**2):
#     T=k+1
#     for j in range(2*numberOfVertices**2):
#         for i in range(10):
#             ID = j+i

#             g = createRandomGraph(numberOfVertices,j, ID)
#             #print("here is graph g: ", g)
#             if g.isCyclic():
#                 pass
#             else:
#                 optimal=opt(g,T)
#                 longestAlg=longestTrailAlgorithm(g,T)
#                 if longestAlg < optimal:
#                     print(g)






