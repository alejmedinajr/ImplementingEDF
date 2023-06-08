# ImplementingEDF
This repository is dedicated to Dial-a-Ride (DARP) Experimentation using the python programming language. The specific instance of DARP that is being evaluated is an algorithm that serves requests with earliest deadlines first (EDF). There is also a brute force algorihtm that finds an optimal solution by generating permutations of all possible orderings of the requests, and serving them in order until the overall time limit is reached. There are also visualization functions that are used to display the graph that represents an instance of requests, as well as a function that displays the solution of both algorithms for an instance. The results of this evaluation will be presented in form of a poster at the [2023 Richard Tapia Confernece](https://tapiaconference.cmd-it.org/attend/presentation/?id=post125&sess=sess300) in Dallas, Texas.   

## Requirements
The following requirments are needed to run the code in this repository:  
`cycler 0.10.0`  
`kiwisolver 1.2.0`  
`matplotlib 3.2.1`  
`numpy 1.20.0`  
`pyparsing 2.4.7`  
`python-dateutil 2.8.1`  
`six 1.14.0`  
`tqdm 4.45.0`  
`networkx 3.1.0`  

## Acknowledgement

The following files contain parts of existing code from Dial-A-Ride Experimentation by Patrick Davis 19':

`Graph.py` - The underlying structure from the graph is mostly based on the code from the existing graph file. The main difference is that our Graph.py file focuses on the edges, which takes form of a collection that is used rather than the normal way edges were used in the existing code. Additionally, there are several helper functions that were added. This includes the visualization functions, which are used to visualize the graph using networkx. The graph object itself also has deadlines and release times, which were not existing in the graph structure from the existing code. 

`GraphGenerator.py` - The graph generators are mostly the same, but there are slight tweaks and new additions. For instance, the existing code did not implement release times or deadlines, so this was added. Moreover, there are other graph generating functions, such as the function that takes an input file and generates a graph based on the text. This function was not in the existing code, and was made from scratch.

The orignal files from Patrick Davis are in the folder named Code in `Python from a different DARP algorithm`. 
## Contributors
-[Alejandro Medina](https://github.com/alejmedinajr)  
-[Dr. Barbara Anthony](https://github.com/anthonybsouthwestern)
