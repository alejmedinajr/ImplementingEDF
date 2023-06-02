from Graph import Graph

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

    while currentTime < timeLimit and len(requests) + len(availableRequests) > 0 and windowSize < timeLimit: # the algorithm ends when the time limit is reached
      
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
                
    #print(timeServed)
    #print("REQUESTS SERVED: " + str(requestsServed)) # nice debugging way to see which requests were served before the final solution is returned            
    return ridesServed, timeServed, requestsServed # return the number of requests that were served by the EDF algorithm