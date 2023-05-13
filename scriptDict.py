import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbInit import Base, KeywordDict, CharDict

engine = create_engine('mysql+pymysql://root:root@localhost/restaurant')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

### Dictionaries ###

# character = {
# 	char1 : {
# 		NAME : translated name,
# 		DESC : description for character,
# 		TONE : [character's, tone, keywords]
# 	},
#	char2 : { ... }
#}

# characters = dict()
# regions = dict()
# keywords = dict()
# items = dict()
# skills = dict()


### Dictionary Functions ###

# Append a new character to charcters dict
# Returns characters dict
def appendChar(origin, trans):
	newChar = CharDict(original=origin, trnaslated=trans)
	session.add(newChar)
	session.commit()

# Edit a character's tone info
# Get features seperated by whitespace
def setTone(name, features):
	char = session.query(CharDict).filter_by(original=name).one()
	char.tone = ', '.join(features.split())
	session.add(char)
	session.commit()

def getTone(name):
	char = session.query(CharDict).filter_by(original=name).one()
	return char.tone

# Append a new keyword to keyword dictionary
def appendKeyword(origin, trans):
	newWord = KeywordDict(original=origin, translated=trans)
	session.add(newWord)
	session.commit()

# Delete a item in keyword dictionary
def deleteKey(keyword):
	word = session.query(KeywordDict).filter_by(original=keyword).one()
	session.delete(word)
	session.commit()