import json
from src.Models.tmuModels import *
from src.tmuRepository import *
import os
from igraph import *
from bidi.algorithm import get_display
from arabic_reshaper import reshape
from src.clean import clean_pattern_for_irandoc
_repository = TmuRepository()

row=_repository.get_all_tags()
# df = pd.Daframe


row=[
    {'first':clean_pattern_for_irandoc(x['first']),
     'second':clean_pattern_for_irandoc(x['second'])}
    for x in row]

nodes=list(set([x['first'] for x in row]))
edges=[(x['first'],x['second']) for x in row]


g = Graph()
g.add_vertices(nodes)
g.add_edges(edges)
g.vs.select(_degree=0).delete()
# g.vs['label'] = [get_display(reshape(label)) for label in g.vs['name']]
g.vs['label'] = g.vs['name']
degree = g.degree()
visual_style = {}
visual_style["edge_curved"] = False
visual_style["vertex_size"] = [int(x)/max(degree)+20 for x in degree]

visual_style["bbox"] = (2400, 1800)
# visual_style["margin"] = 100
# visual_style["vertex_label"] = g.vs['label']

visual_style["layout"] = g.layout_fruchterman_reingold()

g.simplify()

# plot(g, **visual_style)
g.write_graphml('all_irandoc_label_same_name.graphml')