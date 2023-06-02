import csv
from Graph import Graph
import GraphGenerator as gg
import glob
from OPT import opt
from EDF import edf
import random

def reportResults(optSolution, edfSolution, writer, file):
    """
    This function provides a way to write flagged test cases to csv. The reported solutions for OPT and EDF are 
    compared and different flags can be thrown depending on both solutions in comparison to each other.
    The flags can be changed as desired, but this is mainly used when running test cases.
    :param optSolution: The reported solution given by the OPT algorithm for the specific test case file instance.
    :param edfSolution: The reported solution given by the EDF algorithm for the specific test case file instance.
    :param writer: The writer that is used to actually perform the function of writing to the specified csv file.
    :param file: The current test case file that was run, if there was something worthy of reporting in this test case, the file needs to be reported for easy user verification.
    """
    if edfSolution == 2*optSolution: # need to report when edf solution is equal to 2*opt solution
        writer.writerow(["|EDF| = 2*|OPT|", file, optSolution, edfSolution])
    
    if edfSolution != optSolution: # need to report when the two solutions are not the same
        writer.writerow(["|EDF| differs from |OPT|", file, optSolution, edfSolution])

    if edfSolution > optSolution: # need to report when edf does better than opt (this should never happen)
        writer.writerow(["|EDF| > |OPT|", file, optSolution, edfSolution])

    if 2*edfSolution < optSolution: # need to report when edf does has a solution more than twice as less than opt (should also never happen)
        writer.writerow(["|EDF| < 2*|OPT|", file, optSolution, edfSolution])


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
            graphInfo = GG.generateGraphFromFile(file) # function to generate the graph from the specified file
            graph = graphInfo[0] # the graph is at index 0
            timeLimit = Graph.getTimeLimit(graph, graphInfo[1]) # the timeLimit is at index 1
            #print(timeLimit)
            Graph.visualizeGraph(graph, timeLimit, file) # save visual of the graph prior to any algorithms being run
            optInfo = opt(graph, timeLimit) # optInfo contains everything returned by opt algorithm
            print("opt: " + str(optInfo[0])+ " with timeLimit: " + str(timeLimit)) # display opt result to console
            Graph.visualizeGraphSolution(graph, timeLimit, optInfo[1], optInfo[2], "OPT" , file) # create visual of opt result and store it in test suite directory
            edfInfo = edf(graph, timeLimit) # edge info contains everything returned by edf algorithm
            print("edf: " + str(edfInfo[0])+ " with timeLimit: " + str(timeLimit)) # display edf result to console
            Graph.visualizeGraphSolution(graph, timeLimit, edfInfo[1], edfInfo[2], "EDF" , file) # create visual of edf result and store it in test suite directory
            
            reportResults(optInfo[0], edfInfo[0], writer, file)


def runRandomTestCases(minNodes, maxNodes, minEdges, maxEdges, minTimelimit, maxTimelimit, f, p, min, max, graphsGenerated, testFolder, saveTo):
    
    with open(testFolder + " - Report.csv", 'w', newline='') as report: # create a csv report of the results. This is where any flagged test cases will be reported
        writer = csv.writer(report) # create the writer for the csv file
        fields = ["flag", "testcase", "OPT", "EDF"] # fields of what will be written to the csv
        writer.writerow(fields) # writing the first row to csv file - contains all the fields
    
        numberOfNodes = random.randint(minNodes, maxNodes)
        numberOfEdges = random.randint(minEdges, maxEdges)
        timelimit = random.randint(minTimelimit, maxTimelimit)
        id = 0 # the id that will be used for the file saved of the randomly created graph
        for i in range(graphsGenerated):
            file = testFolder + "\\" + saveTo + "_" + str(id) 
            graph = gg.createRandomGraphWithDeadlines(numberOfNodes, numberOfEdges, id, f, p, min, max)
            Graph.visualizeGraph(graph, timelimit, file) # save visual of the graph prior to any algorithms being run
            optInfo = opt(graph, timelimit) # optInfo contains everything returned by opt algorithm
            print("opt: " + str(optInfo[0])+ " with timeLimit: " + str(timelimit)) # display opt result to console
            Graph.visualizeGraphSolution(graph, timelimit, optInfo[1], optInfo[2], "OPT" , file) # create visual of opt result and store it in test suite directory
            edfInfo = edf(graph, timelimit) # edge info contains everything returned by edf algorithm
            print("edf: " + str(edfInfo[0])+ " with timeLimit: " + str(timelimit)) # display edf result to console
            Graph.visualizeGraphSolution(graph, timelimit, edfInfo[1], edfInfo[2], "EDF" , file) # create visual of edf result and store it in test suite directory
            
            reportResults(optInfo[0], edfInfo[0], writer, file)
            id += 1


if __name__ == '__main__':    
    # To run the test cases, the lines until the next empty line need to be uncommented.
    #testFolder = "TestCases"
    #testFolder = "TestCases\\Archived Test Cases"
    #runTestCases(testFolder)
    
    #testFolder = "TestCases"
    #runTestCases(testFolder)
    
    testFolder = "TestCases\\Randomly Generated Test Cases\\batch1"
    runRandomTestCases(3, 15, 3, 15, 5, 50, 0.75, 0.75, 2, 30, 1000, testFolder, "randomGeneratedTestCasesBatch1")
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

        