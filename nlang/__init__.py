from lib import *
import nlang.lexer
import nlang.parser
import nlang.tabmanager
import nlang.ast
import nlang.optimizer
class TestNvm:
	def __init__(self):
		self._dict = dict()
		self._dict['PI'] = 3.14
	def push(self, variable, value):
		self._dict[variable] = value
	def get(self, variable):
		return self._dict.get(variable)

class NLang:
	def __init__(self, filename):
		self.textlines = list()
		for i, line in enumerate(str(open(filename, encoding="utf-8").read()).split("\n")):
			if len(line) > 0:
				self.textlines.append(line + "\n")

		self.lexedlines = []

	def runner(self):
		vm = TestNvm()
		parser = nlang.parser.Parser(vm)
		tab_manager = nlang.tabmanager.TabManager()

		for line in self.lexedlines:
			for exp in parser.oneline(line):
				exp.eval()

	def translator(self):
		vm = TestNvm()
		parser = nlang.parser.Parser(vm)

		for line in self.lexedlines:
			for exp in parser.oneline(line):
				# exp.eval()
				if hasattr(exp, "translate"):
					print("Трансляция")
					print(exp.translate())
				else:
					exp.eval()


	def run(self):
		for line in self.textlines:
			lexedline = nlang.lexer.Lexer(line).tokenize()
			if lexedline != None:
				lexedline.insert(nlang.nobjects.Token("$", DOLLAR))
				self.lexedlines.append(lexedline)

		for i, line in enumerate(self.lexedlines):
			self.lexedlines[i] = nlang.optimizer.OptimizeOneLine(line)

		self.lexedlines = nlang.optimizer.OptimizeMultipleLines(self.lexedlines)
		# print(self.lexedlines[0])
		for line in self.lexedlines:
			for token in line.tokens:
		# 		print(f"[{NToken_ConstantName(token.type)}:\"{token.value}\"]", end="")
				print(f"{token.value}", end="")
		# 	# print(f"Табы: {line.tabs}")
			print()
		# 	print()
		# self.runner()
