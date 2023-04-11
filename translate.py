import os
import json
import openai
import config

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
def parseJson2Char(filePath):
	file = open(filePath)
	data = json.load(file)

	for id, script in data.items():
		appendChar(script["NAME"], "")
	
	return characters


def appendChar(origin, trans):
	characters.update({origin:trans})
	return characters

def appendReg(origin, trans):
	regions.update({origin:trans})
	return regions

# Pre-translation with Translate Term Dictionary
def ruleTrans(sentence):
	# charcheck
	if character:
		for origin in character:
			sentence = sentence.replace(origin, character[origin])
	
	# regcheck
	if region:
		for origin in region:
			sentence = sentence.replace(origin, region[origin])
					
	# keycheck
	if region:
		for origin in keyword:
			sentence = sentence.replace(origin, keyword[origin])
	
	# itemcheck
	if item:
		for origin in item:
			sentence = sentence.replace(origin, item[origin])
	
	# skillcheck
	if skill:
		for origin in skill:
			sentence = sentence.replace(origin, skill[origin])
	
	return sentence

# Translate with GPT-3
def getTranslation(script):
	response = openai.Completion.create(
		model="text-davinci-003",
		prompt="Translate this into Korean:" + script,
		temperature=0.05,
		max_tokens=500,
		top_p=1,
		frequency_penalty=0,
		presence_penalty=0)
	
	return response.choices[0].text.strip()