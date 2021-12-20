import csv, json, requests
from src.config import *
import logging

logging.basicConfig(filename='app.log', filemode='w', encoding='utf-8', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def to_csv(input, filename):
    with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(input)


def to_json(input, filename):
    with open(filename, 'w', encoding="utf-8") as file:
        data = json.dumps(input, ensure_ascii=False)
        file.write(data)


def get_request(url, params={}):
    response = requests.get(url, params=params)
    content = response.content
    if response.status_code == 200:
        result = json.loads(content)
    else:
        logging.error("error on getting url " + url)
        result = {}
    return result
