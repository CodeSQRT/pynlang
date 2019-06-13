from .base import *
from lib.detect import *
class BinaryExpression:
	def __init__(self, _type, expr1, expr2):
		self._type = _type
		self.expr1 = expr1
		self.expr2 = expr2

	def eval(self):
		if self._type == PLUS:
			return self.expr1.eval() + self.expr2.eval()
		elif self._type == MINUS:
			return self.expr1.eval() - self.expr2.eval()
		elif self._type == STAR:
			return self.expr1.eval() * self.expr2.eval()
		elif self._type == SLASH:
			val1 = self.expr1.eval()
			val2 = self.expr2.eval()
			result = val1 / val2
			if "." in str(result):
				splitted = str(result).split(".")
				for letter in splitted[1]:
					if letter != "0":
						return float(result)
				return int(result)
			else:
				return int(result)