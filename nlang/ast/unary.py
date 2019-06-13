from .base import *
from lib.detect import *
class UnaryExpression(Expression):
	def __init__(self, operation, expr1):
		if operation == MINUS:
			self.value = -expr1.eval()
		else:
			self.value = expr1.eval()
	def eval(self):
		return self.value