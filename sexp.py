# S-Exp parser


class Sentinel(object):
	def __init__(self,name):
		self.name = name
		globals()[self.name] = self
	def __repr__(self):
		return self.name	


Sentinel( "T_LPAREN" )
Sentinel( "T_RPAREN" )
Sentinel( "T_STRING" )
Sentinel( "T_NUMBER" )
Sentinel( "T_SYMBOL" )


class ParseError(Exception): pass


def tokenize(input):

	STATE_NORMAL = object()
	STATE_STRING = object()
	STATE_STRING_ESC = object()
	STATE_SYMBOL = object()
	STATE_INTEGER = object()
	STATE_FLOAT = object()
	WHITESPACE = (" ","\t","\n","\r")

	state = STATE_NORMAL
	buffer = ""
	
	while True:
		try:
			next = input.next()
		except StopIteration:
			next = None
		
		if state is STATE_NORMAL:
			if next == "(":
				yield (T_LPAREN,None)
			elif next == ")":
				yield (T_RPAREN,None)
			elif next == '"':
				state = STATE_STRING
			elif "0" <= next < "9":
				buffer += next
				state = STATE_INTEGER
			elif next in WHITESPACE:
				pass
			elif next is None:
				return
			else:
				buffer += next
				state = STATE_SYMBOL
				
		elif state is STATE_STRING:
			if next == "\\":
				state = STATE_STRING_ESC
			elif next == '"':
				yield (T_STRING,buffer)
				buffer = ""
				state = STATE_NORMAL
			elif next is None:
				raise ParseError("Unexpected end of input")
			else:
				buffer += next
				
		elif state is STATE_STRING_ESC:
			if next is None:
				raise ParseError("Unexpected end of input")
			elif next in ('"',"\\"):
				buffer += next
				state = STATE_STRING
			elif next == "n":
				buffer += "\n"
				state = STATE_STRING
			elif next == "r":
				buffer += "\r"
				state = STATE_STRING
			elif next == "t":
				buffer += "\t"
				state = STATE_STRING
			else:
				state = STATE_STRING
				
		elif state is STATE_INTEGER:
			if "0" <= next < "9":
				buffer += next
			elif next == ".":
				buffer += next
				state = STATE_FLOAT
			elif next in WHITESPACE:
				yield (T_NUMBER,int(buffer))
				buffer = ""
				state = STATE_NORMAL
			elif next is None:
				yield (T_NUMBER,int(buffer))
				return
			elif next == "(":
				yield (T_NUMBER,int(buffer))
				yield (T_LPAREN,None)
				buffer = ""
				state = STATE_NORMAL
			elif next == ")":
				yield (T_NUMBER,int(buffer))
				yield (T_RPAREN,None)
				buffer = ""
				state = STATE_NORMAL
			else:
				raise ParseError("Invalid number token")
				
		elif state is STATE_FLOAT:
			if "0" <= next < "9":
				buffer += next
			elif next in WHITESPACE:
				yield (T_NUMBER,float(buffer))
				buffer = ""
				state = STATE_NORMAL
			elif next == "(":
				yield (T_NUMBER,float(buffer))
				yield (T_LPAREN,None)
				buffer = ""
				state = STATE_NORMAL
			elif next == ")":
				yield (T_NUMBER,float(buffer))
				yield (T_RPAREN,None)
				buffer = ""
				state = STATE_NORMAL
			elif next is None:
				yield (T_NUMBER,float(buffer))
				return
			else:
				raise ParseError("Invalid number token")
				
		elif state is STATE_SYMBOL:
			if next in WHITESPACE:
				yield (T_SYMBOL,buffer)
				buffer = ""
				state = STATE_NORMAL
			elif next == "(":
				yield (T_SYMBOL,buffer)
				yield (T_LPAREN,None)
				buffer = ""
				state = STATE_NORMAL
			elif next == ")":
				yield (T_SYMBOL,buffer)
				yield (T_RPAREN,None)
				buffer = ""
				state = STATE_NORMAL
			elif next is None:
				yield (T_SYMBOL,buffer)
				return
			else:
				buffer += next
				
				
def parse_tokens(tokens):
	pass
