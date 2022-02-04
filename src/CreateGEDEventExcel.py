import json
import csv
from igraph import Graph, plot
from bidi.algorithm import get_display
from arabic_reshaper import reshape
import louvain
import pandas as pd

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
            event_list.append([x if x!='null' else None for x in row])


    df = pd.DataFrame(event_list, columns=[
                      'source_tf', 'source_community', 'event', 'target_tf', 'target_community',])
    
    sf=df.dropna()
    sf=sf[['source_community','event', 'target_community']]
    sf.set_index('source_community', inplace=True)
    print(sf)
    sf.to_excel('ged_results_closeness centrality.xlsx', index=False)
    
    
    from openpyxl import Workbook
    wb = Workbook()


    # grab the active worksheet
    ws = wb.active
    ws.title = "لیست مقالات"
    ws.append(sf['source_community'].tolist())



