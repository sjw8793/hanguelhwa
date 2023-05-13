import json
import copy

class Script:
	def __init__(self, path):
		self.path = path
		self.data = json.load(open(path))
		self.idList = []
		self.__update()
	
	def __copy__(self):
		return Script(self.path)
	
	def __deepcopy__(self, memo):
		return Script(copy.deepcopy(self.path, memo))
		
	def update(self):
		for id in self.data.keys():
			self.idList.append(id)
	__update = update

	def getSpeaker(self, id):
		return self.data[id]['NAME']
	
	def getLine(self, id):
		return self.data[id]['TEXT']
	
	def saveTrans(self, id, name, line):
		self.data[id]['NAME'] = name
		self.data[id]['TEXT'] = line

	def getNames(self):
		charList = []
		for script in self.data.values():
			char = script['NAME']
			if char not in charList:
				charList.append(char)
		return charList
	
	def export(self, outpath):
		with open(outpath, 'w', encoding='utf-8') as outfile:
			json.dump(self.data, outfile, indent=2, ensure_ascii=False)