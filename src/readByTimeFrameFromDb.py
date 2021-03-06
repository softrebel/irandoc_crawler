import json
from src.Models.tmuModels import *
from src.tmuRepository import *
import os
from igraph import *
from bidi.algorithm import get_display
from arabic_reshaper import reshape
from src.clean import clean_pattern_for_irandoc

_repository = TmuRepository()

'''
برای دکتر اقدسی سال های 1300 و 1369 و 1372 هرکدام فقط یک مقاله چاپ شده است.
'''
name='محمد اقدسی'
time_frames = [
        ['1300',
         '1369',
         '1372'],
        ['1373',
         '1374',
         '1375',
         '1376',
         '1377'],
        ['1380',
         '1381',
         '1382',
         '1383',
         '1384'],
        ['1385',
         '1386',
         '1387',
         '1388',
         '1389'],
        ['1390',
         '1391',
         '1392',
         '1393',
         '1394'],
        ['1395',
         '1396',
         '1397',
         '1398',
         '1399']
]

for time_frame in time_frames:
    print(time_frame)
    row = _repository.get_article_tags_by_time_frame(name,time_frame)

    # df = pd.Daframe
    def graph_statistics(self):
        print("Number of vertices:", self.vcount())
        print("Number of edges:", self.ecount())
        print("Density of the graph:", 2 * self.ecount() / (self.vcount() * (self.vcount() - 1)))
        degrees = self.degree()
        print("Average degree:", sum(degrees) / self.vcount())
        print("Minimum degree:", min(degrees))
        print("Maximum degree:", max(degrees))
        print("Vertex ID with the maximum degree:", degrees.index(max(degrees)))
        print("Diameter of the graph:", self.diameter())


    Graph.graph_statistics = graph_statistics

    row = [
        {'first': clean_pattern_for_irandoc(x['tag_name']),
         # 'second': clean_pattern_for_irandoc(x['researcher_name']),
         'second':x['uuid'],
         'pure': x['tag_name']}
        for x in row]

    first = list(set([x['first'] for x in row if x['first'] != '']))

    second = list(set([x['second'] for x in row]))

    nodes = [*first, *second]
    edges = [(x['first'], x['second']) for x in row if x['first'] != '']

    g = Graph()
    g.add_vertices(first, attributes={'type': 0})
    g.add_vertices(second, attributes={'type': 1})
    g.add_edges(edges)

    h,z=g.bipartite_projection()
    # g.vs.select(_degree=0).delete()
    # g.vs.select(_degree=1).delete()


    # g.vs['label'] = [get_display(reshape(label)) for label in g.vs['name']]
    h.vs['label'] = h.vs['name']

    degree = h.degree()
    visual_style = {}
    visual_style["edge_curved"] = False
    visual_style["vertex_size"] = [int(x) / max(degree) + 20 for x in degree]

    visual_style["bbox"] = (2400, 1800)
    # visual_style["margin"] = 100
    # visual_style["vertex_label"] = h.vs['label']

    # visual_style["layout"] = h.layout_sugiyama()

    # h.simplify()

    # plot(g, **visual_style)
    h.write_graphml(f'ged_irandoc_one_mode_tf_{time_frame[0]}_{time_frame[-1]}.graphml')
    h.graph_statistics()
