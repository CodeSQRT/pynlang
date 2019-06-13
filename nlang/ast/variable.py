class VariableExpression:
	def __init__(self, vm, type, varname):
		self.vm = vm
		self.varname = varname
	def eval(self):
		return self.vm.get(self.varname)