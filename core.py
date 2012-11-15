"""	
Copyright (c) 2012 Mark Frimston

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

----------------------------------------------------
	
Main import stuff
"""

#import mrf.ascii
from collections import namedtuple


CHAR_H_RATIO = 2.0

Line = namedtuple("Line","a b z stroke salpha w stype")
Rectangle = namedtuple("Rectangle","a b z stroke salpha w stype fill falpha")
Ellipse = namedtuple("Ellipse", "a b z stroke salpha w stype fill falpha")
Arc = namedtuple("Arc","a b z start end stroke salpha w stype fill falpha")
Text = namedtuple("Text","pos z text colour alpha size")
QuadCurve = namedtuple("QuadCurve","a b c z stroke salpha w stype")
Polygon = namedtuple("Polygon","points z stroke salpha w stype fill falpha")

STROKE_SOLID = object()
STROKE_DASHED = object()

C_FOREGROUND = object()
C_BACKGROUND = object()

M_NONE = 0
M_OCCUPIED = (1<<0)
M_BOX_START_S = (1<<1)
M_BOX_AFTER_S = (1<<2)
M_BOX_START_E = (1<<3)
M_BOX_AFTER_E = (1<<4)
M_LINE_START_E = (1<<5)
M_DASH_START_E = (1<<6)
M_LINE_AFTER_E = (1<<7)
M_DASH_AFTER_E = (1<<8)
M_LINE_START_S = (1<<9)
M_DASH_START_S = (1<<10)
M_LINE_AFTER_S = (1<<11)
M_DASH_AFTER_S = (1<<12)
M_LINE_START_SE = (1<<13)
M_DASH_START_SE = (1<<14)
M_LINE_AFTER_SE = (1<<15)
M_DASH_AFTER_SE = (1<<16)
M_LINE_START_SW = (1<<17)
M_DASH_START_SW = (1<<18)
M_LINE_AFTER_SW = (1<<19)
M_DASH_AFTER_SW = (1<<20)

class NonChar(object):
	def isalnum(self): return False
	def isalpha(self): return False
	def isdigit(self): return False
	def islower(self): return False
	def isspace(self): return False
	def istitle(self): return False
	def isupper(self): return False

START_OF_INPUT = NonChar()
END_OF_INPUT = NonChar()

class PatternRejected(Exception): pass
class PatternStateError(Exception): pass
class NoSuchPosition(Exception): pass


class Pattern(object):
	"""Pattern base class with utility methods"""
	
	gen = None
	is_finished = False
	curr = None
	
	def __init__(self):
		self.curr = None
		self.gen = self.matcher()
		self.gen.next()
		#self.debug_canvas = mrf.ascii.Canvas()
		
	def matcher(self):
		yield
 		self.reject()
		
	def reject(self):
		raise PatternRejected()
		
	def occupied(self):
		return self.curr.meta & M_OCCUPIED
		
	def expect(self,chars,meta=M_OCCUPIED):
		if self.occupied() or not self.is_in(self.curr.char,chars):
			self.reject()
		else:
			return meta		

	def offset(self,x,y,pos=None):	
		if pos is None: pos = (self.curr.col,self.curr.row)
		return (pos[0]+x,pos[1]+y)

	def await_pos(self,pos):
		while (self.curr.col,self.curr.row) != pos:
			if( self.curr.row > pos[1] 
					or (self.curr.row == pos[1] and self.curr.col > pos[0])
					or self.curr.char == END_OF_INPUT ):
				raise NoSuchPosition(pos)
			yield M_NONE
			
	def is_in(self,c,chars):
		try:
			return c in chars
		except TypeError:
			return False
			
	def test(self,currentchar):
		try:
			#if currentchar.char != "\n":
			#	self.debug_canvas.set(currentchar.col,currentchar.row,
			#		currentchar.char if currentchar.char != " " else "*")
			return self.gen.send(currentchar)
		except StopIteration:
			self.is_finished = True
			raise
		except NoSuchPosition as e:
			raise PatternRejected(e)
		
	def render(self):
		if not self.is_finished: 
			raise PatternStateError("Pattern not matched")
		return []
		
	#def debug(self):
	#	self.debug_canvas.print_out()

