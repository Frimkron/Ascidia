P_IGNORED = "IGNORED"
P_ACCEPTED = "ACCEPTED"
P_FINISHED = "FINISHED"
P_ABORTED = "ABORTED"

import xml.dom
import xml.dom.minidom
import math
from collections import defaultdict
from collections import namedtuple

Line = namedtuple("Line","a b z stroke w")
Rectangle = namedtuple("Rectangle","a b z stroke w fill")
Ellipse = namedtuple("Ellipse", "a b z stroke w fill")
Arc = namedtuple("Arc","a b z start end stroke w fill")


class SvgOutput(object):

	CHAR_W = 12.0
	CHAR_H = 24.0
	STROKE_W = 2.5

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
		
	
SvgOutput.INST = SvgOutput()


class Pattern(object):
	
	_gen = None
	
	def __init__(self):
		self._gen = self._matcher()
		self._gen.next()
		
	def _matcher(self):
		yield
		yield P_ABORTED
		
	def test(self,row,col,char):
		try:
			return self._gen.send((row,col,char))
		except StopIteration:
			return P_IGNORED
		
	def render(self):
		return []
		
		
class DbCylinderPattern(Pattern):

	tl = None
	br = None
	
	def _matcher(self):
		w,h = 0,0
		j,i,c = yield
		self.tl = (i,j)
		if c != ".": yield P_ABORTED
		j,i,c = yield P_ACCEPTED
		if c != "-": yield P_ABORTED
		j,i,c = yield P_ACCEPTED
		while True:
			if c == ".": break
			elif c != "-": yield P_ABORTED
			j,i,c = yield P_ACCEPTED
		w = i-self.tl[0]+1
		j,i,c = yield P_ACCEPTED
		while i!=self.tl[0]:
			j,i,c = yield P_IGNORED
		if c != "'": yield P_ABORTED
		j,i,c = yield P_ACCEPTED
		for n in range(w-2):
			if c != "-": yield P_ABORTED
			j,i,c = yield P_ACCEPTED
		if c != "'": yield P_ABORTED
		j,i,c = yield P_ACCEPTED
		while i!=self.tl[0]:
			j,i,c = yield P_IGNORED
		while True:					
			if c != "|": yield P_ABORTED
			j,i,c = yield P_ACCEPTED
			for n in range(w-2):
				j,i,c = yield P_IGNORED
			if c != "|": yield P_ABORTED
			j,i,c = yield P_ACCEPTED
			while i!=self.tl[0]:
				j,i,c = yield P_IGNORED
			if c == "'": break
		j,i,c = yield P_ACCEPTED
		for n in range(w-2):
			if c != "-": yield P_ABORTED
			j,i,c = yield P_ACCEPTED
		if c != "'": yield P_ABORTED
		self.br = (i,j)
		yield P_ACCEPTED
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
		j,i,c = yield
		self.tl = (i,j)
		if c != "+": yield P_ABORTED
		j,i,c = yield P_ACCEPTED
		if c != "-": yield P_ABORTED
		j,i,c = yield P_ACCEPTED
		while True:
			if c == "+": break
			elif c != "-": yield P_ABORTED
			j,i,c = yield P_ACCEPTED
		w = i-self.tl[0]+1
		j,i,c = yield P_ACCEPTED
		while i!=self.tl[0]:
			j,i,c = yield P_IGNORED
		while True:
			if c != "|": yield P_ABORTED
			j,i,c = yield P_ACCEPTED
			for n in range(w-2):
				j,i,c = yield P_IGNORED
			if c != "|": yield P_ABORTED
			j,i,c = yield P_ACCEPTED
			while i!=self.tl[0]:
				j,i,c = yield P_IGNORED
			if c == "+": break
		j,i,c = yield P_ACCEPTED
		for n in range(w-2):
			if c != "-": yield P_ABORTED
			j,i,c = yield P_ACCEPTED
		if c != "+": yield P_ABORTED
		self.br = (i,j)
		yield P_ACCEPTED
		yield P_FINISHED
		
	def render(self):
		return [Rectangle((self.tl[0]+0.5,self.tl[1]+0.5),
			(self.br[0]+0.5,self.br[1]+0.5),1,"red",1,None)]
		
	
class HorizLinePattern(Pattern):

	start = None
	end = None

	def _matcher(self):
		j,i,c = yield
		self.start = (i,j)
		if c != "-": yield P_ABORTED
		while True:
			j,i,c = yield P_ACCEPTED
			if c != "-": break
		self.end = (i-1,j)
		yield P_FINISHED
		
	def render(self):
		return [Line((self.start[0],self.start[1]+0.5),
			(self.end[0]+1.0,self.end[1]+0.5),1,"blue",1)]
		
		
PATTERNS = [DbCylinderPattern,BoxPattern,HorizLinePattern]


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
		


if __name__ == "__main__":

	INPUT = """\
+---+  +-<>  ---+ +-------+ .-----. 
|   |  |  +------+| +---+ | '-----' 
+---+--+  | ***  || |   | | | --- |
    |  |  +------+| +---+ | | --- |
    +--+   .--.   +-------+ '-----'
           '--'
           |  |
           '--'"""
		
	complete = MatchLookup()
	for pclass in PATTERNS:
		ongoing = MatchLookup()	
		for j,line in enumerate((INPUT+"\x00").splitlines()):
			#print "line %d: [%s]" % (j+1,line)
			for i,c in enumerate(line):
				#print "char [%s]" % c
				if complete.has_match_at((j,i)):
					#print "%d,%d is occupied" % (j,i)
					#for foo in complete.get_matches((j,i)):
					#	print "%d,%d occupied by %s" % (j,i,str(foo))
					#	for bar in complete.get_positions(foo):
					#		print "also occupies %d,%d" % bar
					continue
				newp = pclass()
				ongoing.add_match(newp)
				for p in ongoing.get_all_matches():
					if not p in ongoing.get_all_matches():
						continue
					r = p.test(j,i,c)
					#print "%s testing [%s]" % (type(p).__name__,c)
					if r == P_ABORTED: 
						ongoing.remove_match(p)
					elif r == P_FINISHED:
						#print "matched %s at line %d char %d: %s" % (
						#	str(p),(j+1),(i+1),str(ongoing.get_positions(p)))
						complete.add_match(p)
						for pos in ongoing.get_positions(p):
							#print "occupying %d,%d" % pos
							complete.add_position(p,pos)
						ongoing.remove_matches_overlapping(p)
					elif r == P_ACCEPTED:
						ongoing.add_position(p,(j,i))
		
	renderitems = []				
	for m in complete.get_all_matches():
		renderitems.extend(m.render())
	with open("test2.svg","w") as f:
		SvgOutput.output(renderitems,f)
	
	
	
	
