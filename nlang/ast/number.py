from lib.detect import *
class NumberExpression:
	def __init__(self, type, value):
		if type == FLOAT:
			self.value = float(value)
		elif type == INT:
			self.value = int(value)
	def eval(self):
		return self.value