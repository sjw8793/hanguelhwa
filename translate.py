import os
import openai
import config

openai.api_key = config.api_key



### Dictionaries ###
character = dict()
region = dict()
keyword = dict()
item = dict()
skill = dict()

# Select dictionary, original word, translation word
def appendRule(dic, origin, trans):
    try:
        dic[origin] = trans
    except NameError:
        print("Error! Selected dictionary doesn't exist")
    return

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

# 