
from itertools import groupby
from src.Models.tmuModels import *
from src.tmuRepository import *

from igraph import *

_repository = TmuRepository()

rows=_repository.get_all_article()

headers=[
    'شناسه ایرانداک',
    'عنوان',
    'سال انتشار',
    'نوع نشر',
    'نام کراول شده',
    'تگ ها',
    '1شناسه ایرانداک محقق',
    '1نام محقق',
    '1نوع محقق',
    '2شناسه ایرانداک محقق',
    '2نام محقق',
    '2نوع محقق',
    '3شناسه ایرانداک محقق',
    '3نام محقق',
    '3نوع محقق',
    '4شناسه ایرانداک محقق',
    '4نام محقق',
    '4نوع محقق',
    '5شناسه ایرانداک محقق',
    '5نام محقق',
    '5نوع محقق',
    '6شناسه ایرانداک محقق',
    '6نام محقق',
    '6نوع محقق',

    
]


rows = sorted(rows,key=lambda x: x['uuid'])
output=[]

for key, value in groupby(rows, key=lambda x: x['uuid']):
    items=list(value)
    record={
        'uuid':key,
        'title':items[0]['title'],
        'publishDate':items[0]['publishDate'],
        'publication_type':items[0]['publication_type'],
        'crawled_name':items[0]['crawled_name']
    }
    record['tags']=', '.join([item['tag'] for item in items])
    record_as_list=list(record.values())
    ids_seen=[]
    for item in items:
        if item['researcher_id'] not in ids_seen:
            ids_seen.append(item['researcher_id'])
            record_as_list.append(item['researcher_id'])
            record_as_list.append(item['researcher_name'])
            record_as_list.append(item['researcher_type'])
    output.append(record_as_list)


from openpyxl import Workbook
wb = Workbook()


# grab the active worksheet
ws = wb.active
ws.title="لیست مقالات"
ws.append(headers)
for out in output:
    ws.append(out)

# Rows can also be appended
# ws.append(row)


# Save the file
wb.save("sample.xlsx")