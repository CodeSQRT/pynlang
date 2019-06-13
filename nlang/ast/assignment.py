class AssignmentStatement:
	def __init__(self, vm, variable, expr1):
		self.vm = vm
		self.variable = variable
		self.expr1 = expr1
	def eval(self):
		self.vm.push(self.variable, self.expr1.eval())
		return ""

	def __str__(self):
		return str(f"{self.variable}:{self.expr1}")