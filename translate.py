import os
import json
import openai
import config
from fileManage import Script

openai.api_key = config.API_KEY


### Dictionaries ###

# character = {
# 	char1 : {
# 		NAME : translated name,
# 		DESC : description for character,
# 		TONE : [character's, tone, keywords]
# 	},
#	char2 : { ... }
#}

characters = dict()
regions = dict()
keywords = dict()
items = dict()
skills = dict()


# Get names from json script and add into character dict
# Returns character dict
def parseJson2Char(file: Script):
	names = file.getNames()
	for name in names:
		characters[name] = ""

	return characters


def appendChar(origin, trans):
	characters.update({origin:trans})
	return characters

def appendReg(origin, trans):
	regions.update({origin:trans})
	return regions

def getTone(name):
	pass

# Pre-translation with Translate Term Dictionary
def ruleTrans(sentence):
	# charcheck
	if characters:
		for origin in characters:
			sentence = sentence.replace(origin, characters[origin])
	
	# regcheck
	if regions:
		for origin in regions:
			sentence = sentence.replace(origin, regions[origin])
					
	# keycheck
	if regions:
		for origin in keywords:
			sentence = sentence.replace(origin, keywords[origin])
	
	# itemcheck
	if items:
		for origin in items:
			sentence = sentence.replace(origin, items[origin])
	
	# skillcheck
	if skills:
		for origin in skills:
			sentence = sentence.replace(origin, skills[origin])
	
	return sentence

# Translate with GPT-3
def aiTrans(line):
	response = openai.Completion.create(
		model="text-davinci-003",
		prompt="Translate this into Korean:\n" + line,
		temperature=0.05,
		max_tokens=1000,
		top_p=1,
		frequency_penalty=0,
		presence_penalty=0)
	
	return response.choices[0].text.strip()

def fixTone(line, tone):
	response = openai.Completion.create(
		model="text-davinci-003",
		prompt= tone + "다음을 " + tone +" 말투로 바꿔줘:\n" + line +"\n",
		temperature=0.05,
		max_tokens=600,
		top_p=1,
		frequency_penalty=0,
		presence_penalty=0)
	
	return response.choices[0].text.strip()

def getTranslation(file: Script):
	for id in file.idList:
		name = characters[file.getSpeaker(id)]
		line = file.getLine(id)
		line = aiTrans(ruleTrans(line))
		file.saveTrans(id, name, line)
	
	return file