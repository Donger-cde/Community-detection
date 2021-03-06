# Community detetction
## Girvan-Newman algorithm 
Implements the Girvan-Newman algorithm and outputs the resultant hierarchical decomposition of the network. If there are multiple edges have the same highest betweenness score, remove all of them simultaneously.
## Modularity
Implements the calculation of modularity, and outputs the corresponding cluster structure.
# Input file
input.txt
# Environment
Python3 + PyCharm
# Dependencies
networkx  
copy  
communities.py  
# Main steps of the program
1. Read the input file into a matrix
2. Convert the matrix into a graph using networkx
3. Calculate the betweenness of each edge
4. Remove the edges with highest betweenness score
5. Connected components are communities
6. Gives a hierarchical decomposition of the network
7. Calculate Modularity
8. Repeat the step 3 to 7 until no edges left in the graph
9. The optimal structure should be the set of communities that have the highest modularity
