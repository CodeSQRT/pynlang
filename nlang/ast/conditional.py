from lib.detect import *
class ConditionalStatement:
	def __init__(self, operation, expr):
		self.expr = expr

	def eval(self):
		return self.expr.eval()

class ConditionalExpression:
	def __init__(self, operation=None, expr1=None, expr2=None, _type=None):
		self._type = _type
		self.operation = operation
		self.expr1 = expr1
		self.expr2 = expr2
	def eval(self):
		if self._type == OPERATORS_ELSE: return True
		if self.operation == LESS: return (self.expr1.eval() < self.expr2.eval())
		elif self.operation == GREATER: return (self.expr1.eval() > self.expr2.eval())
		elif self.operation == EQEQUAL: return (self.expr1.eval() == self.expr2.eval())
		elif self.operation == AMPAMP:
			return self.expr1.eval() and self.expr2.eval()
		elif self.operation == VBARVBAR:
			return self.expr1.eval() or self.expr2.eval()