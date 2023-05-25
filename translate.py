import os
import json
import openai
import config
import scriptDict
from fileManage import Script
from dbInit import CharDict, KeywordDict

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

# characters = dict()
# regions = dict()
# keywords = dict()
# items = dict()
# skills = dict()


### Parsing Functions ###

# Get names from json script and add into characters dict
# Returns characters dict
def parseJson2Char(file: Script):
	names = file.getNames()
	for name in names:
		scriptDict.appendChar(name, "")



### Translate Functions ###

# Pre-translation with Translate Term Dictionary
def ruleTrans(sentence):
	for character in scriptDict.characters():
		sentence = sentence.replace(character.original, character.translated)
	for word in scriptDict.words():
		sentence = sentence.replace(word.original, word.translated)
	return sentence

# Translate with GPT-3
def aiTrans(line):
	response = openai.Completion.create(
		model="text-davinci-003",
		prompt="Translate this into Korean.\nText: " + line,
		temperature=0.05,
		max_tokens=1000,
		top_p=1,
		frequency_penalty=0,
		presence_penalty=0)
	
	return response.choices[0].text.strip()

# def fixTone(line, tone):
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
	features = scriptDict.getTone(name)

	response = openai.Completion.create(
		model="text-davinci-003",
		prompt= "Translate this game dialogue line into Korean, considering suggested characteristics.\nCharacter name: " + name + "\nCharacter features: " + features + "\nLine: " + line + "\nTranslated line:",
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
		file.saveTrans(id, scriptDict.getChar(char).translated, line)
	
	return file