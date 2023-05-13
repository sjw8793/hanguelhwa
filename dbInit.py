import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, text

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
    __tablename__ = 'character'

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

engine = create_engine('mysql+pymysql://root:root@localhost')

drop = """DROP DATABASE IF EXISTS scriptdict"""
create = """CREATE DATABASE scriptdict default CHARACTER SET UTF8"""
use = """USE scriptdict"""

with engine.connect() as conn:
    conn.execute(text(drop))
    conn.execute(text(create))
    conn.execute(text(use))

Base.metadata.create_all(engine)