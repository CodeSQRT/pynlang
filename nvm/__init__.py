from .utils import ConstantDict
from . import detect

class Nvm:
	def __init__(self, text=None, filename=None):

		if filename != None:
			self.text = open(filename, encoding="utf-8").read().replace("	", "").split("\n")
		elif text != None:
			self.text = text.split("\n")

		self.defaults = dict({"null":{"type":13, "value":0}})
		self.variables = dict(self.defaults)
		self.stack = list()
		self.entry = "start"

		self.call_func_name = None

		self.func = None
		self.ret = False
	
	def call(self):
		for line in self.text:
			if line != "":
				self.check(line)

		for line in self.text:
			if line != "":
				self.check(line)
				if self.func == self.call_func_name:
					self.execute(line)
	
	def start(self):
		for line in self.text:
			if line != "":
				self.check(line)

		for line in self.text:
			if line != "":
				self.check(line)
				print(self.func)
				if self.func == self.entry:
					self.execute(line)

	def lex(self, line):
		if " " in line:
			allsp = line.split(" ", maxsplit=1)
			tagword = detect.NvmLexer_TagWord(allsp[0])
			res = str()
			for ch in allsp[1]:
				if ch != ';': res += ch
				else:
					break
			allsp[1] = str(res)
			if len(allsp) > 0:
				if "," in allsp[1]:
					args = allsp[1].split(",")
				else:
					args = [allsp[1]]
			else:
				args = []
		else:
			tagword = detect.NvmLexer_TagWord(line)
			args = []
		return dict(tagword=tagword, args=args)

	def run(self, line):
		def string(value):
			for i, char in enumerate(value):
				try:
					if i == 0 or i == len(value) - 1:
						if value[i] == '"':
							value = value[:i] + "" + value[i+1:]
				except Exception as e:
					print(e)
			return value
		if line['tagword'] == detect.MOV:
			value = line['args'][1]
			_type = detect.NvmLexer_TagWord(line['args'][2])
			if _type == detect.FLOAT:
				value = float(value)
			elif _type == detect.INT:
				value = int(value)
			elif _type == detect.STRING:
				value = string(value)
			elif _type == detect.VARIABLE:
				value = self.variables.get(value)
				if value['type'] == detect.FLOAT:
					value = float(value['value'])
				elif value['type'] == detect.INT:
					value = int(value['value'])
				elif value['type'] == detect.STRING:
					value = string(value['value'])
			self.variables[line['args'][0]] = dict(type=_type, value=value)

		elif line['tagword'] == detect.ADD:
			variable = self.variables.get(line['args'][0])
			value = line['args'][1]
			valtype = detect.NvmLexer_TagWord(line['args'][2])
			if variable == None:
				return "Does not exists"
			# if valtype == variable['type'] or valtype == detect.VARIABLE:

			if valtype != detect.VARIABLE:
				if valtype == detect.FLOAT:
					value = float(value)
				elif valtype == detect.INT:
					value = int(value)
				elif valtype == detect.STRING:
					value = string(value)
				val = dict(value=value, type=valtype)
			elif valtype == detect.VARIABLE:
				val = self.variables.get(value)

			if variable['type'] == detect.STRING and val['type'] == detect.INT:
				self.variables[line['args'][0]]['value'] += string(str(val['value']))
			else:
				self.variables[line['args'][0]]['value'] += val['value']
		elif line['tagword'] == detect.SUB:
			variable = self.variables.get(line['args'][0])
			value = line['args'][1]
			valtype = detect.NvmLexer_TagWord(line['args'][2])
			if variable == None:
				return "Does not exists"
			if valtype == variable['type'] or valtype == detect.VARIABLE:
				if valtype != detect.VARIABLE:
					if variable['type'] == detect.FLOAT:
						value = float(value)
					elif variable['type'] == detect.INT:
						value = int(value)
					elif variable['type'] == detect.STRING:
						value = string(value)
				elif valtype == detect.VARIABLE:
					value = self.variables.get(value)
					if value['type'] == detect.FLOAT:
						value = float(value['value'])
					elif variable['type'] == detect.INT:
						value = int(value['value'])
					elif variable['type'] == detect.STRING:
						value = string(value['value'])
				self.variables[line['args'][0]]['value'] -= value
			else:
				return "Different Types"
		elif line['tagword'] == detect.MUL:
			variable = self.variables.get(line['args'][0])
			value = line['args'][1]
			valtype = detect.NvmLexer_TagWord(line['args'][2])
			if variable == None:
				return "Does not exists"
			if valtype == variable['type'] or valtype == detect.VARIABLE:
				if valtype != detect.VARIABLE:
					if variable['type'] == detect.FLOAT:
						value = float(value)
					elif variable['type'] == detect.INT:
						value = int(value)
					elif variable['type'] == detect.STRING:
						value = string(value)
				elif valtype == detect.VARIABLE:
					value = self.variables.get(value)
					if value['type'] == detect.FLOAT:
						value = float(value['value'])
					elif variable['type'] == detect.INT:
						value = int(value['value'])
					elif variable['type'] == detect.STRING:
						value = string(value['value'])

				self.variables[line['args'][0]]['value'] *= value
			else:
				return "Different Types"
		elif line['tagword'] == detect.DIV:
			variable = self.variables.get(line['args'][0])
			value = line['args'][1]
			valtype = detect.NvmLexer_TagWord(line['args'][2])
			if variable == None:
				return "Does not exists"
			if valtype == variable['type'] or valtype == detect.VARIABLE:
				if valtype != detect.VARIABLE:
					if variable['type'] == detect.FLOAT or valtype == detect.FLOAT:
						value = float(value)
					elif variable['type'] == detect.INT or valtype == detect.INT:
						value = int(value)
					elif variable['type'] == detect.STRING:
						value = string(value)
				elif valtype == detect.VARIABLE:
					value = self.variables.get(value)
					if value['type'] == detect.FLOAT:
						value = float(value['value'])
					elif value['type'] == detect.INT:
						value = int(value['value'])
					elif value['type'] == detect.STRING:
						value = string(value['value'])

				self.variables[line['args'][0]]['value'] /= value

				if variable['type'] == detect.FLOAT or valtype == detect.FLOAT:
					self.variables[line['args'][0]]['value'] = float(self.variables[line['args'][0]]['value'])
				elif variable['type'] == detect.INT or valtype == detect.INT:
					self.variables[line['args'][0]]['value'] = int(self.variables[line['args'][0]]['value'])
				elif variable['type'] == detect.STRING:
					self.variables[line['args'][0]]['value'] = string(self.variables[line['args'][0]]['value'])
			else:
				return "Different Types"

		elif line['tagword'] == detect.STD:
			value = line['args'][1]
			_type = detect.NvmLexer_TagWord(line['args'][2])

			if _type == detect.FLOAT:
				value = float(value)
			elif _type == detect.INT:
				value = int(value)
			elif _type == detect.STRING:
				value = string(value)
			elif _type == detect.VARIABLE:
				value = self.variables.get(value)
				if value['type'] == detect.FLOAT:
					value = float(value['value'])
				elif value['type'] == detect.INT:
					value = int(value['value'])
				elif value['type'] == detect.STRING:
					value = string(str(value['value']))

			if line['args'][0] == "in":
				self.variables[line['args'][2]] = dict(type=detect.STRING)
				self.variables[line['args'][2]]['value'] = input(string(str(value)))
			else:
				print(str(value))

		elif line['tagword'] == detect.PUSH:
			value = line['args'][0]
			_type = detect.NvmLexer_TagWord(line['args'][1])
			if _type == detect.FLOAT:
				value = float(value)
			elif _type == detect.INT:
				value = int(value)
			elif _type == detect.STRING:
				value = string(value)
			elif _type == detect.VARIABLE:
				value = self.variables.get(value)
				if value['type'] == detect.FLOAT:
					value = float(value['value'])
				elif variable['type'] == detect.INT:
					value = int(value['value'])
				elif variable['type'] == detect.STRING:
					value = string(value['value'])
			self.stack.append(dict(
				value=value, type=_type
			))
		elif line['tagword'] == detect.CALL:
			funcname = str(self.func)
			variables = dict(self.variables)

			self.variables = dict(self.defaults)
			self.variables['ret'] = self.variables['null']
			self.variables['argc'] = variables['argc']
			for key, value in self.variables.items():
				if "arg" in key:
					self.variables[key] = value

			# print(self.variables)
			self.call_func_name = line['args'][0]
			print(f"Вызываем {self.call_func_name}")
			self.call()
			print(f"Возвращаемся на {funcname} с переменными {variables}")

			self.call_func_name = None

			self.func = str(funcname)
			self.variables = dict(variables)
		else:
			try:
				self.execute(f"std out,{line['tagword']},var")
			except:
				return "Does Not exist"
		return True

	def check(self, line):
		if line[0] == '@':
			spl = line.split(" ")
			spl[0] = spl[0].replace("@", "")
			if spl[0] == "entry":
				self.entry = spl[1]
		elif ":" == line[len(line) - 1]:
			self.func = line.replace(":", "")
		elif ".end" in line[:4]:
			self.func = None

	def execute(self, line):
		if line[0] == ';':
			return
		return self.run(self.lex(line))