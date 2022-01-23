import json
from src.Models.tmuModels import *
from src.tmuRepository import *
import os
from igraph import *
from bidi.algorithm import get_display
from arabic_reshaper import reshape
from src.clean import clean_pattern_for_irandoc
_repository = TmuRepository()

row=_repository.get_article_tags()
# df = pd.Daframe
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




row=[
    {'first':clean_pattern_for_irandoc(x['tag_name']),
     'second':clean_pattern_for_irandoc(x['researcher_name']),
     'pure':x['tag_name']}
    for x in row]

first=list(set([x['first'] for x in row if x['first']!='']))

second=list(set([x['second'] for x in row]))

nodes=[*first,*second]
edges=[(x['first'],x['second']) for x in row if x['first']!='' ]


g=Graph()
g.add_vertices(first,attributes={'type':0})
g.add_vertices(second,attributes={'type':1})
g.add_edges(edges)
# g.vs.select(_degree=0).delete()
# g.vs.select(_degree=1).delete()



# g.vs['label'] = [get_display(reshape(label)) for label in g.vs['name']]
g.vs['label'] = g.vs['name']

degree = g.degree()
visual_style = {}
visual_style["edge_curved"] = False
visual_style["vertex_size"] = [int(x)/max(degree)+20 for x in degree]

visual_style["bbox"] = (2400, 1800)
# visual_style["margin"] = 100
# visual_style["vertex_label"] = g.vs['label']

# visual_style["layout"] = g.layout_sugiyama()

# g.simplify()

# plot(g, **visual_style)
g.write_graphml('all_irandoc_two_mode.graphml')
g.graph_statistics()


