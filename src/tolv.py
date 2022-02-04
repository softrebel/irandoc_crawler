import json
output={
    'windows':[]
}
names=[
    'ged_irandoc_one_mode_tf_1388_1393.graphml',
    'ged_irandoc_one_mode_tf_1392_1395.graphml',
    'ged_irandoc_one_mode_tf_1394_1400.graphml',

]
for name in names:
    temp = {'communities': []}
    from igraph import Graph,plot
    from bidi.algorithm import get_display
    from arabic_reshaper import reshape
    import louvain
    # g = Graph.Read_GraphML('teimourpour_with_labels_without_zero_degree.graphml')
    g = Graph.Read_GraphML(name)
    partition = louvain.find_partition(g, louvain.CPMVertexPartition, resolution_parameter = 0.05)

    g.vs['label'] = [get_display(reshape(label)) for label in g.vs['label']]
    visual_style = {}
    degree = g.degree()
    visual_style["vertex_size"] = [int(x)+20 for x in degree]

    visual_style["bbox"] = (2400, 1800)
    visual_style["margin"] = 100
    visual_style["vertex_label"] = g.vs['label']
    partition.subgraphs()
    g.vs["group"] = partition.membership
    # temp['communities'] = [[[x.vs[z]['name'] for z in e.tuple]
    #                         for e in x.es] for x in partition.subgraphs() if len(x.es) > 0]
    temp['communities']=[]
    degrees = g.degree()
    for x in partition.subgraphs():
        if len(x.es) > 0:
            for edge in x.es:
                edgelist = [(g.vs[e.source]['name'], g.vs[e.target]
                             ['name'], e['weight']/sum(degrees)) for e in x.es]
                edgelist.extend([(e.target, e.source, e['weight']/sum(degrees))
                                for e in x.es])
                temp['communities'].append(edgelist)
                
    for x in partition.subgraphs():
        degrees=x.degree()
        # closeness=x.closeness()

        max_degree=degrees.index(max(degrees))

        group_name=x.vs[max_degree]['name']
        for vs in x.vs:
            g.vs[vs.index]['group_name']=group_name


    print(f'modularity louvain {name}: {partition.modularity}')


    visual_style["layout"] = g.layout_fruchterman_reingold()
    visual_style['mark_groups'] = True
    visual_style['vertex_order_by'] = ('group', 'asc')

    # plot(partition,  **visual_style)
    plot(partition, f'{name}.svg', **visual_style)
    # plot(clusters2, 'c_edge_betweenness.png', **visual_style)
    output['windows'].append(temp)
    g.write_graphml(f'clustered_{name}')

with open('louvain_output_weighted.json', 'w',encoding='utf-8') as f:
    json.dump(output, f, indent=4,ensure_ascii=False)












