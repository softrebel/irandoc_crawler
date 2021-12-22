import json
from src.Models.tmuModels import *
from src.tmuRepository import *
import os

arr = os.listdir(os.path.join(os.path.curdir,"files"))
print(arr)


for folder in arr:


    _repository = TmuRepository()
    data = {}
    crawled_name = folder.split('.json')[0]
    with open(f'files/{folder}', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    for item in data:
        print(item['uuid'])
        fields = item['fields']
        article = fields[0]
        abstract = fields[1]
        tags = fields[2]
        title = 'Not Shown'
        if not article:
            print('dont have article info', item['uuid'])
            continue
        _article = _repository.get_article_by_uuid(item['uuid'])
        if not _article:
            _article = Article(item['uuid'])
            if article:
                _article.title = article['title']
                _article.jalaliPublishDate = article['ja_pub_yyyy']
                publishable_type_name = article['publishable_type']
                publishable_type = _repository.get_publishable_type_by_name(publishable_type_name)
                if not publishable_type:
                    publishable_type = PublishableType(publishable_type_name)
                    id = _repository.insert_publishable_type_if_not_exist(publishable_type)
                    if not id:
                        raise Exception("error on insert publishable_type")
                    publishable_type.id = id
                _article.publishableTypeId = publishable_type.id
            _article.crawledName = crawled_name
            if abstract:
                _article.abstract = abstract['abstract']
            id = _repository.insert_article_if_not_exist(_article)
            if not id:
                raise Exception("error on insert article")
            _article.id = id

        # contributions
        for contrib in article['contributions']:
            researcher_type_name = contrib['role']['title_fa']
            researcher_type = _repository.get_researcher_type_by_name(researcher_type_name)
            if not researcher_type:
                researcher_type = ProfessorType(researcher_type_name)
                id = _repository.insert_researcher_type_if_not_exist(researcher_type)
                if not id:
                    raise Exception("error on insert researcher_type")
                researcher_type.id = id

            researcher_name = contrib['researcher']['full_name_fa']
            irandocId = contrib['researcher']['id']
            researcher = _repository.get_researcher_by_irandoc_id(irandocId)
            if not researcher:
                researcher = Professor(researcher_name, irandocId)
                id = _repository.insert_researcher_if_not_exist(researcher)
                if not id:
                    raise Exception("error on insert profeesor")
                researcher.id = id

            article_contribution = _repository.get_contrib_by_article_researcher_researchertype(_article.id, researcher.id,
                                                                                              researcher_type.id)
            if not article_contribution:
                article_contribution = ArticleContributions(_article.id, researcher.id, researcher_type.id)
                id = _repository.insert_article_contributions_if_not_exist(article_contribution)
                if not id:
                    raise Exception("error on article contribution")
                article_contribution.id = id

        for tag in tags['tags']:
            irandocId = tag['id']
            name = tag['title_fa']
            titleEn = tag['title_en']
            _tag = _repository.get_tag_by_name(name)
            if not _tag:
                _tag = Tag(name, titleEn, irandocId)
                id = _repository.insert_tag_if_not_exist(_tag)
                if not id:
                    raise Exception("error on tag")
                _tag.id = id
            _article_tag = _repository.get_article_tag_by_article_tag(_article.id, _tag.id)
            if not _article_tag:
                _article_tag = ArticleTag(_article.id, _tag.id)
                id = _repository.insert_article_tag_if_not_exist(_article_tag)
                if not id:
                    raise Exception("error on article tag")
                _article_tag.id = id

        # for field in fields:
        #     print(field[0])
        #     print(field[3])
