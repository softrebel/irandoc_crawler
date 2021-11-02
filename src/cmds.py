from src.config import *
import click
from src.Models.crawl import Crawl
import asyncio
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
@click.option('-k', '--keywords', default="بابک تیمورپور", type=str, prompt=search_prompt, help='عبارت مورد جستجو')
@click.option('-yf', '--year-from', default=0, type=str, prompt=year_from_prompt,
              help='جستجو از این سال شروع می شود')
@click.option('-yt', '--year-to', default=1400, type=str, prompt=year_to_prompt,
              help='جستجو تا این سال انجام می شود')
@click.option('-o', '--output', default='test.json', type=str, prompt=output_prompt,
              help='نام فایل خروجی')
def search(keywords, year_from, year_to,output):
    result = Crawl.search(keywords, year_from, year_to)
    loop = asyncio.get_event_loop()
    article_collection=loop.run_until_complete(Crawl.scrape_articles(result))
    export=Crawl.export(article_collection,output)
    print(LANG['crawl_done'])