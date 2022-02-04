

from src.tmuRepository import *
import os
from igraph import Graph, plot
from bidi.algorithm import get_display
from arabic_reshaper import reshape
from src.clean import clean_pattern_for_irandoc
_repository = TmuRepository()
import click
lang = LANG
generate_bipartite_prompt= click.style(lang['generate_bipartite'],
                             bold=True, bg='green', fg='yellow')
@click.group()
def cli():
    pass




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



@cli.command()
@click.option('-n', '--name', default='بابک تیمورپور', type=str, prompt=generate_bipartite_prompt,
              help='نام فایل ورودی گراف دو بخشی')
def generate(name):
    name=name.strip()
    if not name or name =='':
        print('Name incorrect')
        return
    row = _repository.get_article_tags_by_crawled_name(name)
    if len(row) == 0:
        print('No item retrieved.')
    row = [
        {'first': clean_pattern_for_irandoc(x['tag_name']),
         # 'second': clean_pattern_for_irandoc(x['researcher_name']),
         'second': x['uuid'],
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


    g.vs.select(_degree=0).delete()
    g.vs['label'] = g.vs['name']
    g.vs['label'] = [get_display(reshape(label)) for label in g.vs['label']]
    degree = g.degree()
    g.simplify()
    visual_style = {}
    visual_style["edge_curved"] = False
    visual_style["vertex_size"] = [int(x) / max(degree) + 20 for x in degree]

    visual_style["bbox"] = (2400, 1800)

    layouts={
        'layout_fruchterman_reingold':
            g.layout_fruchterman_reingold, 'layout_bipartite':g.layout_bipartite
    }
    for key,item in layouts.items():
        visual_style["layout"] = item()
        filename=f'{name}_pure_bipartite_graph_{key}.svg'
        plot(g,filename, **visual_style)
        print(filename,'Created.')
    g.write_graphml(f'{name}_pure_bipartite_graph.graphml')
    print(f'{name}_pure_bipartite_graph.graphml Created')



if __name__ == '__main__':
    cli.commands['generate']()


