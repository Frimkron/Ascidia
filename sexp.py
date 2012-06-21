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
	def __eq__(self,other):
		return isinstance(other,Symbol) and other.name==self.name


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
				yield (T_RPAREN,None)
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
		if len(stack) > 0:
			raise ParseError("Unmatched left parenthesis")
				
	try:
		ttype,tval = tokens.next()
		raise ParseError("Unexpected %s after document" % str(ttype))
	except StopIteration: pass
	
	return retval


def _parse(input,tkz,prs):
	try:
		buffer = input.read(1024)
	except AttributeError:
		ir = iter(input)
	else:
		def adapter(buffer):
			while buffer != "":
				for c in buffer: yield c
				buffer = input.read(1024)
		ir = adapter(buffer)
	return prs(tkz(ir))
	
	
def parse(input):
	"""Parses the given sequence, iterator or stream of characters
		into a parse tree of nested tuples"""
	return _parse(input,tokenize,parse_tokens)
				

if __name__ == "__main__":
	import unittest
	import mock
	import io

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
		
		def test_ignores_whitespace(self):
			t = tokenize(iter(" \t\n\r"))
			with self.assertRaises(StopIteration):
				t.next()
				
		def test_tokenizes_l_paren(self):
			t = tokenize(iter("("))
			result = t.next()
			self.assertEquals((T_LPAREN,None),result)
	
		def test_tokenizes_r_paren(self):
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
		
		def test_ends_int_on_l_paren(self):
			t = tokenize(iter("99("))
			result = t.next()
			self.assertEquals((T_NUMBER,"99"),result)
			result = t.next()
			self.assertEquals((T_LPAREN,None),result)	
		
		def test_ends_int_on_r_paren(self):
			t = tokenize(iter("99)"))
			result = t.next()
			self.assertEquals((T_NUMBER,"99"),result)
			result = t.next()
			self.assertEquals((T_RPAREN,None),result)
			
		def test_ends_int_on_whitespace(self):
			t = tokenize(iter("99\t"))
			result = t.next()
			self.assertEquals((T_NUMBER,"99"),result)
		
		def test_int_becomes_symbol_if_contains_non_digit(self):
			t = tokenize(iter("1234abc"))
			result = t.next()
			self.assertEquals((T_SYMBOL,"1234abc"),result)
			
		def test_tokenizes_positive_integer(self):
			t = tokenize(iter("+12"))
			result = t.next()
			self.assertEquals((T_NUMBER,"+12"), result)
			
		def test_tokenizes_negative_integer(self):
			t = tokenize(iter("-12"))
			result = t.next()
			self.assertEquals((T_NUMBER,"-12"),result)
		
		def test_number_becomes_symbol_if_missing_digits_after_sign(self):
			t = tokenize(iter("+"))
			result = t.next()
			self.assertEquals((T_SYMBOL,"+"),result)

		def test_number_becomes_symbol_if_l_paren_after_sign(self):
			t = tokenize(iter("+("))
			self.assertEquals((T_SYMBOL,"+"),t.next())
			self.assertEquals((T_LPAREN,None),t.next())
			
		def test_number_becomes_symbol_if_r_paren_after_sign(self):
			t = tokenize(iter("+)"))
			self.assertEquals((T_SYMBOL,"+"),t.next())
			self.assertEquals((T_RPAREN,None),t.next())
			
		def test_number_becomes_symbol_if_whitespace_after_sign(self):
			t = tokenize(iter("+\n"))
			self.assertEquals((T_SYMBOL,"+"),t.next())
			
		def test_tokenizes_single_decimal_place(self):
			t = tokenize(iter("12.1"))
			result = t.next()
			self.assertEquals((T_NUMBER,"12.1"),result)
			
		def test_tokenizes_multiple_decimal_places(self):
			t = tokenize(iter("99.0123456789"))
			result = t.next()
			self.assertEquals((T_NUMBER,"99.0123456789"),result)
		
		def test_ends_float_on_l_paren(self):
			t = tokenize(iter("99.12("))
			result = t.next()
			self.assertEquals((T_NUMBER,"99.12"),result)
			result = t.next()
			self.assertEquals((T_LPAREN,None),result)
			
		def test_ends_float_on_r_paren(self):
			t = tokenize(iter("99.12)"))
			result = t.next()
			self.assertEquals((T_NUMBER,"99.12"),result)
			result = t.next()
			self.assertEquals((T_RPAREN,None),result)
			
		def test_ends_float_on_whitespace(self):
			t = tokenize(iter("99.12\r"))
			result = t.next()
			self.assertEquals((T_NUMBER,"99.12"),result)
		
		def test_number_becomes_symbol_if_missing_decimal_places(self):
			t = tokenize(iter("123."))
			result = t.next()
			self.assertEquals((T_SYMBOL,"123."),result)
				
		def test_number_becomes_symbol_if_l_paren_before_decimal_places(self):
			t = tokenize(iter("123.("))
			self.assertEquals((T_SYMBOL,"123."),t.next())
			self.assertEquals((T_LPAREN,None),t.next())
				
		def test_number_becomes_symbol_if_r_paren_before_decimal_places(self):
			t = tokenize(iter("123.)"))
			self.assertEquals((T_SYMBOL,"123."),t.next())
			self.assertEquals((T_RPAREN,None),t.next())
				
		def test_number_becomes_symbol_if_whitespace_before_decimal_places(self):
			t = tokenize(iter("123. "))
			self.assertEquals((T_SYMBOL,"123."),t.next())
		
		def test_number_becomes_symbol_if_non_digit_in_decimal(self):
			t = tokenize(iter("123.lol"))
			self.assertEquals((T_SYMBOL,"123.lol"),t.next())	

		def test_tokenizes_empty_string(self):
			t = tokenize(iter('""'))
			self.assertEquals((T_STRING,''),t.next())
			
		def test_tokenizes_non_empty_string(self):
			t = tokenize(iter('"foo"'))
			self.assertEquals((T_STRING,'foo'),t.next())

		def test_errors_for_unclosed_string(self):
			with self.assertRaises(ParseError):
				t = tokenize(iter('"foo'))
				t.next()
				
		def test_allows_whitespace_in_string(self):
			t = tokenize(iter('"foo \n\r\tbar"'))
			self.assertEquals((T_STRING,'foo \n\r\tbar'),t.next())
			
		def test_allows_l_paren_in_string(self):
			t = tokenize(iter('"("'))
			self.assertEquals((T_STRING,'('),t.next())
		
		def test_allows_r_paren_in_string(self):
			t = tokenize(iter('")"'))
			self.assertEquals((T_STRING,')'),t.next())
			
		def test_can_escape_quote_in_string(self):
			t = tokenize(iter('"\\""'))
			self.assertEquals((T_STRING,'"'),t.next())
			
		def test_can_escape_backslash_in_string(self):
			t = tokenize(iter('"\\\\"'))
			self.assertEquals((T_STRING,'\\'),t.next())

		def test_can_use_newline_escape_in_string(self):
			t = tokenize(iter('"\\n"'))
			self.assertEquals((T_STRING,'\n'),t.next())
			
		def test_can_use_carriage_return_escape_in_string(self):
			t = tokenize(iter('"\\r"'))
			self.assertEquals((T_STRING,'\r'),t.next())
			
		def test_can_use_tab_escape_in_string(self):
			t = tokenize(iter('"\\t"'))
			self.assertEquals((T_STRING,'\t'),t.next())
			
		def test_removes_other_escapes_in_string(self):
			t = tokenize(iter('"foo\\qbar"'))
			self.assertEquals((T_STRING,'foobar'),t.next())
			
		def test_errors_for_incomplete_string_escape(self):
			with self.assertRaises(ParseError):
				t = tokenize(iter('"\\'))
				t.next()
				
		def test_tokenizes_symbol(self):
			t = tokenize(iter("*@#~&$!"))
			self.assertEquals((T_SYMBOL,"*@#~&$!"),t.next())
			
		def test_ends_symbol_on_l_paren(self):
			t = tokenize(iter("@@@("))
			self.assertEquals((T_SYMBOL,"@@@"),t.next())
			self.assertEquals((T_LPAREN,None),t.next())
			
		def test_ends_symbol_on_r_paren(self):
			t = tokenize(iter("~~~)"))
			self.assertEquals((T_SYMBOL,"~~~"),t.next())
			self.assertEquals((T_RPAREN,None),t.next())
			
		def test_ends_symbol_on_whitespace(self):
			t = tokenize(iter("&&&\t"))
			self.assertEquals((T_SYMBOL,"&&&"),t.next())


	class TestParseTokens(unittest.TestCase):
		
		def test_parses_empty_token_stream(self):
			result = parse_tokens(iter([]))
			self.assertEquals(None, result)
		
		def test_parses_single_integer(self):
			result = parse_tokens(iter([(T_NUMBER,"12")]))
			self.assertEquals(12, result)

		def test_parses_single_float(self):
			result = parse_tokens(iter([(T_NUMBER,"99.42")]))
			self.assertEquals(99.42, result)
			
		def test_parses_single_string(self):
			result = parse_tokens(iter([(T_STRING,"foobar")]))
			self.assertEquals("foobar",result)
	
		def test_parses_single_symbol(self):
			result = parse_tokens(iter([(T_SYMBOL,"***")]))
			self.assertEquals(Symbol("***"),result)
			
		def test_parses_single_empty_list(self):
			result = parse_tokens(iter([(T_LPAREN,None),(T_RPAREN,None)]))
			self.assertEquals((),result)
			
		def test_errors_for_more_than_one_item(self):
			with self.assertRaises(ParseError):
				parse_tokens(iter([(T_STRING,"baz"),(T_NUMBER,"2")]))
				
		def test_errors_for_unmatched_l_paren(self):
			with self.assertRaises(ParseError):
				parse_tokens(iter([(T_LPAREN,None)]))
		
		def test_errors_for_unmatched_r_paren(self):
			with self.assertRaises(ParseError):
				parse_tokens(iter([(T_RPAREN,None)]))
				
		def test_parses_list_with_single_item(self):
			result = parse_tokens(iter([(T_LPAREN,None),(T_NUMBER,"9"),(T_RPAREN,None)]))
			self.assertEquals((9,), result)
			
		def test_parses_list_with_multiple_items(self):
			result = parse_tokens(iter([(T_LPAREN,None),(T_STRING,"blah"),
				(T_NUMBER,"42"),(T_SYMBOL,"^_^"),(T_RPAREN,None)]))
			self.assertEquals(("blah",42,Symbol("^_^")),result)
			
		def test_parses_nested_list(self):
			result = parse_tokens(iter([(T_LPAREN,None),(T_NUMBER,"66"),
				(T_LPAREN,None),(T_STRING,"hi"),(T_RPAREN,None),(T_RPAREN,None)]))
			self.assertEqual((66,("hi",)), result)
			
		def test_errors_for_unmatched_l_paren_in_nested(self):
			with self.assertRaises(ParseError):
				result = parse_tokens(iter([(T_LPAREN,None),(T_LPAREN,None),
					(T_RPAREN,None)]))
					
		def test_errors_for_unmatched_r_paren_in_nested(self):
			with self.assertRaises(ParseError):
				result = parse_tokens(iter([(T_LPAREN,None),(T_LPAREN,None),
					(T_RPAREN,None),(T_RPAREN,None),(T_RPAREN,None)]))


	class TestParse(unittest.TestCase):

		def test_feeds_tokenize_result_to_parser(self):
			FOO = object()
			psr = mock.Mock()
			_parse("foo", lambda x: FOO, psr)
			psr.assert_called_once_with(FOO)

		def test_returns_parser_result(self):
			FOO = object()
			BAR = object()
			self.assertEquals(FOO, _parse("foo", lambda x: BAR, 
				lambda x: FOO))
			
		def test_passes_iter_to_tokenize(self):
			citr = [None]
			def set_citr(x):
				citr[0] = x
			tkz = mock.Mock()
			tkz.side_effect = set_citr
			_parse(iter("foo"), tkz, mock.Mock())
			self.assertIsNotNone(citr[0])
			self.assertEquals("f",citr[0].next())
			self.assertEquals("o",citr[0].next())
			self.assertEquals("o",citr[0].next())
			with self.assertRaises(StopIteration):
				citr[0].next()
			
		def test_passes_iter_from_iterable_to_tokenize(self):
			citr = [None]
			def set_citr(x): 
				citr[0] = x
			tkz = mock.Mock()
			tkz.side_effect = set_citr
			_parse("foo", tkz, mock.Mock())
			self.assertIsNotNone(citr[0])
			self.assertEquals("f",citr[0].next())
			self.assertEquals("o",citr[0].next())
			self.assertEquals("o",citr[0].next())
			with self.assertRaises(StopIteration):
				citr[0].next()
				
		def test_passes_iter_from_filelike_to_tokenize(self):
			citr = [None]
			def set_citr(x):
				citr[0] = x
			tkz = mock.Mock()
			tkz.side_effect = set_citr
			_parse(io.BytesIO("foo"), tkz, mock.Mock())
			self.assertIsNotNone(citr[0])
			self.assertEquals("f",citr[0].next())
			self.assertEquals("o",citr[0].next())
			self.assertEquals("o",citr[0].next())
			with self.assertRaises(StopIteration):
				citr[0].next()
				
		def test_iter_from_filelike_buffers_1k(self):
			citr = [None]
			def set_citr(x):
				citr[0] = x
			tkz = mock.Mock()
			tkz.side_effect = set_citr
			flike = mock.Mock()
			flike.read.side_effect = ("p"*1024,"q"*10,"")
			_parse(flike, tkz, mock.Mock())
			self.assertIsNotNone(citr[0])
			for i in citr[0]: pass
			self.assertEquals(3, flike.read.call_count)
			self.assertEquals(((1024,),{}), flike.read.call_args_list[0])
			self.assertEquals(((1024,),{}), flike.read.call_args_list[1])
			self.assertEquals(((1024,),{}), flike.read.call_args_list[2])
			
		
	unittest.main()
			
			
