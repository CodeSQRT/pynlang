from lib.detect import *
class DirectiveStatement:
	def __init__(self, vm, directive, expr1):
		self.vm = vm
		self.directive = directive
		self.expr1 = expr1
	def eval(self):
		if self.directive == DIRECTIVES_STDWRITE:
			print(str(self.expr1.eval()).replace("\\n", "\n"), end="")