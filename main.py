
import xml.dom
import xml.dom.minidom
import math
from collections import defaultdict
from collections import namedtuple

CHAR_H_RATIO = 2.0

Line = namedtuple("Line","a b z stroke w")
Rectangle = namedtuple("Rectangle","a b z stroke w fill")
Ellipse = namedtuple("Ellipse", "a b z stroke w fill")
Arc = namedtuple("Arc","a b z start end stroke w fill")
Text = namedtuple("Text","pos z text colour size")

M_NONE = 0
M_OCCUPIED = (1<<0)
M_LINE_SQ_CORNER = (1<<1)
M_BOX_TOP = (1<<2)
M_BOX_BOTTOM = (1<<3)
M_BOX_LEFT = (1<<4)
M_BOX_RIGHT = (1<<5)

END_OF_INPUT = "\x00"


class SvgOutput(object):

	CHAR_W = 12.0
	CHAR_H = CHAR_W * CHAR_H_RATIO
	STROKE_W = 2.5
	FONT_SIZE = 16.0

	@staticmethod
	def output(items,stream):
		SvgOutput.INST._output(items,stream)
			
	def _output(self,items,stream):
		doc = xml.dom.minidom.getDOMImplementation().createDocument(None,"svg",None)
		root = doc.documentElement
		root.setAttribute("xmlns","http://www.w3.org/2000/svg")
		root.setAttribute("version","1.1")
		for item in sorted(items,key=lambda i: i.z):
			hname = "_do_%s" % type(item).__name__
			getattr(self,hname,lambda i,d,p: None)(item,doc,root)
		doc.writexml(stream,addindent="\t",newl="\n")
			
	def _colour(self,colour):
		return colour if colour else "none"
	
	def _x(self,x):
		return str(int(x * SvgOutput.CHAR_W))
		
	def _y(self,y):
		return str(int(y * SvgOutput.CHAR_H))
		
	def _w(self,w):
		return str(float(w * SvgOutput.STROKE_W))
			
	def _style_attrs(self,item,el):
		if hasattr(item,"stroke"):
			el.setAttribute("stroke",self._colour(item.stroke))
		if hasattr(item,"w"):
			el.setAttribute("stroke-width",self._w(item.w))
		if hasattr(item,"fill"):
			el.setAttribute("fill",self._colour(item.fill))
			
	def _do_Line(self,line,doc,parent):
		el = doc.createElement("line")
		el.setAttribute("x1",self._x(line.a[0]))
		el.setAttribute("y1",self._y(line.a[1]))
		el.setAttribute("x2",self._x(line.b[0]))
		el.setAttribute("y2",self._y(line.b[1]))
		self._style_attrs(line,el)
		parent.appendChild(el)
	
	def _do_Rectangle(self,rect,doc,parent):
		el = doc.createElement("rect")
		el.setAttribute("x",self._x(rect.a[0]))
		el.setAttribute("y",self._y(rect.a[1]))
		el.setAttribute("width",self._x(rect.b[0]-rect.a[0]))
		el.setAttribute("height",self._y(rect.b[1]-rect.a[1]))
		self._style_attrs(rect,el)
		parent.appendChild(el)
		
	def _do_Ellipse(self,ellipse,doc,parent):
		w = ellipse.b[0]-ellipse.a[0]
		h = ellipse.b[1]-ellipse.a[1]
		el = doc.createElement("ellipse")
		el.setAttribute("cx",self._x(ellipse.a[0]+w/2))
		el.setAttribute("cy",self._y(ellipse.a[1]+h/2))
		el.setAttribute("rx",self._x(w/2))
		el.setAttribute("ry",self._y(h/2))
		self._style_attrs(ellipse,el)
		parent.appendChild(el)
		
	def _do_Arc(self,arc,doc,parent):
		rx = (arc.b[0]-arc.a[0])/2
		ry = (arc.b[1]-arc.a[1])/2
		cx,cy = arc.a[0]+rx, arc.a[1]+ry
		sx = cx+math.cos(arc.start)*rx
		sy = cy+math.sin(arc.start)*ry
		ex = cx+math.cos(arc.end)*rx
		ey = cy+math.sin(arc.end)*ry
		el = doc.createElement("path")
		el.setAttribute("d","M %s,%s A %s,%s 0 %d 1 %s,%s" % (
			self._x(sx),self._y(sy), self._x(rx),self._y(ry), 
			1, self._x(ex),self._y(ey)))
		self._style_attrs(arc,el)
		parent.appendChild(el)
		
	def _do_Text(self,text,doc,parent):
		el = doc.createElement("text")
		el.setAttribute("x",self._x(text.pos[0]))
		el.setAttribute("y",self._y(text.pos[1]+0.75))
		el.setAttribute("font-family","monospace")
		el.appendChild(doc.createTextNode(text.text))
		el.setAttribute("fill",self._colour(text.colour))
		el.setAttribute("font-size",str(int(text.size*SvgOutput.FONT_SIZE)))
		parent.appendChild(el)
		
	
SvgOutput.INST = SvgOutput()


class PatternRejected(Exception): pass
class PatternStateError(Exception): pass

class Pattern(object):
	
	_gen = None
	_is_finished = False
	
	def __init__(self):
		self._gen = self._matcher()
		self._gen.next()
		
	def _matcher(self):
		yield
		self._reject()
		
	def _reject(self):
		raise PatternRejected()
		
	def _occupied(self,curr):
		return curr.meta & M_OCCUPIED
		
	def _expect(self,curr,char,meta=M_OCCUPIED):
		if self._occupied(curr) or curr.char != char:
			self._reject()
		else:
			return meta		

	def _awaiting_char_below(self,curr,pos):
		return (( curr.row <= pos[1] or curr.col < pos[0] )
				and curr.char != END_OF_INPUT )
				
	def test(self,currentchar):
		try:
			return self._gen.send(currentchar)
		except StopIteration:
			self._is_finished = True
			raise
		
	def render(self):
		if not self._is_finished: 
			raise PatternStateError("Pattern not matched")
		return []
		

class LiteralPattern(Pattern):

	pos = None
	char = None
	
	def _matcher(self):
		curr = yield
		if not curr.meta & M_OCCUPIED and not curr.char.isspace():  
			yield M_OCCUPIED
		else:
			self._reject()
		self.pos = curr.col,curr.row
		self.char = curr.char
		return
		
	def render(self):
		Pattern.render(self)
		return [ Text(self.pos,0,self.char,"brown",1) ]
		

class DiamondPattern(Pattern):

	tl = None
	br = None
	
	def _matcher(self):
		curr = yield
		startj,starti = curr.row,curr.col
		lasti = curr.col
		rowcount = 0
		curr = yield self._expect(curr,"/")
		curr = yield self._expect(curr,"\\")
		while True:
			while curr.col!=lasti-1: curr = yield M_NONE
			if curr.char != "/": break
			rowcount += 1
			curr = yield self._expect(curr,"/")
			for n in range(rowcount*2): curr = yield M_NONE
			curr = yield self._expect(curr,"\\")
			lasti -= 1
		curr = yield M_NONE
		w = rowcount*2 + 2
		h = (rowcount+1) * 2
		while rowcount >= 0:
			curr = yield self._expect(curr,"\\")
			for n in range(rowcount*2): curr = yield M_NONE
			curr = yield self._expect(curr,"/")
			if rowcount > 0: 
				while curr.col!=lasti+1: curr = yield M_NONE
			lasti += 1
			rowcount -= 1			
		self.tl = (starti-(w/2-1),startj)
		self.br = (starti+(w/2),startj+(h-1))		
		return
		
	def render(self):
		Pattern.render(self)
		w = self.br[0]-self.tl[0]+1
		h = self.br[1]-self.tl[1]+1
		return [		
			Line( (self.tl[0]+w/2.0, self.tl[1]),
				(self.br[0]+1.0, self.tl[1]+h/2.0), 1, "orange", 1),
			Line( (self.tl[0]+w/2.0, self.tl[1]),
				(self.tl[0], self.tl[1]+h/2.0), 1, "orange", 1),
			Line( (self.tl[0]+w/2.0, self.br[1]+1.0),
				(self.br[0]+1.0, self.tl[1]+h/2.0), 1, "orange", 1),
			Line( (self.tl[0]+w/2.0, self.br[1]+1.0),
				(self.tl[0], self.tl[1]+h/2.0), 1, "orange", 1) ]
				
		
class DbCylinderPattern(Pattern):

	tl = None
	br = None
	
	def _matcher(self):
		w,h = 0,0
		curr = yield
		self.tl = (curr.col,curr.row)
		curr = yield self._expect(curr,".")
		curr = yield self._expect(curr,"-")
		while True:
			if curr.char == ".": break
			curr = yield self._expect(curr,"-")
		w = curr.col-self.tl[0]+1
		curr = yield self._expect(curr,".")
		while curr.col!=self.tl[0]: curr = yield M_NONE
		curr = yield self._expect(curr,"'")
		for n in range(w-2):
			curr = yield self._expect(curr,"-")
		curr = yield self._expect(curr,"'")
		while curr.col!=self.tl[0]: curr = yield M_NONE
		while True:	
			curr = yield self._expect(curr,"|")
			for n in range(w-2):
				curr = yield M_NONE
			curr = yield self._expect(curr,"|")
			while curr.col!=self.tl[0]:
				curr = yield M_NONE
			if curr.char == "'": break
		curr = yield self._expect(curr,"'")
		for n in range(w-2):
			curr = yield self._expect(curr,"-")
		self.br = (curr.col,curr.row)
		curr = yield self._expect(curr,"'")
		return
		
	def render(self):
		Pattern.render(self)
		return [
			Ellipse((self.tl[0]+0.5,self.tl[1]+0.5),
				(self.br[0]+0.5,self.tl[1]+1.0+0.5),
				1,"purple",1,None),
			Line((self.tl[0]+0.5,self.tl[1]+1.0),
				(self.tl[0]+0.5,self.br[1]), 1,"purple",1),
			Line((self.br[0]+0.5,self.tl[1]+1.0),
				(self.br[0]+0.5,self.br[1]), 1,"purple",1),
			Arc((self.tl[0]+0.5,self.br[1]-1.0+0.5),
				(self.br[0]+0.5,self.br[1]+0.5),
				1, 0.0, math.pi, "purple",1,None)	]
				

class BoxPattern(Pattern):
	
	tl = None
	br = None
	
	def _matcher(self):
		w,h = 0,0
		curr = yield
		self.tl = (curr.col,curr.row)
		curr = yield self._expect(curr,"+")
		curr = yield self._expect(curr,"-")
		while True:
			if curr.char == "+": break
			curr = yield self._expect(curr,"-")
		w = curr.col-self.tl[0]+1
		curr = yield self._expect(curr,"+")
		while curr.col!=self.tl[0]: curr = yield M_NONE
		while True:
			curr = yield self._expect(curr,"|")
			for n in range(w-2): curr = yield M_NONE
			curr = yield self._expect(curr,"|")
			while curr.col!=self.tl[0]: curr = yield M_NONE
			if curr.char == "+": break
		curr = yield self._expect(curr,"+")
		for n in range(w-2):
			curr = yield self._expect(curr,"-")
		self.br = (curr.col,curr.row)
		curr = yield self._expect(curr,"+")
		return
		
	def render(self):
		Pattern.render(self)
		return [Rectangle((self.tl[0]+0.5,self.tl[1]+0.5),
			(self.br[0]+0.5,self.br[1]+0.5),1,"red",1,None)]
			
			
class LineSqCornerPattern(Pattern):
	
	def _matcher(self):
		curr = yield
		if( curr.char == "+" and not curr.meta & M_OCCUPIED 
				and curr.meta & M_LINE_SQ_CORNER):
			yield M_OCCUPIED
		else:
			self._reject()
		return 


class UpDiagLinePattern(Pattern):
	
	END_NORMAL = object()
	END_CORNER = object()
	
	startpos = None
	starttype = None
	endpos = None
	endtype = None
	
	def _matcher(self):
		curr = yield
		self.startpos = (curr.col,curr.row)
		self.starttype = UpDiagLinePattern.END_NORMAL
		if curr.char == "+":
			if not self._occupied(curr) or curr.meta & M_LINE_SQ_CORNER:
				self.starttype = UpDiagLinePattern.END_CORNER
				curr = yield M_LINE_SQ_CORNER
				while self._awaiting_char_below(curr,(self.startpos[0]-1,self.startpos[1])):
					curr = yield M_NONE
				if curr.col != self.startpos[0]-1:
					self._reject()
			else:
				self._reject()
		pos = curr.col,curr.row
		curr = yield self._expect(curr,"/")
		while True:
			while self._awaiting_char_below(curr,(pos[0]-1,pos[1])):
				curr = yield M_NONE
			if curr.col != pos[0]-1 or curr.char != "/": break
			pos = curr.col,curr.row
			curr = yield self._expect(curr,"/")
		self.endtype = UpDiagLinePattern.END_NORMAL
		self.endpos = pos
		if curr.char == "+" and curr.col == pos[0]-1:
			if not self._occupied(curr) or curr.meta & M_LINE_SQ_CORNER:
				self.endtype = UpDiagLinePattern.END_CORNER
				self.endpos = (curr.col,curr.row)
				curr = yield M_LINE_SQ_CORNER
		return
		
	def render(self):
		Pattern.render(self)
		soffset = (0.5,0.5) if self.starttype==UpDiagLinePattern.END_CORNER else (1.0,0.0)
		eoffset = (0.5,0.5) if self.endtype==UpDiagLinePattern.END_CORNER else (0.0,1.0)
		return [ Line(
					(self.startpos[0]+soffset[0],self.startpos[1]+soffset[1]),
					(self.endpos[0]+eoffset[0],self.endpos[1]+eoffset[1]),
					1,"blue",1) ]
						
	
class DownDiagLinePattern(Pattern):
	
	END_NORMAL = object()
	END_CORNER = object()
	
	startpos = None
	starttype = None
	endpos = None
	endtype = None
		
	def _matcher(self):
		curr = yield
		self.startpos = (curr.col,curr.row)
		self.starttype = DownDiagLinePattern.END_NORMAL
		if curr.char == "+":
			if not self._occupied(curr) or curr.meta & M_LINE_SQ_CORNER:
				self.starttype = DownDiagLinePattern.END_CORNER
				curr = yield M_LINE_SQ_CORNER
				while self._awaiting_char_below(curr,(self.startpos[0]+1,self.startpos[1])):
					curr = yield M_NONE
				if curr.col != self.startpos[0]+1:
					self._reject()
			else:
				self._reject()
		pos = curr.col,curr.row
		curr = yield self._expect(curr,"\\")
		while True:
			while self._awaiting_char_below(curr,(pos[0]+1,pos[1])):
				curr = yield M_NONE
			if curr.col != pos[0]+1 or curr.char != "\\": break
			pos = curr.col,curr.row
			curr = yield self._expect(curr,"\\")
		self.endtype = DownDiagLinePattern.END_NORMAL
		self.endpos = pos
		if curr.char == "+" and curr.col == pos[0]+1:
			if not self._occupied(curr) or curr.meta & M_LINE_SQ_CORNER:
				self.endtype = DownDiagLinePattern.END_CORNER
				self.endpos = (curr.col,curr.row)
				curr = yield M_LINE_SQ_CORNER			
		return 
		
	def render(self):
		Pattern.render(self)
		soffset = 0.5 if self.starttype==DownDiagLinePattern.END_CORNER else 0
		eoffset = 0.5 if self.endtype==DownDiagLinePattern.END_CORNER else 1.0
		return [ Line(
					(self.startpos[0]+soffset,self.startpos[1]+soffset),
					(self.endpos[0]+eoffset,self.endpos[1]+eoffset),
					1,"blue",1) ]
	
	
class VertLinePattern(Pattern):
	
	END_NORMAL = object()
	END_CORNER = object()
	
	startpos = None
	starttype = None
	endpos = None
	endtype = None	
	
	def _matcher(self):
		curr = yield
		self.startpos = (curr.col,curr.row)
		self.starttype = VertLinePattern.END_NORMAL
		if curr.char == "+":
			if not self._occupied(curr) or curr.meta & M_LINE_SQ_CORNER:
				self.starttype = VertLinePattern.END_CORNER
				curr = yield M_LINE_SQ_CORNER
				while self._awaiting_char_below(curr,self.startpos):
					curr = yield M_NONE
				if curr.col != self.startpos[0]: 
					self._reject()
			else:
				self._reject()
		pos = curr.col,curr.row
		curr = yield self._expect(curr,"|")
		while True:
			while self._awaiting_char_below(curr,pos):
				curr = yield M_NONE
			if curr.col != self.startpos[0] or curr.char != "|": break
			pos = curr.col,curr.row
			curr = yield self._expect(curr,"|")
		self.endtype = VertLinePattern.END_NORMAL
		self.endpos = pos
		if curr.char == "+" and curr.col == self.startpos[0]:
			if not self._occupied(curr) or curr.meta & M_LINE_SQ_CORNER:
				self.endtype = VertLinePattern.END_CORNER
				self.endpos = (curr.col,curr.row)
				curr = yield M_LINE_SQ_CORNER			
		return 
		
	def render(self):
		Pattern.render(self)
		soffset = 0.5 if self.starttype==VertLinePattern.END_CORNER else 0
		eoffset = 0.5 if self.endtype==VertLinePattern.END_CORNER else 1.0
		return [ Line(
					(self.startpos[0]+0.5,self.startpos[1]+soffset),
					(self.endpos[0]+0.5,self.endpos[1]+eoffset),
					1,"blue",1) ]
	
	
class HorizLinePattern(Pattern):

	END_NORMAL = object()
	END_CORNER = object()

	startpos = None
	starttype = None
	endpos = None
	endtype = None

	def _matcher(self):
		curr = yield
		self.startpos = (curr.col,curr.row)
		self.starttype = HorizLinePattern.END_NORMAL
		if curr.char == "+":
			self.starttype = HorizLinePattern.END_CORNER
			if not self._occupied(curr):
				curr = yield M_LINE_SQ_CORNER
			elif curr.meta & M_LINE_SQ_CORNER:
				curr = yield M_NONE
			else:
				self._reject()
		curr = yield self._expect(curr,"-")
		while True:
			if curr.char != "-": break
			curr = yield self._expect(curr,"-")
		self.endtype = HorizLinePattern.END_NORMAL
		if curr.char == "+":
			self.endtype = HorizLinePattern.END_CORNER
			if not self._occupied(curr):
				curr = yield M_LINE_SQ_CORNER
			elif curr.meta & M_LINE_SQ_CORNER:
				curr = yield M_NONE
			else:
				self.endtype = HorizLinePattern.END_NORMAL
		self.endpos = (curr.col-1,curr.row)
		return
		
	def render(self):
		Pattern.render(self)
		soffset = 0.5 if self.starttype==HorizLinePattern.END_CORNER else 0
		eoffset = 0.5 if self.endtype==HorizLinePattern.END_CORNER else 1.0
		return [ Line(
					(self.startpos[0]+soffset,self.startpos[1]+0.5),
					(self.endpos[0]+eoffset,self.endpos[1]+0.5),
					1,"blue",1) ]
			

class TinyCirclePattern(Pattern):

	pos = None
	
	def _matcher(self):
		curr = yield
		if curr.char.isalpha(): self._reject()
		curr = yield M_NONE
		self.pos = curr.col,curr.row
		curr = yield self._expect(curr,"O")
		if curr.char.isalpha(): self._reject()
		return
		
	def render(self):
		Pattern.render(self)
		return [ Ellipse((self.pos[0]+0.5-0.4,self.pos[1]+0.5-0.4/CHAR_H_RATIO), 
				(self.pos[0]+0.5+0.4,self.pos[1]+0.5+0.4/CHAR_H_RATIO), 1, "magenta", 1, None) ]
				
				
class SmallCirclePattern(Pattern):
	
	left = None
	right = None
	y = None
	
	def _matcher(self):
		curr = yield
		self.left = curr.col
		self.y = curr.row
		curr = yield self._expect(curr,"(")
		for n in range(3):
			if curr.char == ")": break
			curr = yield M_NONE
		else:
			self._reject()
		self.right = curr.col
		curr = yield self._expect(curr,")")
		return
		
	def render(self):
		Pattern.render(self)
		d = self.right-self.left
		return [ Ellipse((self.left+0.5,self.y+0.5-d/2.0/CHAR_H_RATIO),
				(self.right+0.5,self.y+0.5+d/2.0/CHAR_H_RATIO), 1, "green",1,None) ]
	
		
PATTERNS = [
	DbCylinderPattern,
	DiamondPattern,
	BoxPattern,
	SmallCirclePattern,
	TinyCirclePattern,
	HorizLinePattern,
	VertLinePattern,
	UpDiagLinePattern,
	DownDiagLinePattern,
	LineSqCornerPattern,
	LiteralPattern
]


class MatchLookup(object):

	_matches = None
	_occupants = None
	_match_meta = None
	
	def __init__(self):
		self._matches = []
		self._occupants = defaultdict(list)
		self._match_meta = defaultdict(dict)

	def get_all_matches(self):
		return list(self._matches)
		
	def get_occupants_at(self,pos):
		return list(self._occupants[pos])
		
	def get_meta_for(self,match):
		return dict(self._match_meta[match])
		
	def add_match(self,match):
		self._matches.append(match)
		
	def add_meta(self,match,pos,meta):
		if meta & M_OCCUPIED:
			self._occupants[pos].append(match)
		self._match_meta[match][pos] = meta
		
	def remove_match(self,match):
		try: 
			self._matches.remove(match)
		except ValueError: pass
		for pos,meta in self._match_meta[match].items():
			if meta & M_OCCUPIED:
				try:
					self._occupants[pos].remove(match)
				except ValueError: pass
		del(self._match_meta[match])
		
	def remove_cooccupants(self,match):
		for pos,meta in self.get_meta_for(match).items():
			if meta & M_OCCUPIED:
				for m in self.get_occupants_at(pos):
					self.remove_match(m)
		
		
CurrentChar = namedtuple("CurrentChar","row col char meta")


if __name__ == "__main__":

	INPUT = """\
MiniOreos Oranges O O O test
+---+  +-<>  ---+ +-------+ .-----.  /`
| O |  |  +------+| +---+ | '-----' //``     + + +- 
+---+--+ O| ***  || |(*)| |-| --- | ``//    /|/| |
/`  |O |  +------+| +---+ | | --- |  `/+-+   +   +- 
    +--+   .--.   +-------+ '-----' /` | |  + +  |
() (A)  `  '--' /`This is a test|  /+ `+-+  |`|`
  (  )   ` |  | `/  --- ---+    | // ` `      +
   (   )  +'--'    +---+ --+--+-+ `   +/
          |        ||-`-`     | |  ` //
                   +-----+      |   `/""".replace("`","\\")
#	INPUT = """\
# + 1
# | 2      
# | 3    
# + 4  
# | 5     
# | 6     
# + 7"""
 
		
	complete_matches = []
	complete_meta = {}
	for pclass in PATTERNS:
		ongoing = MatchLookup()	
		for j,line in enumerate((INPUT+END_OF_INPUT).splitlines()):
			for i,char in enumerate(line):	
				meta = complete_meta.get((j,i),M_NONE)
				newp = pclass()
				ongoing.add_match(newp)
				for match in ongoing.get_all_matches():
					if not match in ongoing.get_all_matches():
						continue
					try:
						matchmeta = match.test(CurrentChar(j,i,char,meta))
					except PatternRejected:
						ongoing.remove_match(match)
					except StopIteration:
						complete_matches.append(match)
						for p,m in ongoing.get_meta_for(match).items():
							complete_meta[p] = complete_meta.get(p,M_NONE) | m
						ongoing.remove_cooccupants(match)
						ongoing.remove_match(match)
					else:
						ongoing.add_meta(match,(j,i),matchmeta)
		
	renderitems = []				
	for m in complete_matches:
		renderitems.extend(m.render())
	with open("test2.svg","w") as f:
		SvgOutput.output(renderitems,f)
	
	
	
	
