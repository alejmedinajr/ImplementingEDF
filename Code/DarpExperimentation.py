import csv
from Graph import Graph
import GraphGenerator as gg
import glob
from OPT import opt
from EDF import edf
import random

def reportResults(optSolution, optTime, edfSolution, edfTime, writer, file):
    """
    This function provides a way to write flagged test cases to csv. The reported solutions for OPT and EDF are 
    compared and different flags can be thrown depending on both solutions in comparison to each other.
    The flags can be changed as desired, but this is mainly used when running test cases.
    :param optSolution: The reported solution given by the OPT algorithm for the specific test case file instance.
    :param edfSolution: The reported solution given by the EDF algorithm for the specific test case file instance.
    :param writer: The writer that is used to actually perform the function of writing to the specified csv file.
    :param file: The current test case file that was run, if there was something worthy of reporting in this test case, the file needs to be reported for easy user verification.
    """
    if edfSolution == optSolution: # record the solutions for every test case. If they are not equal, then a special flag will be written depending on the situation
        writer.writerow(["|EDF| = |OPT|", file, optSolution, optTime, edfSolution, edfSolution])
    
    else: 
        if edfSolution == 2*optSolution: # need to report when edf solution is equal to 2*opt solution
            writer.writerow(["|EDF| = 2*|OPT|", file, optSolution, optTime, edfSolution, edfSolution])

        elif edfSolution > optSolution: # need to report when edf does better than opt (this should never happen)
            writer.writerow(["|EDF| > |OPT|", file, optSolution, optTime, edfSolution, edfSolution])

        elif 2*edfSolution < optSolution: # need to report when edf does has a solution more than twice as less than opt (should also never happen)
            writer.writerow(["|EDF| < 2*|OPT|", file, optSolution, optTime, edfSolution, edfSolution])

        else: # need to report when the two solutions are not the same
            writer.writerow(["|EDF| differs from |OPT|", file, optSolution, optTime, edfSolution, edfSolution])

def runTestCases(testFolder):
    """
    This function provides a way to run test cases from a specific directory. The visual of each graph is saved as a png file and shown to the user.
    :param testFolder: Describes the root folder where the test cases are.
    """
    with open(testFolder + " - Report.csv", 'w', newline='') as report: # create a csv report of the results. This is where any flagged test cases will be reported
        writer = csv.writer(report) # create the writer for the csv file
        fields = ["flag", "testcase", "OPT", "EDF"] # fields of what will be written to the csv
        writer.writerow(fields) # writing the first row to csv file - contains all the fields
    
        for file in glob.glob(testFolder + "\\test*.txt"): # find every file in the specified folder that is a test file (test#.txt)
            print("Running: " + file) # print statement to let the user know which file test case is currently running
            graphInfo = gg.generateGraphFromFile(file) # function to generate the graph from the specified file
            graph = graphInfo[0] # the graph is at index 0
            timeLimit = graphInfo[1] # the timeLimit is at index 1
            Graph.visualizeGraph(graph, timeLimit, file) # save visual of the graph prior to any algorithms being run
            optInfo = opt(graph, timeLimit) # optInfo contains everything returned by opt algorithm
            print("opt: " + str(optInfo[0])+ " with timeLimit: " + str(timeLimit)) # display opt result to console
            Graph.visualizeGraphSolution(graph, timeLimit, optInfo[1], optInfo[2], "OPT" , file) # create visual of opt result and store it in test suite directory
            edfInfo = edf(graph, timeLimit) # edge info contains everything returned by edf algorithm
            print("edf: " + str(edfInfo[0])+ " with timeLimit: " + str(timeLimit)) # display edf result to console
            Graph.visualizeGraphSolution(graph, timeLimit, edfInfo[1], edfInfo[2], "EDF" , file) # create visual of edf result and store it in test suite directory
            
            reportResults(optInfo[0], optInfo[3], edfInfo[0], edfInfo[3], writer, file) # write any possible flags from results


def runRandomTestCases(minNodes, maxNodes, minEdges, maxEdges, minTimelimit, maxTimelimit, f, p, min, max, graphsGenerated, testFolder, saveTo):
    """
    This function provides a way to run test cases on randomly generated graphs. All results are saved to specified directory.
    :param minNodes: The lower bound on the range of possible number of nodes for randomly generated graph
    :param maxNodes: The upper bound on the range of possible number of nodes for randomly generated graph
    :param minEdges: The lower bound on the range of possible number of edges for randomly generated graph
    :param maxEdges: The upper bound on the range of possible number of edges for randomly generated graph
    :param minTimelimit: The lower bound on the range of possible timelimit values
    :param maxTimelimit: The upper bound on the range of possible timelimit values
    :param f: The frequency of bidirectional edges. If f = 0, no bidirectional edges will be allowed, otherwise the value of f represents the frequency of bidirectional edges.
    :param p: The percent of edges that will have deadlines (we only want a p percent of edges to be requests)
    :param min: The minimum value that a deadline could be
    :param max: The maximum value that a deadline could be
    :param graphsGenerated: The total number of random graphs that will be generated
    :param testFolder: The parent folder where the output files should be saved to
    :param saveTo: The name the file should have as it is saved
    """
    with open(testFolder + " - Report.csv", 'w', newline='') as report: # create a csv report of the results. This is where any flagged test cases will be reported
        writer = csv.writer(report) # create the writer for the csv file
        fields = ["flag", "testcase", "OPT", "OPT Time (s)", "EDF", "EDF Time (s)"] # fields of what will be written to the csv
        writer.writerow(fields) # writing the first row to csv file - contains all the fields
    
        id = 0 # the id that will be used for the file saved of the randomly created graph
        for i in range(graphsGenerated):
            numberOfNodes = random.randint(minNodes, maxNodes) # number of nodes for random graph will be [minNodes, maxNodes]
            numberOfEdges = random.randint(minEdges, maxEdges) # number of edges for random graph will be [minEdges, maxEdges]
            timelimit = random.randint(minTimelimit, maxTimelimit) # the timelimit is also random [minTimelimit, maxTimelimit]
            
            file = testFolder + "\\" + saveTo + "_" + str(id) 
            graph = gg.createRandomGraphWithDeadlines(numberOfNodes, numberOfEdges, id, f, p, min, max)
            Graph.visualizeGraph(graph, timelimit, file) # save visual of the graph prior to any algorithms being run

            optInfo = opt(graph, timelimit) # optInfo contains everything returned by opt algorithm
            print("opt: " + str(optInfo[0])+ " with timeLimit: " + str(timelimit)) # display opt result to console
            if optInfo[0] > 0:
                Graph.visualizeGraphSolution(graph, timelimit, optInfo[1], optInfo[2], "OPT" , file) # create visual of opt result and store it in test suite directory
            edfInfo = edf(graph, timelimit) # edge info contains everything returned by edf algorithm
            print("edf: " + str(edfInfo[0])+ " with timeLimit: " + str(timelimit)) # display edf result to console
            if edfInfo[0] > 0:
                Graph.visualizeGraphSolution(graph, timelimit, edfInfo[1], edfInfo[2], "EDF" , file) # create visual of edf result and store it in test suite directory
            
            reportResults(optInfo[0], optInfo[3], edfInfo[0], edfInfo[3], writer, file) # write any possible flags from results
            id += 1 # the id of the graph needs to be increased by 1


if __name__ == '__main__':    
    inputTestSuite = ["TestCases\\Archived Test Cases", "TestCases"] # collection of known existing test suits for grpah input files
    #inputTestSuite = ["TestCases\\Archived Test Cases"] # collection of known existing test suits for grpah input files
    
    randomTestSuite = ["TestCases\\Randomly Generated Test Cases\\batch1", "TestCases\\Randomly Generated Test Cases\\batch2", "TestCases\\Randomly Generated Test Cases\\batch3"] # collection of where the random generated batches should be saved
    
    largerRandomTestSuite = ["TestCases\\Randomly Generated Test Cases\\batch4", "TestCases\\Randomly Generated Test Cases\\batch5", "TestCases\\Randomly Generated Test Cases\\batch6"] # collection of where the random generated batches should be saved
    #randomTestSuite = ["TestCases\\Randomly Generated Test Cases\\batch1"]
    i = 1 # the batch numbe rneeds to be incremented so the batches are distinct
    #for testFolder in randomTestSuite:
        #runRandomTestCases(14, 15, 3, 9, 10, 60, 0.8, 1, 5, 30, 500, testFolder, "randomGeneratedTestCasesBatch" + str(i)) # run the random tests on randomly generated graphs
        #i +=1 # increase to signify the next batch

    #for testFolder in inputTestSuite: # run all input test suite files
    #    runTestCases(testFolder)

    i = 4
    for testFolder in largerRandomTestSuite:
        runRandomTestCases(60, 60, 20, 20, 15, 45, 0.8, 1, 5, 30, 100, testFolder, "randomGeneratedTestCasesBatch" + str(i)) # run the random tests on randomly generated graphs
        i += 1 # increase to signify the next batch
