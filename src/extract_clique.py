import igraph as ig
from igraph import *
from itertools import combinations
keywords = Graph.Read_GraphML('all_irandoc_label_same_name.graphml')
keywords.vs.select(_degree=0).delete()
keywords.vs.select(_degree=1).delete()
cliques = keywords.maximal_cliques(min=3)
nodes=[]

def graph_statistics(self):
    print("Number of vertices:", self.vcount())
    print("Number of edges:", self.ecount())
    print("Density of the graph:", 2 * self.ecount() / (self.vcount() * (self.vcount() - 1)))
    degrees = self.degree()
    print("Average degree:", sum(degrees) / self.vcount())
    print("Maximum degree:", max(degrees))
    print("Vertex ID with the maximum degree:", degrees.index(max(degrees)))
    print("Diameter of the graph:", self.diameter())
Graph.graph_statistics=graph_statistics

g=Graph.Read_GraphML('all_irandoc_two_mode.graphml')



for clique in cliques:
    degrees=[keywords.vs[x].degree() for x in clique]
    idx=degrees.index(max(degrees))
    if clique[idx] not in nodes:
        nodes.append(clique[idx])
    # for node in clique:
    #     if node not in nodes:
    #         nodes.append(node)
    #         break
cliques_graph=Graph.subgraph(keywords,nodes)
cliques_graph.vs.select(_degree=0).delete()
cliques_graph.vs.select(_degree=1).delete()
cliques_graph.write_graphml('cliques_graph.graphml')
def cliqsBySize(cliques):
    cqsizes = {}
    for cx in cliques:
        cxsz = len(cx)  # Size of the clique
        cqsizes[cxsz] = cqsizes.get(cxsz, 0) + 1
    return cqsizes
print("Number of Nodes in Keywords graph is:",keywords.vcount())
print("Number of Edges in Keywords graph is:",keywords.ecount())
print("Number of Nodes in Cliques graph is:",cliques_graph.vcount())
print("Number of Edges in Cliques graph is:",cliques_graph.ecount())
for i in cliqsBySize(cliques):
    print('Number of Cliques of size',i,'is:',cliqsBySize(cliques)[i])




keywords.graph_statistics()
degree=keywords.degree()

import matplotlib.pyplot as plt
plt.hist(degree,range=(0,150),bins=10)
# plt.show()
plt.savefig('test.png')




