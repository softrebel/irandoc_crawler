from src.cmds import *
import time
from src.utils import *
import os
tutors=[]
crawled=[]
with open('crawled.txt','r',encoding='utf-8') as f:
    for line in f:
        crawled.append(line.strip())
with open('input.txt', 'r', encoding='utf-8') as f:
    for line in f:
        staf = line.strip().split(':')[0]
        if staf not in crawled:
            tutors.append(staf)


for tutor in tutors:
    file=f'{tutor}.json'
    exists=os.path.exists(file)
    if exists:
        logging.info(f'exists {tutor}')
        continue
    logging.info(f'starting {tutor}')
    starting_crawl(tutor, '0', '1400', f'{tutor}.json')
    logging.info(f'Completed {tutor}')
    time.sleep(1)

