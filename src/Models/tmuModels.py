
class Professor:
    def __init__(self,name,irandocId=None,id=None):
        self.name=name
        self.irandocId=irandocId
        self.id=id
class ProfessorType:
    def __init__(self,name,id=None):
        self.name=name
        self.id=id
class PublishableType:
    def __init__(self,name,id=None):
        self.name=name
        self.id=id
class Tag:
    def __init__(self,name,titleEn=None,irandocId=None,id=None):
        self.name=name
        self.titleEn=titleEn
        self.irandocId=irandocId
        self.id=id
class Article:
    def __init__(self,uuid,title=None,abstract=None,publishableTypeId=None,jalaliPublishDate=None,crawledName=None,id=None):
        self.uuid=uuid
        self.title=title
        self.abstract=abstract
        self.publishableTypeId=publishableTypeId
        self.jalaliPublishDate=jalaliPublishDate
        self.crawledName=crawledName
        self.id=id
class ArticleContributions:
    def __init__(self,articleId,researcherId,researcherTypeId,id=None):
        self.articleId=articleId
        self.researcherId=researcherId
        self.researcherTypeId=researcherTypeId
        self.id=id
class ArticleTag:
    def __init__(self,articleId,tagId,id=None):
        self.articleId=articleId
        self.tagId=tagId
        self.id=id

