import pandas as pd
import copy, json

class Script:
	def __init__(self, path:str):
		self.path = path
		if self.path.endswith(".json"):
			self.data = pd.read_json(self.path, encoding='utf-8')
		else:
			self.data = pd.read_excel(self.path)
		self.len = len(self.data)
	
	def __copy__(self):
		return Script(self.path)
	
	def __deepcopy__(self, memo):
		return Script(copy.deepcopy(self.path, memo))

	def getSpeaker(self, id):
		return self.data.loc[id, 'NAME']
	
	def getLine(self, id):
		return self.data.loc[id, 'TEXT']

	def saveTrans(self, id, name, line):
		self.data.loc[id, 'NAME'] = name
		self.data.loc[id, 'TEXT'] = line

	def getNames(self):
		return self.data['NAME'].unique().tolist()
	
	def export(self, outpath):
		self.data.to_excel(excel_writer=outpath)