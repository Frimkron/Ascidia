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


class Symbol(object):
	def __init__(self,name):
		self.name = name
	def __repr__(self):
		return "Symbol(%s)" % self.name


def tokenize(input):
	"""Returns an iterable which reads characters from iterable 'input'
		and will yield token 2-tuples"""

	# T_LPAREN:	(
	# T_RPAREN:	)
	# T_STRING:	"([^"\]|\\.)*"
	# T_NUMBER:	[+-]?[0-9]+(\.[0-9]+)?
	# T_SYMBOL: [^ \t\n\r()]+

	STATE_NORMAL = object()
	STATE_STRING = object()
	STATE_STRING_ESC = object()
	STATE_SYMBOL = object()
	STATE_INTEGER_START = object()
	STATE_INTEGER = object()
	STATE_FLOAT_START = object()
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
			elif next in ("-","+"):
				buffer += next
				state = STATE_INTEGER_START
			elif "0" <= next <= "9":
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
				
		elif state is STATE_INTEGER_START:
			if "0" <= next <= "9":
				buffer += next
				state = STATE_INTEGER
			elif next in WHITESPACE:
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
				state = STATE_SYMBOL
				
		elif state is STATE_INTEGER:
			if "0" <= next <= "9":
				buffer += next
			elif next == ".":
				buffer += next
				state = STATE_FLOAT_START
			elif next in WHITESPACE:
				yield (T_NUMBER,buffer)
				buffer = ""
				state = STATE_NORMAL
			elif next is None:
				yield (T_NUMBER,buffer)
				return
			elif next == "(":
				yield (T_NUMBER,buffer)
				yield (T_LPAREN,None)
				buffer = ""
				state = STATE_NORMAL
			elif next == ")":
				yield (T_NUMBER,buffer)
				yield (T_RPAREN,None)
				buffer = ""
				state = STATE_NORMAL
			else:
				buffer += next
				state = STATE_SYMBOL
				
		elif state is STATE_FLOAT_START:
			if "0" <= next <= "9":
				buffer += next
				state = STATE_FLOAT
			elif next in WHITESPACE:
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
				yield (T_LPAREN,None)
				buffer = ""
				state = STATE_NORMAL
			elif next is None:
				yield (T_SYMBOL,buffer)
				return
			else:
				buffer += next
				state = STATE_SYMBOL
				
		elif state is STATE_FLOAT:
			if "0" <= next <= "9":
				buffer += next
			elif next in WHITESPACE:
				yield (T_NUMBER,buffer)
				buffer = ""
				state = STATE_NORMAL
			elif next == "(":
				yield (T_NUMBER,buffer)
				yield (T_LPAREN,None)
				buffer = ""
				state = STATE_NORMAL
			elif next == ")":
				yield (T_NUMBER,buffer)
				yield (T_RPAREN,None)
				buffer = ""
				state = STATE_NORMAL
			elif next is None:
				yield (T_NUMBER,buffer)
				return
			else:
				buffer += next
				state = STATE_SYMBOL
				
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

	retval = None
	stack = []

	for ttype,tval in tokens:	
		
		if ttype == T_LPAREN:
			stack.append([])
			
		elif ttype == T_RPAREN:
			try:
				l = stack.pop()
			except IndexError:
				raise ParseError("Unmatched right parenthesis")
			t = tuple(l)
			if len(stack)==0:
				retval = t
				break
			stack[-1].append(t)
			
		else:
			v = {
				T_STRING: lambda v: v,
				T_NUMBER: lambda v: float(v) if "." in v else int(v),
				T_SYMBOL: lambda v: Symbol(v)
			}[ttype](tval)
			
			if len(stack)==0:
				retval = v
				break
			stack[-1].append(v)
	else:
		raise ParseError("Unmatched left parenthesis")
				
	try:
		ttype,tval = tokens.next()
		raise ParseError("Unexpected %s after document" % str(ttype))
	except StopIteration: pass
				

if __name__ == "__main__":
	import unittest

	class TestTokenize(unittest.TestCase):
		
		def test_yields_tokens(self):
			t = tokenize(iter("12"))
			result = t.next()
		
		def test_stops_iteration_at_end_of_tokens(self):
			t = tokenize(iter("12"))
			t.next()
			with self.assertRaises(StopIteration):
				t.next()
				
		def test_stops_immediately_for_no_tokens(self):
			t = tokenize(iter(""))
			with self.assertRaises(StopIteration):
				t.next()
				
		def test_tokenizes_l_paren(self):
			t = tokenize(iter("("))
			result = t.next()
			self.assertEquals((T_LPAREN,None),result)
			
		def test_tokenizes_r_parent(self):
			t = tokenize(iter(")"))
			result = t.next()
			self.assertEquals((T_RPAREN,None),result)
			
		def test_tokenizes_single_digit_integer(self):
			t = tokenize(iter("1"))
			result = t.next()
			self.assertEquals((T_NUMBER,"1"),result)
			
		def test_tokenizes_multiple_digit_integer(self):
			t = tokenize(iter("1234567890"))
			result = t.next()
			self.assertEquals((T_NUMBER,"1234567890"),result)
			
		def test_tokenizes_positive_integer(self):
			t = tokenize(iter("+12"))
			result = t.next()
			self.assertEquals((T_NUMBER,"+12"), result)
			
		def test_tokenizes_negative_integer(self):
			t = tokenize(iter("-12"))
			result = t.next()
			self.assertEquals((T_NUMBER,"-12"),result)
			
		def test_tokenizes_single_decimal_place(self):
			t = tokenize(iter("12.1"))
			result = t.next()
			self.assertEquals((T_NUMBER,"12.1"),result)
			
		def test_tokenizes_multiple_decimal_places(self):
			t = tokenize(iter("99.0123456789"))
			result = t.next()
			self.assertEquals((T_NUMBER,"99.0123456789"),result)
			
		def test_number_becomes_symbol_if_contains_letters(self):
			t = tokenize(iter("1234abc"))
			result = t.next()
			self.assertEquals((T_SYMBOL,"1234abc"),result)
				
		def test_number_becomes_symbol_if_missing_decimal_places(self):
			t = tokenize(iter("123."))
			result = t.next()
			self.assertEquals((T_SYMBOL,"123."),result)
				
		def test_number_becomes_symbol_if_missing_digits_after_sign(self):
			t = tokenize(iter("+"))
			result = t.next()
			self.assertEquals((T_SYMBOL,"+"),result)
	
	unittest.main()
			
			
