import json
from src.Models.tmuModels import *
from src.tmuRepository import *
import os
from igraph import *
from bidi.algorithm import get_display
from arabic_reshaper import reshape
from src.clean import clean_pattern_for_irandoc
_repository = TmuRepository()
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

import click
lang = LANG
search_prompt = click.style(lang['search_text'],
                            bold=True, bg='green', fg='yellow')
year_from_prompt = click.style(lang['year_from'],
                               bold=True, bg='green', fg='yellow')
year_to_prompt = click.style(lang['year_to'],
                             bold=True, bg='green', fg='yellow')
main_prompt= click.style(lang['main'],
                             bold=True, bg='green', fg='yellow')
output_prompt= click.style(lang['output'],
                             bold=True, bg='green', fg='yellow')

@click.group()
def cli():
    pass

@cli.command()
@click.option('-r', '--researcher_name', default="بابک تیمورپور", type=str, prompt=search_prompt, help='نام استاد مورد نظر')
@click.option('-yf', '--year-from', default=0, type=str, prompt=year_from_prompt,
              help='جستجو از این سال شروع می شود')
@click.option('-yt', '--year-to', default=1400, type=str, prompt=year_to_prompt,
              help='جستجو تا این سال انجام می شود')
@click.option('-o', '--output', default='output_bipartite.graphml', type=str, prompt=output_prompt,
              help='نام فایل خروجی گراف')
def search(researcher_name, year_from, year_to,output):
    items=read_from_db(researcher_name, year_from, year_to)
    create_graphml(items,output)
    create_excel(items)

def read_from_db(researcher_name, year_from, year_to):
    items=_repository.get_article_tag_by_researcher_name(researcher_name, year_from, year_to)
    return items

def create_graphml(items,output):
    row = [
        {'first': clean_pattern_for_irandoc(x['tag']),
         # 'second': clean_pattern_for_irandoc(x['researcher_name']),
         'second': x['uuid'],
         'pure': x['tag']}
        for x in items]

    first = list(set([x['first'] for x in row if x['first'] != '']))

    second = list(set([x['second'] for x in row]))

    nodes = [*first, *second]
    edges = [(x['first'], x['second']) for x in row if x['first'] != '']

    h = Graph()
    h.add_vertices(first, attributes={'type': 0})
    h.add_vertices(second, attributes={'type': 1})
    h.add_edges(edges)

    # h, z = g.bipartite_projection()
    # g.vs.select(_degree=0).delete()
    # g.vs.select(_degree=1).delete()

    h.vs['label'] = [get_display(reshape(label)) for label in h.vs['name']]
    # h.vs['label'] = h.vs['name']

    h.write_graphml(output)
    print("Graph created successfully")
    print("Graph statistics:")
    h.graph_statistics()


def create_excel(items):
    from itertools import groupby
    from operator import itemgetter

    itemlist = sorted(items,
                      key=itemgetter('uuid'))

    output = []

    # Display data grouped by grade
    for key, value in groupby(itemlist,
                              key=itemgetter('uuid')):
        # print(key)
        temp = {}
        for k in value:
            # print(k)
            if len(temp.keys()) == 0:
                first = k
                temp.update({
                    'شناسه مقاله': key,
                    'عنوان': first['title'],
                    'نام جستجو شده': first['crawled_name'],
                    'سال انتشار': int(first['jalali_publish_date']),
                    'نوع انتشار': first['publishable_type'],
                    'uuid': key,
                    'title': first['title'],
                    'crawled_name': first['crawled_name'],
                    'jalali_publish_date': int(first['jalali_publish_date']),
                    'publishable_type': first['publishable_type'],

                })
            if 'tags' not in list(temp.keys()):
                temp['tags'] = []
            if 'researchers' not in list(temp.keys()):
                temp['researchers'] = []

            if k['tag'] not in temp['tags']:
                temp['tags'].append(k['tag'])
            if k['researcher'] not in [x['name'] for x in temp['researchers']]:
                temp['researchers'].append({
                    'name': k['researcher'],
                    'type': k['reseacher_type'],
                    'irandoc_id': k['researcher_irandoc_id']
                })
        output.append(temp)

    output = sorted(output, key=lambda d: d['jalali_publish_date'], reverse=True)
    for i in range(len(output)):
        output[i]['واژگان'] = '، '.join(output[i]['tags'])
        output[i]['researchers'] = sorted(output[i]['researchers'], key=lambda d: d['type'])
        j = 1
        for researcher in output[i]['researchers']:
            keys = list(output[i].keys())
            type = researcher['type']
            while type in keys:
                type = f'{type} {j}'
                j += 1
            name=researcher['name']
            # if name ==output[i]['crawled_name']:
            #     name=f'**{name}**'
            output[i][type] = name
            id = f'شناسه {type}'
            output[i][id] = researcher['irandoc_id']


        del output[i]['tags']
        del output[i]['researchers']
        del output[i]['uuid']
        del output[i]['title']
        del output[i]['crawled_name']
        del output[i]['jalali_publish_date']
        del output[i]['publishable_type']

    import pandas as pd
    df = pd.DataFrame(output)

    import xlwings as xw
    wb = xw.Book()
    sheet = wb.sheets['Sheet1']
    sheet.range('A1').value = df
    print("Excel created successfully")


if __name__ == '__main__':
    while True:
        value = click.prompt(LANG['main'], type=click.Choice(list(cli.commands.keys()) + ['exit']))
        if value != 'exit':
            cli.commands[value]()
        else:
            break