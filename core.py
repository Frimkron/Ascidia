"""	
Main import stuff
"""

from collections import namedtuple


CHAR_H_RATIO = 2.0

Line = namedtuple("Line","a b z stroke w stype")
Rectangle = namedtuple("Rectangle","a b z stroke w stype fill")
Ellipse = namedtuple("Ellipse", "a b z stroke w stype fill")
Arc = namedtuple("Arc","a b z start end stroke w stype fill")
Text = namedtuple("Text","pos z text colour size")
QuadCurve = namedtuple("QuadCurve","a b c z stroke w stype")

STROKE_SOLID = object()
STROKE_DASHED = object()

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

END_OF_INPUT = "\x00"

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
		
	def matcher(self):
		yield
 		self.reject()
		
	def reject(self):
		raise PatternRejected()
		
	def occupied(self):
		return self.curr.meta & M_OCCUPIED
		
	def expect(self,chars,meta=M_OCCUPIED):
		if self.occupied() or not self.curr.char in chars:
			self.reject()
		else:
			return meta		

	def offset(self,x,y,pos=None):	
		if pos is None: pos = (self.curr.col,self.curr.row)
		return (pos[0]+x,pos[1]+y)

	def await_pos(self,pos):
		while (self.curr.col,self.curr.row) != pos:
			if self.curr.row > pos[1] or self.curr.char == END_OF_INPUT:
				raise NoSuchPosition(pos)
			yield M_NONE
			
	def test(self,currentchar):
		try:
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

