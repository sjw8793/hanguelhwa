import os
import sys
import pymysql
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database, drop_database

Base = declarative_base()

class KeywordDict(Base):
    __tablename__ = 'keyword'

    id = Column(Integer, primary_key=True)
    original = Column(String(100), nullable=False)
    translated = Column(String(100))
    description = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'original': self.original,
            'translated': self.translated,
            'description': self.description
        }
    
class CharDict(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    original = Column(String(100), nullable=False)
    translated = Column(String(100))
    description = Column(String(250))
    tone = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'original': self.original,
            'translated': self.translated,
            'description': self.description,
            'tone': self.tone
        }

keyword_sql = '''
CREATE TABLE keyword
(id int NOT NULL AUTO_INCREMENT, 
 original varchar(100) NOT NULL,
 translated varchar(100),
 description varchar(250),
 PRIMARY KEY (id))
'''

character_sql = '''
CREATE TABLE characters
(id int NOT NULL AUTO_INCREMENT, 
 original varchar(100) NOT NULL,
 translated varchar(100),
 description varchar(250),
 tone varchar(250),
 PRIMARY KEY (id))
'''

drop_sql = '''
DROP DATABASE IF EXISTS scriptdict
'''

create_sql = '''
CREATE DATABASE scriptdict default CHARACTER SET UTF8
'''

# RESET database
conn = pymysql.connect(host='localhost', user='root', password='root', charset='utf8')
curs = conn.cursor()

curs.execute(drop_sql)
curs.execute(create_sql)

conn.close()


# Set up tables
conn = pymysql.connect(host='localhost', user='root', password='root', db='scriptdict', charset='utf8')
curs = conn.cursor()

curs.execute(keyword_sql)
curs.execute(character_sql)

conn.close()


engine = create_engine('mysql+pymysql://root:root@localhost/scriptdict')

Base.metadata.create_all(engine)