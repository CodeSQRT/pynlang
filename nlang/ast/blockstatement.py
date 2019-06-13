class BlockStatement:
	def __init__(self, vm, statements):
		self.statements = statements
		self.vm = vm
	
	def eval(self):
		for statement in self.statements:
			statement.eval()