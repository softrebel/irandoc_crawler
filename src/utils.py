import csv,json,requests
def to_csv(input,filename):
    with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(input)
def to_json(input,filename):
    with open(filename, 'w',encoding="utf-8") as file:
        data=json.dumps(input,ensure_ascii=False)
        file.write(data)


def get_request(url,params={}):
    response = requests.get(url,params=params)
    content = json.loads(response.content)
    return content