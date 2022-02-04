import json

with open('src/محمد اقدسی.json',encoding='utf-8') as f:
    data=json.load(f)

# print(data)
output=[]
for item in data:
    print(item['uuid'])
    fields = item['fields']
    article = fields[0]
    abstract = fields[1]
    tags = fields[2]
    if tags and 'tags' in tags:
        article_tags = [x['title_fa'] for x in tags['tags']]
        output = []
