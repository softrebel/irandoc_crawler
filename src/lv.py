from igraph import *
import louvain
g = Graph.Read_GraphML('ged_irandoc_one_mode_tf_1385_1389.graphml')
print(g.summary())
g.vs.select(_degree=0).delete()
g.vs.select(_degree=1).delete()
print(g.summary())
partition = louvain.find_partition(g, louvain.CPMVertexPartition, resolution_parameter = 0.05)
degree = g.degree()

# g['name']=[]
visual_style = {}
visual_style["edge_curved"] = False
visual_style["margin"] = 100
visual_style["vertex_size"] = [int(x)+20 for x in degree]
visual_style['vertex_label']=None
visual_style['vertex_label']=g.vs['label']
visual_style["bbox"] = (2400, 1800)

visual_style["layout"] = g.layout_fruchterman_reingold()
# plot(partition, 'louvain.svg',**visual_style)
plot(partition, **visual_style)