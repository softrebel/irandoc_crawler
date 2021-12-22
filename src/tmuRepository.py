from src.config import *
import sqlite3
from src.Models.tmuModels import *
class TmuRepository:
    def __init__(self):
        pass







    def get_professor_type_by_name(self,name):
        con = sqlite3.connect(DB_NAME)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM professor_type WHERE name=?", (name,))

        row = cur.fetchone()
        con.close()
        if row:
            record = dict(row)
            result = ProfessorType(**record)
            result.id = record['id']
            return result

        return  None

    def get_professor_by_name(self,name):
        con = sqlite3.connect(DB_NAME)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM professor WHERE name=?", (name,))

        row = cur.fetchone()
        con.close()
        if row:
            record = dict(row)
            result = Professor(**record)
            result.id = record['id']
            return result

        return None

    def get_professor_by_irandoc_id(self,irandocId):
        con = sqlite3.connect(DB_NAME)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM professor WHERE irandocId=?", (irandocId,))

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
    def get_contrib_by_article_professor_professortype(self,articleId,professorId,professorTypeId):
        con = sqlite3.connect(DB_NAME)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM article_contributions WHERE articleId=? and professorId=? and professorTypeId=?"
                    , (articleId,professorId,professorTypeId))

        row = cur.fetchone()
        con.close()
        if row:
            record = dict(row)
            result = ArticleContributions(**record)
            result.id = record['id']
            return result

        return None

    def insert_article_contributions_if_not_exist(self,item:ArticleContributions):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        # Insert a row of data
        cur.execute(f'''
        INSERT OR IGNORE INTO article_contributions (articleId,professorId,professorTypeId) VALUES (?,?,?)
        ''',(item.articleId,item.professorId,item.professorTypeId,))
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
    def insert_professor_if_not_exist(self,item:Professor):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        # Insert a row of data
        cur.execute(f'''
        INSERT OR IGNORE INTO professor (name,irandocId) VALUES (?,?)
        ''',(item.name,item.irandocId))
        con.commit()
        id=cur.lastrowid
        con.close()
        return id


    def insert_professor_type_if_not_exist(self,item:ProfessorType):
        con = sqlite3.connect(DB_NAME)

        cur = con.cursor()
        # Insert a row of data
        cur.execute(f'''
        INSERT OR IGNORE INTO professor_type (name) VALUES (?)
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
    a=_reposity.get_professor_type_by_name('استاد راهنما')
    print(a)