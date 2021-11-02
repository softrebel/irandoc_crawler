import requests,json
from src.config import *
import asyncio,random,time







def get_article(uuid):
    url = f"{BASE_API_URL}/{RESOURCES['articles']}/{uuid}"
    content = get_request(url)
    return content

def get_abstract(uuid):
    url = f"{BASE_API_URL}/{RESOURCES['abstract'].format(uuid=uuid)}"
    content = get_request(url)
    return content

def get_tags(uuid):
    url = f"{BASE_API_URL}/{RESOURCES['tags'].format(uuid=uuid)}"
    content = get_request(url)
    return content

def get_aditional_fields(uuid):
    url = f"{BASE_API_URL}/{RESOURCES['additional_fields'].format(uuid=uuid)}"
    content = get_request(url)
    return content








class Crawl():

    @staticmethod
    def search(keywords,year_from,year_to):
        output=[]
        query_params=QUERY_PARAMS
        query_params.update({
            'keywords':keywords,
            'year_from':year_from,
            'year_to':year_to
        })
        url=f"{BASE_API_URL}/{RESOURCES['search']}"
        response = requests.get(url, params=query_params)
        content = json.loads(response.content)
        total_pages = content['total_pages']
        output.extend(content['results'])
        for page in range(2, total_pages + 1):
            query_params['page'] = page
            response = requests.get(url, params=query_params)
            content = json.loads(response.content)
            output.extend(content['results'])

        return output

    @staticmethod
    def export(result,output_name):
        ext=output_name.split('.')[-1]
        if ext not in SUPPORTED_EXTENSIONS.keys():
            raise Exception(LANG['format_not_supported'])
        exporter=SUPPORTED_EXTENSIONS[ext]
        exporter(result,output_name)
        return True



    @staticmethod
    async def scrape_articles(article_list):
        article_collection=[]
        for article in article_list:


            print("scraping Started",article['uuid'])
            loop = asyncio.get_event_loop()
            async_get_article = loop.run_in_executor(None, get_article, article['uuid'])
            async_get_abstract = loop.run_in_executor(None, get_abstract, article['uuid'])
            async_get_tags = loop.run_in_executor(None, get_tags, article['uuid'])
            async_get_aditional_fields = loop.run_in_executor(None, get_aditional_fields, article['uuid'])

            fields=await asyncio.gather(
                async_get_article,
                async_get_abstract,
                async_get_tags,
                async_get_aditional_fields
            )
            article_collection.append(fields)
            print("scraping Done ", article['uuid'])
            rand_sleep = random.randint(*SLEEP_RANGE)
            time.sleep(rand_sleep)

        return article_collection




