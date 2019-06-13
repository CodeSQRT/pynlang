from lib.detect import *
class StringExpression:
	def __init__(self, vm, _type, value, prefix=None):
		self._type = _type
		self.value = value
		self.vm = vm
		self.prefix = prefix
	def eval(self):
		if self.prefix == STRING_PREFIX_FORMAT:
			for key, value in self.vm._dict.items():
				self.value = self.value.replace("{" + key + "}", str(value))
		return self.value