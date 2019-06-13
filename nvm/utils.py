class ConstantDict(dict):
	def __init__(self, items):
		dict.__init__(items)

	def __setitem__(self, name, value):
		if "name" not in self.__dict__:
			raise Exception("You cant change value")