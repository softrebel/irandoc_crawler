from src.config import *
import sqlite3
from src.Models.tmuModels import *
class TmuRepository:
    def __init__(self):
        pass



    def get_all_tags(self):
        query='''
        select f.name as first,g.name as second from  (
            select tag.name,articleId
            from article
                     inner join article_tag on articleId = article.id
                     inner join tag on tagId = tag.id ) as f
            inner join  (
            select tag.name,articleId
            from article
                     inner join article_tag on articleId = article.id
                     inner join tag on tagId = tag.id ) as g
            on f.articleId=g.articleId
            where f.name != g.name
        '''
        con = sqlite3.connect(DB_NAME)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute(query)
        rows=[dict(row) for row in cur.fetchall()]
        return rows

    def get_article_tag_by_article_tag(self,articleId,tagId):
        con = sqlite3.connect(DB_NAME)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM article_tag WHERE articleId=? and tagId=?", (articleId,tagId))

        row = cur.fetchone()
        con.close()
        if row:
            record = dict(row)
            result = ArticleTag(**record)
            result.id = record['id']
            return result

        return  None





    def get_tag_by_name(self,name):
        con = sqlite3.connect(DB_NAME)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM tag WHERE name=?", (name,))

        row = cur.fetchone()
        con.close()
        if row:
            record = dict(row)
            result = Tag(**record)
            result.id = record['id']
            return result

        return  None

    def get_researcher_type_by_name(self,name):
        con = sqlite3.connect(DB_NAME)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM researcher_type WHERE name=?", (name,))

        row = cur.fetchone()
        con.close()
        if row:
            record = dict(row)
            result = ProfessorType(**record)
            result.id = record['id']
            return result

        return  None

    def get_researcher_by_name(self,name):
        con = sqlite3.connect(DB_NAME)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM researcher WHERE name=?", (name,))

        row = cur.fetchone()
        con.close()
        if row:
            record = dict(row)
            result = Professor(**record)
            result.id = record['id']
            return result

        return None

    def get_researcher_by_irandoc_id(self,irandocId):
        con = sqlite3.connect(DB_NAME)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM researcher WHERE irandocId=?", (irandocId,))

        row = cur.fetchone()
        con.close()
        if row:
            record = dict(row)
            result = Professor(**record)
            result.id = record['id']
            return result

        return None

    def get_article_by_uuid(self,uuid):
        con = sqlite3.connect(DB_NAME)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM article WHERE uuid=?", (uuid,))

        row = cur.fetchone()
        con.close()
        if row:
            record = dict(row)
            result = Article(**record)
            result.id = record['id']
            return result

        return None

    def get_publishable_type_by_name(self,name):
        con = sqlite3.connect(DB_NAME)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM publishable_type WHERE name=?", (name,))

        row = cur.fetchone()
        con.close()
        if row:
            record = dict(row)
            result = PublishableType(**record)
            result.id = record['id']
            return result

        return None
    def get_contrib_by_article_researcher_researchertype(self,articleId,researcherId,researcherTypeId):
        con = sqlite3.connect(DB_NAME)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM article_contributions WHERE articleId=? and researcherId=? and researcherTypeId=?"
                    , (articleId,researcherId,researcherTypeId))

        row = cur.fetchone()
        con.close()
        if row:
            record = dict(row)
            result = ArticleContributions(**record)
            result.id = record['id']
            return result

        return None

    def insert_article_tag_if_not_exist(self,item:ArticleTag):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        # Insert a row of data
        cur.execute(f'''
        INSERT OR IGNORE INTO article_tag (articleId,tagId) VALUES (?,?)
        ''',(item.articleId,item.tagId,))
        con.commit()
        id=cur.lastrowid
        con.close()
        return id


    def insert_tag_if_not_exist(self,item:Tag):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        # Insert a row of data
        cur.execute(f'''
        INSERT OR IGNORE INTO tag (name,titleEn,irandocId) VALUES (?,?,?)
        ''',(item.name,item.titleEn,item.irandocId,))
        con.commit()
        id=cur.lastrowid
        con.close()
        return id

    def insert_article_contributions_if_not_exist(self,item:ArticleContributions):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        # Insert a row of data
        cur.execute(f'''
        INSERT OR IGNORE INTO article_contributions (articleId,researcherId,researcherTypeId) VALUES (?,?,?)
        ''',(item.articleId,item.researcherId,item.researcherTypeId,))
        con.commit()
        id=cur.lastrowid
        con.close()
        return id

    def insert_publishable_type_if_not_exist(self,item:PublishableType):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        # Insert a row of data
        cur.execute(f'''
        INSERT OR IGNORE INTO publishable_type (name) VALUES (?)
        ''',(item.name,))
        con.commit()
        id=cur.lastrowid
        con.close()
        return id
    def insert_researcher_if_not_exist(self,item:Professor):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        # Insert a row of data
        cur.execute(f'''
        INSERT OR IGNORE INTO researcher (name,irandocId) VALUES (?,?)
        ''',(item.name,item.irandocId))
        con.commit()
        id=cur.lastrowid
        con.close()
        return id


    def insert_researcher_type_if_not_exist(self,item:ProfessorType):
        con = sqlite3.connect(DB_NAME)

        cur = con.cursor()
        # Insert a row of data
        cur.execute(f'''
        INSERT OR IGNORE INTO researcher_type (name) VALUES (?)
        ''',(item.name,))
        con.commit()
        id = cur.lastrowid
        con.close()
        return id

    def insert_article_if_not_exist(self,item:Article):
        con = sqlite3.connect(DB_NAME)

        cur = con.cursor()
        # Insert a row of data
        cur.execute(f'''
        INSERT OR IGNORE INTO article 
        (uuid,title,abstract,publishableTypeId,jalaliPublishDate,crawledName) 
        VALUES (?,?,?,?,?,?)
        ''',(item.uuid,item.title,item.abstract,item.publishableTypeId,item.jalaliPublishDate,item.crawledName))
        con.commit()
        id = cur.lastrowid
        con.close()
        return id


if __name__ == '__main__':
    _reposity=TmuRepository()
    a=_reposity.get_researcher_type_by_name('استاد راهنما')
    print(a)