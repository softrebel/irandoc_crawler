from src.cmds import *
import time
tutors=[]
with open('input.txt', 'r', encoding='utf-8') as f:
    for line in f:
        tutors.append(line.split(':')[0])


for tutor in tutors:
    logging.info(f'starting {tutor}')
    starting_crawl(tutor, '0', '1400', f'{tutor}.json')
    logging.info(f'Completed {tutor}')
    time.sleep(1)

