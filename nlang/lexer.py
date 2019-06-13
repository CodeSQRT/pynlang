from goto import with_goto
import nlang.nobjects
from lib.detect import *
class Lexer:
	def __init__(self, textline):
		self.textline = textline

	@with_goto
	def tokenize(self):
		lexedline = nlang.nobjects.LexedLine()
		buffer = nlang.nobjects.Buffer()
		for i, letter in enumerate(self.textline):
			if letter == "	": lexedline.tabs += 1
			else: break
		self.textline = self.textline.replace("	", "")

		for i, letter in enumerate(self.textline):
			if letter == "#":
				return None
			onechar = nlang.nobjects.NToken_OneChar(letter)
			if i + 1 < len(self.textline):
				twochars = nlang.nobjects.NToken_TwoChars(letter, self.textline[i + 1])
			else:
				twochars = None

			if (onechar in LANG_OPS):
				if (i > 0):
					if (
						onechar == NOT_DETECTED and
						NToken_OneChar(self.textline[i - 1]) == NOT_DETECTED
					): goto ._1break
					if (self.textline[i - 1] == "\\"): goto ._increment

				if len(buffer.value) > 0:
					if (buffer.value[0] == '"'):
						length = len(buffer.value)
						less = -1
						if (length == 1):
							less = 0
						if length + less < len(buffer.value):
							if (
								buffer.value[length + less] != '"'
							):
								goto ._increment
						elif length + less - 1 < len(buffer.value):
							goto ._increment

					if (buffer.value[len(buffer.value) - 1] == "."): goto ._increment

				if len(buffer.value) > 0:
					lexedline.insert(nlang.nobjects.Token(buffer.value, NToken_Keyword(buffer.value)))

				buffer.value = ""
				goto ._1break
			

			label ._1break
			if twochars != None and (twochars in STRING_PREFIXES):
				if len(buffer.value) > 0:
					if buffer.value[0] == '"':
						goto ._increment

				buffer.value = NToken_PrefixByConstant(twochars)
				if (buffer.value[0] == '"'):
					length = len(buffer.value)

					if (
						buffer.value[length - 1] != '"' or
						buffer.value[length - 2] == "\\"
					): goto ._increment
				if lexedline.get(len(lexedline.tokens) - 1).type not in STRING_PREFIXES:
					lexedline.insert(nlang.nobjects.Token(buffer.value, twochars))
					buffer.value = ""
					goto ._continue
				else:
					buffer.value = ""
					goto ._increment

			label ._increment
			buffer.value += letter

			label ._continue

		return lexedline