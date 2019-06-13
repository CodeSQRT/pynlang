from lib import *
from lib.detect import *
class Buffer:
	def __init__(self):
		self.value = ""
		self.type = 0
	def __setattr__(self, name, value):
		self.__dict__[name] = value

class Token:
	def __init__(self, value, type):
		if type == STRING:
			value = value[1:]
			value = value[:len(value) - 1]
		self.value = value
		self.type = type
	
	def __str__(self):
		return str(f"{NToken_ConstantName(self.type)}:\"{self.value}\"")

class LexedLine:
	def __init__(self):
		self.tabs = 0
		self.tpl = None
		self.tokens = list()

	def __str__(self):
		# return str(self.tokens)
		dump = list()
		for tok in self.tokens:
			dump.append(tok.__dict__)
		return str(dump)

	def insert(self, token):
		self.tokens.append(token)

	def pop(self, token):
		self.tokens.pop(token)

	def search(self, type=None, value=None):
		searched = []
		if type == None:
			for i, token in enumerate(self.tokens):
				if token.value == value:
					searched.append({"index":i, "value":token})
		else:
			for i, token in enumerate(self.tokens):
				if token.type == type:
					searched.append({"index":i, "value":token})
		return searched
	def get(self, index):
		if len(self.tokens) > index:
			return self.tokens[index]
		else:
			return None
	
	def set(self, index, value):
		if len(self.tokens) > index:
			self.tokens[index] = value
		else:
			return False
	
	def __len__(self):
		return len(self.tokens)