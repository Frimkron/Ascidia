import xml.dom
import xml.dom.minidom
import math
from collections import defaultdict
from collections import namedtuple

P_IGNORED = "IGNORED"
P_ACCEPTED = "ACCEPTED"
P_FINISHED = "FINISHED"
P_ABORTED = "ABORTED"

CHAR_H_RATIO = 2.0

Line = namedtuple("Line","a b z stroke w")
Rectangle = namedtuple("Rectangle","a b z stroke w fill")
Ellipse = namedtuple("Ellipse", "a b z stroke w fill")
Arc = namedtuple("Arc","a b z start end stroke w fill")
Text = namedtuple("Text","pos z text colour size")

M_GENERAL = (1<<0)
M_LINE_SQ_CORNER = (1<<1)
M_BOX_TOP = (1<<2)
M_BOX_BOTTOM = (1<<3)
M_BOX_LEFT = (1<<4)
M_BOX_RIGHT = (1<<5)
M_LINE = (1<<6)
M_VERTICAL = (1<<7)
M_HORIZONTAL = (1<<8)
M_UP_DIAGONAL = (1<<9)
M_DOWN_DIAGONAL = (1<<10)


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


class Pattern(object):
	
	_gen = None
	
	def __init__(self):
		self._gen = self._matcher()
		self._gen.next()
		
	def _matcher(self):
		yield
		yield P_ABORTED
		
	def _expect(self,curr,char):
		if curr.char == char and not curr.occupied:
			return P_ACCEPTED
		else:
			return P_ABORTED
		
	def test(self,currentchar):
		try:
			return self._gen.send(currentchar)
		except StopIteration:
			return P_IGNORED
		
	def render(self):
		return []


class LiteralPattern(Pattern):

	pos = None
	char = None
	
	def _matcher(self):
		curr = yield
		if not curr.occupied and not curr.char.isspace():  
			yield P_ACCEPTED
		else:
			yield P_ABORTED
		self.pos = curr.col,curr.row
		self.char = curr.char
		yield P_FINISHED	
		
	def render(self):
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
			while curr.col!=lasti-1: curr = yield P_IGNORED
			if curr.char != "/": break
			rowcount += 1
			curr = yield self._expect(curr,"/")
			for n in range(rowcount*2): curr = yield P_IGNORED
			curr = yield self._expect(curr,"\\")
			lasti -= 1
		curr = yield P_IGNORED
		w = rowcount*2 + 2
		h = (rowcount+1) * 2
		while rowcount >= 0:
			curr = yield self._expect(curr,"\\")
			for n in range(rowcount*2): curr = yield P_IGNORED
			curr = yield self._expect(curr,"/")
			if rowcount > 0: 
				while curr.col!=lasti+1: curr = yield P_IGNORED
			lasti += 1
			rowcount -= 1			
		self.tl = (starti-(w/2-1),startj)
		self.br = (starti+(w/2),startj+(h-1))		
		yield P_FINISHED
		
	def render(self):
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
		while curr.col!=self.tl[0]:
			curr = yield P_IGNORED
		curr = yield self._expect(curr,"'")
		for n in range(w-2):
			curr = yield self._expect(curr,"-")
		curr = yield self._expect(curr,"'")
		while curr.col!=self.tl[0]:
			curr = yield P_IGNORED
		while True:	
			curr = yield self._expect(curr,"|")
			for n in range(w-2):
				curr = yield P_IGNORED
			curr = yield self._expect(curr,"|")
			while curr.col!=self.tl[0]:
				curr = yield P_IGNORED
			if curr.char == "'": break
		curr = yield self._expect(curr,"'")
		for n in range(w-2):
			curr = yield self._expect(curr,"-")
		self.br = (curr.col,curr.row)
		curr = yield self._expect(curr,"'")
		yield P_FINISHED
		
	def render(self):
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
		while curr.col!=self.tl[0]:
			curr = yield P_IGNORED
		while True:
			curr = yield self._expect(curr,"|")
			for n in range(w-2):
				curr = yield P_IGNORED
			curr = yield self._expect(curr,"|")
			while curr.col!=self.tl[0]:
				curr = yield P_IGNORED
			if curr.char == "+": break
		curr = yield self._expect(curr,"+")
		for n in range(w-2):
			curr = yield self._expect(curr,"-")
		self.br = (curr.col,curr.row)
		curr = yield self._expect(curr,"+")
		yield P_FINISHED
		
	def render(self):
		return [Rectangle((self.tl[0]+0.5,self.tl[1]+0.5),
			(self.br[0]+0.5,self.br[1]+0.5),1,"red",1,None)]
		
	
class HorizLinePattern(Pattern):

	start = None
	end = None

	def _matcher(self):
		curr = yield
		self.start = (curr.col,curr.row)
		curr = yield self._expect(curr,"-")
		while True:
			if curr.char != "-": break
			curr = yield self._expect(curr,"-")
		self.end = (curr.col-1,curr.row)
		yield P_FINISHED
		
	def render(self):
		return [Line((self.start[0],self.start[1]+0.5),
			(self.end[0]+1.0,self.end[1]+0.5),1,"blue",1)]
			

class TinyCirclePattern(Pattern):

	pos = None
	
	def _matcher(self):
		curr = yield
		if curr.char.isalpha(): yield P_ABORTED
		curr = yield P_IGNORED
		self.pos = curr.col,curr.row
		curr = yield self._expect(curr,"O")
		if curr.char.isalpha(): yield P_ABORTED
		yield P_FINISHED
		
	def render(self):
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
			curr = yield P_IGNORED
		else:
			yield P_ABORTED
		self.right = curr.col
		curr = yield self._expect(curr,")")
		yield P_FINISHED
		
	def render(self):
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
	LiteralPattern
]


class MatchLookup(object):

	_matches = None
	_match_by_pos = None
	_pos_by_match = None
	
	def __init__(self):
		self._matches = []
		self._match_by_pos = defaultdict(list)
		self._pos_by_match = defaultdict(list)

	def get_all_matches(self):
		return list(self._matches)
		
	def get_matches(self,pos):
		return list(self._match_by_pos[pos])
		
	def get_positions(self,match):
		return list(self._pos_by_match[match])
		
	def add_match(self,match):
		self._matches.append(match)
		
	def add_position(self,match,pos):
		self._match_by_pos[pos].append(match)
		self._pos_by_match[match].append(pos)
		
	def has_match_at(self,pos):
		return len(self.get_matches(pos))>0
		
	def remove_match(self,match):
		try: 
			self._matches.remove(match)
		except ValueError: pass
		for p in self._pos_by_match[match]:
			try:
				self._match_by_pos[p].remove(match)
			except ValueError: pass
		try:
			del(self._pos_by_match[match])
		except KeyError: pass
		
	def remove_matches_overlapping(self,match):
		for pos in self.get_positions(match):
			for m in self.get_matches(pos):
				self.remove_match(m)
		
		
CurrentChar = namedtuple("CurrentChar","row col char meta")


if __name__ == "__main__":

	INPUT = """\
MiniOreos Oranges O O O test
+---+  +-<>  ---+ +-------+ .-----.  /`
| O |  |  +------+| +---+ | '-----' //``
+---+--+ O| ***  || |(*)| | | --- | ``//
/`  |O |  +------+| +---+ | | --- |  `/+-+
    +--+   .--.   +-------+ '-----' /` | |
() (A)     '--' /`This is a test   /  `+-+
  (  )     |  | `/                /    `
   (   )   '--'                   `    /
                                   `  /
                                    `/""".replace("`","\\")
#	INPUT = """\
#   O+--+r
#    |  |
#    +--+"""
		
	complete = MatchLookup()
	for pclass in PATTERNS:
	
		#if pclass == TinyCirclePattern:
		#	import pdb
		#	pdb.set_trace()		
	
		# TODO: need to pass meta data back to algorithm to
		# store alongside match's costituent characters
	
		ongoing = MatchLookup()	
		for j,line in enumerate((INPUT+"\x00").splitlines()):
			for i,c in enumerate(line):				
				occupied = complete.has_match_at((j,i))
				newp = pclass()
				ongoing.add_match(newp)
				for p in ongoing.get_all_matches():
					if not p in ongoing.get_all_matches():
						continue
					r = p.test(CurrentChar(j,i,c,occupied))
					if r == P_ABORTED: 
						ongoing.remove_match(p)
					elif r == P_FINISHED:
						complete.add_match(p)
						for pos in ongoing.get_positions(p):
							complete.add_position(p,pos)
						ongoing.remove_matches_overlapping(p)
					elif r == P_ACCEPTED:
						ongoing.add_position(p,(j,i))
		
	renderitems = []				
	for m in complete.get_all_matches():
		renderitems.extend(m.render())
	with open("test2.svg","w") as f:
		SvgOutput.output(renderitems,f)
	
	
	
	
