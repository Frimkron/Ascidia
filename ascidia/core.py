"""     
Main import stuff
"""

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

class NonChar:
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


class Pattern:
    """Pattern base class with utility methods"""
    
    gen = None
    is_finished = False
    curr = None
    
    def __init__(self):
        self.curr = None
        self.gen = self.matcher()
        next(self.gen)
        
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
