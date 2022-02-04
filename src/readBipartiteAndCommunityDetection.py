from src.tmuRepository import *
from igraph import Graph, plot
from bidi.algorithm import get_display
from arabic_reshaper import reshape
import louvain
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
_repository = TmuRepository()


import click
lang = LANG

input_prompt= click.style(lang['input_file'],
                             bold=True, bg='green', fg='yellow')

@click.group()
def cli():
    pass

@cli.command()
@click.option('-i', '--input', default='output_bipartite.graphml', type=str, prompt=input_prompt,
              help='نام فایل ورودی گراف دو بخشی')
def search(input):
    run_community_detection_and_plot(input)



def run_community_detection_and_plot(input_prompt):
    h = Graph.Read_GraphML(input_prompt)
    g, z = h.bipartite_projection()
    # g.vs.select(_degree=0).delete()
    # g.vs.select(_degree=1).delete()

    partition = louvain.find_partition(g, louvain.CPMVertexPartition, resolution_parameter=0.05)

    visual_style = {}
    degree = g.degree()
    visual_style["vertex_size"] = [int(x) + 20 for x in degree]

    visual_style["bbox"] = (2400, 1800)
    visual_style["margin"] = 100
    visual_style["vertex_label"] = g.vs['label']

    g.vs["group"] = partition.membership

    print(f'modularity louvain {input_prompt}: {partition.modularity}')

    visual_style["layout"] = g.layout_fruchterman_reingold()
    visual_style['mark_groups'] = True
    visual_style['vertex_order_by'] = ('group', 'asc')

    # plot(partition,  **visual_style)
    plot(partition, f'{input_prompt.replace(".graphml","")}_louvain.svg', **visual_style)





if __name__ == '__main__':
    cli.commands['search']()






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

'''