from lib.detect import *
import nlang.nobjects
import nlang.tabmanager
def OptimizeOneLine(lexedline):
	for i, token in enumerate(lexedline.tokens):
		if token.type == EQUAL:
			if lexedline.tokens[i + 1].type == EQUAL:
				lexedline.tokens[i].type = EQEQUAL
				lexedline.tokens[i].value = "=="
				del lexedline.tokens[i + 1]
		if token.type == VBAR:
			if lexedline.tokens[i + 1].type == VBAR:
				lexedline.tokens[i].type = VBARVBAR
				lexedline.tokens[i].value = "||"
				del lexedline.tokens[i + 1]
		if token.type == AMPER:
			if lexedline.tokens[i + 1].type == AMPER:
				lexedline.tokens[i].type = AMPAMP
				lexedline.tokens[i].value = "&&"
				del lexedline.tokens[i + 1]
	tpl = LexedLine_Template(lexedline)
	lexedline.tpl = tpl
	return lexedline

def OptimizeMultipleLines(lexedlines):

	self = nlang.nobjects.Buffer()
	self.lexedlines = lexedlines
	self.first = None
	def one(i, lexedline):
		if lexedline.tpl == CLASS_DECLARATION or lexedline.tpl == FUNCTION_DECLARATION:
			lexedline.tokens[0] = nlang.nobjects.Token(lexedline.get(0).value, lexedline.tpl)
			index = lexedline.search(type=DOLLAR)[0]['index']
			lexedline.get(index).type = LBRACE
			lexedline.get(index).value = "{"
			self.lbrace += 1
			try:
				while True:
					if lexedline.tpl == FUNCTION_DECLARATION:
						if self.first is not CLASS_DECLARATION:
							if self.lexedlines[i + 1].tabs <= lexedline.tabs:
								return
					if self.lexedlines[i + 1].tabs < lexedline.tabs:
						return
					if one(i + 1, self.lexedlines[i + 1]):
						self.tabs = lexedline.tabs
					else:
						break
			except:
				pass
			try:
				lexedline.tokens += self.lexedlines[i + 1].tokens
				del self.lexedlines[i + 1]
			except:
				pass
		elif lexedline.tabs > self.tabs:
			self.lexedlines[i - 1].tokens += lexedline.tokens
			del self.lexedlines[i]
			index = lexedline.search(type=DOLLAR)[0]['index']
			lexedline.get(index).type = DOTCOMMA
			lexedline.get(index).value = ";"
			return True
		else:
			lexedline.insert(nlang.nobjects.Token("}", RBRACE))
			self.rbrace += 1
			return False

	def main():
		for i, lexedline in enumerate(self.lexedlines):
			if lexedline.tpl == CLASS_DECLARATION or lexedline.tpl == FUNCTION_DECLARATION:
				self.tabs = 0
				self.lbrace = 0
				self.rbrace = 0

				self.first = lexedline.tpl
				one(i, lexedline)
				for i, token in enumerate(lexedline.tokens):
					if i > 0:
						if lexedline.get(i - 1).type == DOTCOMMA and token.type == FUNCTION_DECLARATION:
							lexedline.tokens = lexedline.tokens[:i] + [nlang.nobjects.Token("}", RBRACE)] + lexedline.tokens[i:]
							self.rbrace += 1
				while self.lbrace > self.rbrace:
					lexedline.insert(nlang.nobjects.Token("}", RBRACE))
					self.rbrace += 1
				lexedline.insert(nlang.nobjects.Token("$", DOLLAR))
		return self.lexedlines



	return main()