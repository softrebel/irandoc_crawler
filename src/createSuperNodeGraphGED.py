import json
import csv
from igraph import Graph, plot
from bidi.algorithm import get_display
from arabic_reshaper import reshape
import louvain

names = [
    'ged_results_closeness centrality.csv',

]

event_types = {
    'continuing': 1,
    'shrinking': 2,
    'growing': 3,
    'split': 4,
    'merge': 5,
    'dissolving': 6,
    'No_event': 7,
}
for name in names:
    event_list = []
    with open('src/ged_results_closeness centrality.csv', 'r', encoding='utf-8') as f:
        spamreader = csv.reader(f, delimiter=',', quotechar='|')
        for row in spamreader:
            event_list.append(row)

    print(event_list)
    added_nodes = set()
    # g = Graph.Read_GraphML('teimourpour_with_labels_without_zero_degree.graphml')
    g = Graph()
    for item in event_list:
        if item[0] == 'null':
            item[0] = item[2]
            item[1] = item[3]
        if item[2] == 'null':
            item[2] = item[0]
            item[3] = item[1]
        source_name = f'T{item[0]} G{item[1]}'
        source_type = item[0]
        source_event = item[2]
        if source_name not in added_nodes:
            g.add_vertex(source_name, type=source_type, event=source_event)
            added_nodes.add(source_name)
        target_name = f'T{item[2]} G{item[3]}'
        target_type = item[0]
        target_event = item[2]
        if target_name not in added_nodes:
            g.add_vertex(target_name, type=target_type, event=target_event)
            added_nodes.add(target_name)
        g.add_edge(source_name, target_name, label=item[4])

    # g.vs['label'] = [get_display(reshape(label)) for label in g.vs['label']]
    visual_style = {}
    degree = g.degree()
    visual_style["vertex_size"] = [int(x)+50 for x in degree]

    visual_style["bbox"] = (2400, 1800)
    visual_style["margin"] = 50
    visual_style["vertex_label"] = g.vs['name']
    visual_style["layout"] = g.layout_fruchterman_reingold()
    # visual_style["layout"] = g.layout("rt")
    visual_style['mark_groups'] = True
    # visual_style['vertex_order_by'] = ('group', 'asc')

    plot(g,  **visual_style)
    # plot(g, f'{name}.svg', **visual_style)
    g.write_graphml(f'ged_super_node.graphml')
