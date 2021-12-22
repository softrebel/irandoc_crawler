import json
from src.Models.tmuModels import *
from src.tmuRepository import *

_repository = TmuRepository()
data = {}
crawled_name = 'الهام آخوندزاده '
with open(f'{crawled_name}.json', 'r', encoding='utf-8') as f:
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
        id=_repository.insert_article_if_not_exist(_article)
        if not id:
            raise Exception("error on insert article")
        _article.id=id


    # contributions
    for contrib in article['contributions']:
        professor_type_name = contrib['role']['title_fa']
        professor_type = _repository.get_professor_type_by_name(professor_type_name)
        if not professor_type:
            professor_type = ProfessorType(professor_type_name)
            id = _repository.insert_professor_type_if_not_exist(professor_type)
            if not id:
                raise Exception("error on insert professor_type")
            professor_type.id = id

        professor_name = contrib['researcher']['full_name_fa']
        irandocId = contrib['researcher']['id']
        professor = _repository.get_professor_by_irandoc_id(irandocId)
        if not professor:
            professor = Professor(professor_name,irandocId)
            id = _repository.insert_professor_if_not_exist(professor)
            if not id:
                raise Exception("error on insert profeesor")
            professor.id = id

        article_contribution=_repository.get_contrib_by_article_professor_professortype(_article.id,professor.id,professor_type.id)
        if not article_contribution:
            article_contribution = ArticleContributions(_article.id,professor.id,professor_type.id)
            id = _repository.insert_article_contributions_if_not_exist(article_contribution)
            if not id:
                raise Exception("error on article contribution")
            article_contribution.id = id
        print(article_contribution.id)


    print(abstract)

    # for field in fields:
    #     print(field[0])
    #     print(field[3])
