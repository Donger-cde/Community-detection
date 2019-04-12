import networkx as nx
import copy
import matplotlib.pyplot as plt

inputfile = 'input.txt'


# read input.txt file to a matrix
def read_input(inputfilepath):
    matrix = []
    with open(inputfilepath, 'r') as file_to_read:
        number = int(file_to_read.readline())
        for i in range(number):
            line = file_to_read.readline().strip('\n')
            line = list(map(int, line.split(' ')))
            matrix.append(line)
    return matrix


# convert matrix to networkx graph structure
def build_graph(matrix):
    G = nx.Graph()
    G.add_nodes_from([0 for i in range(len(matrix))])
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                G.add_edge(i, j)
    return G


def work_up(betweenness, queue, workup, shortestpaths):
    flow = {}
    path = {}
    for key in shortestpaths.keys():
        path[key] = 1
    # walk up th graph
    while queue:
        currentnode = queue.pop(len(queue)-1)
        if currentnode in workup.keys():
            for parentnode in workup[currentnode]:
                # split fraction of each edge
                coefficient = shortestpaths[parentnode] / shortestpaths[currentnode]
                a = path[currentnode] * coefficient
                flow[(currentnode, parentnode)] = a
                path[parentnode] = path[parentnode] + flow[(currentnode, parentnode)]
                if (currentnode, parentnode) in betweenness.keys():
                    betweenness[(currentnode, parentnode)] = betweenness[(currentnode, parentnode)] + flow[(currentnode, parentnode)]
                elif (parentnode, currentnode) in betweenness.keys():
                    betweenness[(parentnode, currentnode)] = betweenness[(parentnode, currentnode)] + flow[(currentnode, parentnode)]
    return betweenness


# calculate the betweenness and return the betweenness of every edges
def get_betweenness(graph):
    # define the betweenness {(1,2): 1.33}
    betweenness = dict.fromkeys(graph.edges(), 0.0)
    # iterate all nodes in the graph
    for node in graph.nodes:
        level = {node: 0}
        seen = [node]
        queue = [node]
        shortestpaths = {node: 1}
        # store the parents node of a node
        workup = {}
        # bfs
        while queue:
            currentnode = queue.pop(0)
            for subnode in graph[currentnode]:
                # if it's the first time seen this node
                if subnode not in seen:
                    queue.append(subnode)
                    level[subnode] = level[currentnode]+1
                    shortestpaths[subnode] = shortestpaths[currentnode]
                    seen.append(subnode)
                    workup[subnode] = [currentnode]
                # if it's not the first time seen this node and this node is in the next level
                elif level[subnode] == level[currentnode]+1:
                    shortestpaths[subnode] = shortestpaths[subnode]+shortestpaths[currentnode]
                    workup[subnode].append(currentnode)

        # Sum up the flow values to get the betweenness
        # working up the tree to calculate flow
        betweenness = work_up(betweenness, seen, workup, shortestpaths)
    return betweenness


# accumulate the betweenness
def acc_betweenness(betweenness, betweenness_temp):
    # k represents the edge, v is the value of betweenness
    for k, v in betweenness_temp.items():
        # n1,n2 represent two nodes of a edge
        n1, n2 = list(k)
        # since the graph is the undirected graph, so (n1,n2) and (n2,n1) is the same edge
        if (n1, n2) in betweenness.keys():
            betweenness[(n1, n2)] += v/2
        elif (n2, n1) in betweenness.keys():
            betweenness[(n2, n1)] += v/2
        else:
            betweenness[k] = v/2
    return betweenness


def girvan_newman_algorithm(graph):
    # Girvan_Newman_algorithm:
    # Calculate the betweenness of each edge and remove the edges with highest betweenness score
    # Repaet this process until no edges in the graph


    # store the original graph
    origingraph = copy.deepcopy(graph)
    # total edges of the original graph
    m = origingraph.number_of_edges()
    decomposition = []
    modularity = []
    # store the connected components in a graph
    subgraph = [graph]

    # repaet the process until no edges in the graph
    while graph.number_of_edges() != 0:
        # Calculate betweenness of edges
        betweenness = dict.fromkeys(graph.edges(), 0.0)

        # if there are more than one unconnected components
        # calculate their betweenness respectively，then sum
        for subgraphi in subgraph:
            # calculate the betweenness of each community
            betweenness_temp = get_betweenness(subgraphi)
            # accumulate the betweenness to get the betweenness of whole graph
            betweenness = acc_betweenness(betweenness, betweenness_temp)

        # Remove the edge with the highest betweenness
        highest = max(betweenness.values())
        removelist = []
        for edge, betw in betweenness.items():
            if betw == highest:
                # (if two or more edges tie for highest score, remove all of them)
                removelist.append(edge)
        graph.remove_edges_from(removelist)
        # Connected components are communities
        communities =list(nx.connected_components(graph))
        subgraph = nx.connected_component_subgraphs(graph)

        # Gives a hierarchical decomposition of the network
        decomposition.append(communities)

        # Calculate Modularity
        q = 0
        for group in communities:
            for nodei in group:
                for nodej in group:
                    ki = origingraph.degree(nodei)
                    kj = origingraph.degree(nodej)
                    aij = 0
                    if graph.has_edge(nodei, nodej) is True:
                        aij = 1
                    else:
                        aij = 0
                    q = aij - (ki*kj)/(m*2) +q
        q = q/(2*m)
        modularity.append(q)
    return decomposition, modularity


def main():
    # read the input.txt data from the txt file and store in a matrix
    data = read_input(inputfile)
    # convert the matrix to a networkx graph
    graph = build_graph(data)

    # nx.draw_networkx(graph)
    # plt.show()

    # Implements the Girvan - Newman algorithm
    # and outputs the resultant hierarchical decomposition of the network.
    decomposition, modularity = girvan_newman_algorithm(graph)

    # output question1
    print('network decomposition:')
    for i in range(len(decomposition)):
        result = str(decomposition[i]).replace('[', '(').replace(']', ')').replace('{', '[').replace('}', ']')
        print(result)

    # output question2
    # if the modularity is max， this is the optimal structure
    maxm = modularity[0]
    optimal = 0
    for i in range(len(modularity)):
        m = modularity[i]
        print(str(len(decomposition[i]))+' clusters: modularity '+str(m))
        if m > maxm:
            maxm = m
            optimal = i

    print('optimal structure: ' +
          str(decomposition[optimal]).replace('[', '(').replace(']', ')').replace('{', '[').replace('}', ']'))


if __name__ == "__main__":

    main()

