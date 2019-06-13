from lib.detect import *
from .ast import *
from lib import exceptions
class Parser:
	def __init__(self, vm):
		self.position = 0

		self.vm = vm
	
	def oneline(self, line):
		self.line = line
		if line.get(0).type == SKIP: return []
		result = list()
		while not self.match(DOLLAR):
			result.append(self.statement())
		self.position = 0
		self.nowlineindex = 0
		return result

	"""Тут будет рекурсивный спуск Statement"""
	def statement(self):
		return self.assignment()

	def assignment(self):
		current = self.get(0)
		if current.type == VARIABLE and self.get(2).type == EQUAL:
			variable = current.value
			self.consume(VARIABLE)
			self.consume(SPACE)
			self.consume(EQUAL)
			self.consume(SPACE)
			return AssignmentStatement(self.vm, variable, self.expression())
		return self.directive()

	def directive(self):
		current = self.get(0)
		if current.type == DIRECTIVES_STDWRITE and self.get(1).type == SPACE:
			self.consume(DIRECTIVES_STDWRITE)
			self.consume(SPACE)
			return DirectiveStatement(self.vm, current.type, self.expression())
		return self.conditional_statement()
	
	def conditional_statement(self):
		current = self.get(0)
		if current.type == OPERATORS_IF and self.get(1).type == SPACE:
			return ConditionalStatement(self.vm, self.oneconditional_statement(), self.oneconditional_statement(), self.oneconditional_statement())
		raise Exception(exceptions.UNKNOWN_CONSTRUCTION)
	
	def oneconditional_statement(self):
		current = self.get(0)
		if current.type == OPERATORS_IF or current.type == OPERATORS_ELIF and self.get(1).type == SPACE:
			return OneConditionalStatement(self.vm, self.expression(), self.block())
		return OneConditionalStatement(self.vm, True, self.body())

	def block(self):
		current = self.get(0)
		if current.type == LBRACE:
			self.consume(LBRACE)
			block = BlockStatement(self.vm, [])
			while not self.match(RBRACE):
				block.append(self.statement())
			self.consume(RBRACE)
			return block

	# def declaration(self):
	# 	current = self.get(0)
	# 	if current.type == FUNCTION_DECLARATION and self.get(1).type == SPACE and self.get(2).type == LPAR:
	# 		print("Декларация функции")
	# 		self.consume(FUNCTION_DECLARATION)
	# 		self.consume(SPACE)
	# 		self.consume(LPAR)
	# 		exit()
	# 		return FunctionStatement(self.vm, current.type, self.arguments(), self.body())

	# 	raise Exception(exceptions.UNKNOWN_CONSTRUCTION)

	#Выражения. Например, 15 == 15 или (1 - f) * 2
	def expression(self):
		return self.logicalor()

	#||
	def logicalor(self):
		result = self.logicaland()
		while True:
			if self.match(VBARVBAR):
				result = ConditionalExpression(VBARVBAR, result, self.logicaland(), _type=self.line.tokens[0].type)
				continue
			break
		return result
	# #&&
	def logicaland(self):
		result = self.equality()
		while True:
			if self.match(AMPAMP):
				result = ConditionalExpression(AMPAMP, result, self.equality(), _type=self.line.tokens[0].type)
				continue
			break
		return result

	def equality(self):
		result = self.conditional()
		while True:
			if self.match(EQEQUAL):
				result = ConditionalExpression(EQEQUAL, result, self.conditional(), _type=self.line.tokens[0].type)
				continue
			break
		return result

	def conditional(self):
		result = self.additive()
		while True:
			if self.match(LESS):
				result = ConditionalExpression(LESS, result, self.additive(), _type=self.line.tokens[0].type)
				continue
			break
		return result
	
	def additive(self):
		result = self.multiplicative()
		while True:
			if self.match(SPACE):
				pass
			if self.get(0).type == PLUS or self.get(0).type == MINUS:
				self.consume(SPACE, -1, exceptions.SPACE_REQUIRED_IN_MATH_EXPRESSIONS, incr=False)
				self.consume(SPACE, 1, exceptions.SPACE_REQUIRED_IN_MATH_EXPRESSIONS, incr=False)
			if self.match(PLUS):
				result = BinaryExpression(PLUS, result, self.multiplicative())
				continue
			if self.match(MINUS):
				result = BinaryExpression(MINUS, result, self.multiplicative())
				continue
			break
		return result

	

	def multiplicative(self):
		result = self.unary()
		while True:
			if self.match(SPACE):
				pass
			if self.get(0).type == STAR or self.get(0).type == SLASH:
				self.consume(SPACE, -1, exceptions.SPACE_REQUIRED_IN_MATH_EXPRESSIONS, incr=False)
				self.consume(SPACE, 1, exceptions.SPACE_REQUIRED_IN_MATH_EXPRESSIONS, incr=False)
			if self.match(STAR):
				result = BinaryExpression(STAR, result, self.unary())
				continue
			if self.match(SLASH):
				result = BinaryExpression(SLASH, result, self.unary())
				continue
			break
		return result

	def unary(self):

		if self.match(MINUS):
			return UnaryExpression(MINUS, self.primary())
		if self.match(PLUS):
			return self.primary()
		return self.primary()

	def primary(self):
		current = self.get(0)
		if self.match(INT) or self.match(FLOAT):
			return NumberExpression(current.type, current.value)
		if self.match(STRING_PREFIX_FORMAT):
			prefix = self.get(-1).type
			if self.match(STRING):
				string = self.get(-1)
				return StringExpression(self.vm, string.type, string.value, prefix)
		if self.match(STRING):
			return StringExpression(self.vm, current.type, current.value)
		if self.match(VARIABLE):
			return VariableExpression(self.vm, current.type, current.value)
		if self.match(LPAR):
			result = self.expression()
			self.match(RPAR)
			return result
		if self.match(SPACE):
			return self.expression()
		raise Exception(exceptions.UNKNOWN_TOKEN)
	
	def get(self, relative_pos):
		position = self.position + relative_pos
		if (position < len(self.line.tokens)):
			return self.line.tokens[position]
		else:
			return None

	def match(self, type, relative_pos=0):
		current = self.get(relative_pos)
		if current.type != type:
			return False
		self.position += 1
		return True
	
	def consume(self, type, relative_pos=0, exc=exceptions.INVALID_SYNTAX, incr=True):
		current = self.get(relative_pos)
		if current.type != type:
			raise Exception(exc)
		if incr == True:
			self.position += 1
		return current