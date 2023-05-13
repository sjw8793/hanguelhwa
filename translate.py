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


### Parsing Functions ###

# Get names from json script and add into characters dict
# Returns characters dict
def parseJson2Char(file: Script):
	names = file.getNames()
	for name in names:
		characters[name] = dict()
		characters[name]['NAME'] = ""
		characters[name]['DESC'] = ""
		characters[name]['TONE'] = []

	return characters


### Character Add Functions ###

# Append a new character to charcters dict
# Returns characters dict
def appendChar(origin, trans):
	characters[origin] = dict()
	characters[origin]['NAME'] = trans
	characters[origin]['DESC'] = ""
	characters[origin]['TONE'] = []
	return characters

def appendReg(origin, trans):
	regions.update({origin:trans})
	return regions

def setTone(name, features):
	characters[name]['TONE'] = features.split()

def getTone(name):
	print(characters[name]['TONE'])
	return ', '.join(characters[name]['TONE'])


# Pre-translation with Translate Term Dictionary
def ruleTrans(sentence):
	# charcheck
	if characters:
		for origin in characters:
			sentence = sentence.replace(origin, characters[origin]['NAME'])
	
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
		prompt="Translate this into Korean.\nText: \"\"\"" + line + "\"\"\"",
		temperature=0.05,
		max_tokens=1000,
		top_p=1,
		frequency_penalty=0,
		presence_penalty=0)
	
	return response.choices[0].text.strip()

def fixTone(line, tone):
	response = openai.Completion.create(
		model="text-davinci-003",
		prompt= "다음을 " + tone +" 말투로 바꿔줘:\n" + line +"\n",
		temperature=0.05,
		max_tokens=1000,
		top_p=1,
		frequency_penalty=0,
		presence_penalty=0)
	
	return response.choices[0].text.strip()

def aiTranswTone(name, line):
	features = getTone(name)

	response = openai.Completion.create(
		model="text-davinci-003",
		prompt= "Translate this game dialogue line into Korean, considering suggested characteristics. \nCharacter name:" + name + "\nCharacter features:" + features + "\nLine: \"\"\"" + line + "\"\"\"",
		temperature=0.05,
		max_tokens=1000,
		top_p=1,
		frequency_penalty=0,
		presence_penalty=0)
	
	return response.choices[0].text.strip()

def getTranslation(file: Script):
	for id in file.idList:
		char = file.getSpeaker(id)
		line = file.getLine(id)
		line = aiTranswTone(char, ruleTrans(line))
		file.saveTrans(id, characters[char]['NAME'], line)
	
	return file