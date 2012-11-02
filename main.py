#!/usr/bin/python2

"""	
TODO:
	* Image output (cairo?)
	* Rounded corner boxes
	* Slash-cornered boxes
	* Dashed round corner boxes
	* Note/document (folded corner, cutoff)
	* Cloud boxes
	* Tiny ellipse "o"
	* Tiny box "[]"
	* Small ellipse "( foo )"
	* Small boxes "[ foo ]"
	* Nested ellipses "(( foo ))"
	* Nested boxes "[[ foo ]]"	
	* Tiny diamond "<>"
	* Small diamonds "< foo >"
	* Nested diamonds "<< foo >>"
	* Circle arrow "|O<|--"
	* Circle connector "--O|"
	* Circle crows foot "|>O--"
	* One crows foot "|>|--"
	* Only one connector "-||--"
	* 3d boxes
	* Diagonal lines to boxes
	* Pgram box separators
	* Diamond box separators
	* Circle box separators	
	* Rounded corner box separators
	* Slash-corner box separators
	* Cloud box separators
	* 3d box separators
	* Disallow alphas beside down arrows
	* Stacked boxes
	* Open diagram format (which?)
	* Box/Cylinder shadows
	* Hexagon boxes
	* Hexagon box separators
	* Terminal
	* Dashed Paralellogram boxes
	* Diagonal arrowheads
	* Sketch rendering (random distortion, cursive font)
	* Diagonal jumps (X? r?)
	* Secondary colour (why?)
	* Image w and h options
	* Char ratio option
	
"""

import sys
import argparse
import xml.dom
import xml.dom.minidom
import math
import re
import cairo
from collections import defaultdict
from collections import namedtuple

import core
import patterns

NAMED_COLOURS = {
	"red": 		(0.75,0.1,0.1),
	"orange":	(0.9,0.3,0),	
	"yellow":	(0.9,0.9,0.2),
	"green":	(0.1,0.75,0.1),
	"blue":		(0.1,0.1,0.75),
	"purple":	(0.6,0.1,0.6),
	"pink":		(0.75,0.2,0.4),
	"black":	(0,0,0),
	"white":	(1,1,1),
	"gray":		(0.5,0.5,0.5),
	"brown":	(0.5,0.5,0.1),
}


class OutputPrefs(object):
	def __init__(self, 
			fgcolour=(0,0,0), 
			bgcolour=(1,1,1),
			charheight=24):
		for k,v in locals().items():		
			if k!="self": setattr(self,k,v)
			

class PngOutput(object):
	
	STROKE_W = 2.5 # currently fixed
	FONT_SIZE = 0.667 # of character heigt
	
	diagram = None
	stream = None
	prefs = None
	
	@staticmethod
	def output(items,stream,prefs):
		PngOutput(items,stream,prefs)._output()
		
	def __init__(self,items,stream,prefs):
		self.items = items
		self.stream = stream
		self.prefs = prefs
		
	def _output(self):
		surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,512,512)
		self.ctx = cairo.Context(surface)
		for item in sorted(self.items,key=lambda i: i.z):
			hname = "_do_%s" % type(item).__name__
			getattr(self,hname,lambda i: None)(item)
		surface.write_to_png(self.stream)

	def _do_Line(self,line):
		self.ctx.move_to(self._x(line.a[0]),self._y(line.a[1]))
		self.ctx.line_to(self._x(line.b[0]),self._y(line.b[1]))
		self.ctx.set_source_rgba(*self._colour(line.stroke,line.salpha))
		self.ctx.set_line_width(PngOutput.STROKE_W)
		self.ctx.stroke()
		
	def _colour(self,colour,alpha):
		if colour is None:
			return (0,0,0,0)
		elif colour == core.C_FOREGROUND:
			return tuple(list(self.prefs.fgcolour)+[alpha])
		elif colour == core.C_BACKGROUND:
			return tuple(list(self.prefs.bgcolour)+[alpha])
		else:
			return tuple(list(colour)+[alpha])
		
	def _x(self,x):
		return int(x * self.prefs.charheight / core.CHAR_H_RATIO)
		
	def _y(self,y):
		return int(y * self.prefs.charheight)

		
class SvgOutput(object):

	STROKE_W = 2.5 # currently fixed
	FONT_SIZE = 0.667 # of character height
	DASH_PATTERN = 8,8

	diagram = None
	stream = None
	prefs = None
	doc = None

	@staticmethod
	def output(diagram,stream,prefs):
		SvgOutput(diagram,stream,prefs)._output()
			
	def __init__(self,diagram,stream,prefs):
		self.diagram = diagram
		self.stream = stream
		self.prefs = prefs
			
	def _output(self):
		self.doc = xml.dom.minidom.getDOMImplementation().createDocument(None,"svg",None)
		root = self.doc.documentElement
		root.setAttribute("xmlns","http://www.w3.org/2000/svg")
		root.setAttribute("version","1.1")
		self._do_Rectangle(core.Rectangle(a=(0,0),b=self.diagram.size,z=0,stroke=None,salpha=1,
			w=0,stype=core.STROKE_SOLID,fill=self.prefs.bgcolour,falpha=1), root)
		for item in sorted(self.diagram.content,key=lambda i: i.z):
			hname = "_do_%s" % type(item).__name__
			getattr(self,hname,lambda i,p: None)(item,root)
		self.doc.writexml(self.stream,addindent="\t",newl="\n")
					
	def _do_Line(self,line,parent):
		el = self.doc.createElement("line")
		el.setAttribute("x1",self._x(line.a[0]))
		el.setAttribute("y1",self._y(line.a[1]))
		el.setAttribute("x2",self._x(line.b[0]))
		el.setAttribute("y2",self._y(line.b[1]))
		self._style_attrs(line,el)
		parent.appendChild(el)
	
	def _do_Rectangle(self,rect,parent):
		el = self.doc.createElement("rect")
		el.setAttribute("x",self._x(rect.a[0]))
		el.setAttribute("y",self._y(rect.a[1]))
		el.setAttribute("width",self._x(rect.b[0]-rect.a[0]))
		el.setAttribute("height",self._y(rect.b[1]-rect.a[1]))
		self._style_attrs(rect,el)
		parent.appendChild(el)
		
	def _do_Ellipse(self,ellipse,parent):
		w = ellipse.b[0]-ellipse.a[0]
		h = ellipse.b[1]-ellipse.a[1]
		el = self.doc.createElement("ellipse")
		el.setAttribute("cx",self._x(ellipse.a[0]+w/2.0))
		el.setAttribute("cy",self._y(ellipse.a[1]+h/2.0))
		el.setAttribute("rx",self._x(w/2.0))
		el.setAttribute("ry",self._y(h/2.0))
		self._style_attrs(ellipse,el)
		parent.appendChild(el)
		
	def _do_Arc(self,arc,parent):
		rx = (arc.b[0]-arc.a[0])/2.0
		ry = (arc.b[1]-arc.a[1])/2.0
		cx,cy = arc.a[0]+rx, arc.a[1]+ry
		sx = cx+math.cos(arc.start)*rx
		sy = cy+math.sin(arc.start)*ry
		ex = cx+math.cos(arc.end)*rx
		ey = cy+math.sin(arc.end)*ry
		el = self.doc.createElement("path")
		el.setAttribute("d","M %s,%s A %s,%s 0 %d 1 %s,%s" % (
			self._x(sx),self._y(sy), self._x(rx),self._y(ry), 
			1, self._x(ex),self._y(ey)))
		self._style_attrs(arc,el)
		parent.appendChild(el)
		
	def _do_QuadCurve(self,curve,parent):
		el = self.doc.createElement("path")
		el.setAttribute("d","M %s,%s Q %s,%s %s,%s" % (
			self._x(curve.a[0]),self._y(curve.a[1]), 
			self._x(curve.c[0]),self._y(curve.c[1]),
			self._x(curve.b[0]),self._y(curve.b[1]) ))
		self._style_attrs(curve,el)
		el.setAttribute("fill","none")
		parent.appendChild(el)
		
	def _do_Polygon(self,polygon,parent):
		el = self.doc.createElement("polygon")
		el.setAttribute("points",
			" ".join(["%s,%s" % (self._x(p[0]),self._y(p[1])) for p in polygon.points]))
		self._style_attrs(polygon,el)
		parent.appendChild(el)

	def _do_Text(self,text,parent):
		el = self.doc.createElement("text")
		el.setAttribute("x",self._x(text.pos[0]))
		el.setAttribute("y",self._y(text.pos[1]+0.75))
		el.setAttribute("font-family","monospace")
		el.appendChild(self.doc.createTextNode(text.text))
		el.setAttribute("fill",self._colour(text.colour))
		el.setAttribute("fill-opacity",self._alpha(text.alpha))
		el.setAttribute("font-size",str(int(text.size*self.prefs.charheight*SvgOutput.FONT_SIZE)))
		parent.appendChild(el)
		
	def _colour(self,colour):
		if colour is None: return "none"
		if colour == core.C_FOREGROUND: colour = self.prefs.fgcolour
		if colour == core.C_BACKGROUND: colour = self.prefs.bgcolour
		return "rgb(%d,%d,%d)" % tuple([int(c*255) for c in colour])
			
	def _x(self,x):
		return str(int(x * self.prefs.charheight / core.CHAR_H_RATIO))
		
	def _y(self,y):
		return str(int(y * self.prefs.charheight))
		
	def _w(self,w):
		return str(float(w * SvgOutput.STROKE_W))
			
	def _alpha(self,a):
		return str(a)
			
	def _style_attrs(self,item,el):
		if hasattr(item,"stroke"):
			el.setAttribute("stroke",self._colour(item.stroke))
		if hasattr(item,"w"):
			el.setAttribute("stroke-width",self._w(item.w))
		if hasattr(item,"stype"):
			if item.stype == core.STROKE_DASHED:
				el.setAttribute("stroke-dasharray",",".join(
						map(str,SvgOutput.DASH_PATTERN)))
		if hasattr(item,"salpha"):
			el.setAttribute("stroke-opacity",self._alpha(item.salpha))
		if hasattr(item,"fill"):
			el.setAttribute("fill",self._colour(item.fill))
		if hasattr(item,"falpha"):
			el.setAttribute("fill-opacity",self._alpha(item.falpha))
		
	
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
		if meta & core.M_OCCUPIED:
			self._occupants[pos].append(match)
		self._match_meta[match][pos] = meta
		
	def remove_match(self,match):
		try: 
			self._matches.remove(match)
		except ValueError: pass
		for pos,meta in self._match_meta[match].items():
			if meta & core.M_OCCUPIED:
				try:
					self._occupants[pos].remove(match)
				except ValueError: pass
		del(self._match_meta[match])
		
	def remove_cooccupants(self,match):
		for pos,meta in self.get_meta_for(match).items():
			if meta & core.M_OCCUPIED:
				for m in self.get_occupants_at(pos):
					self.remove_match(m)
		
		
CurrentChar = namedtuple("CurrentChar","row col char meta")

Diagram = namedtuple("Diagram","size content")

def process_diagram(text,patternlist):

	lines = []
	lines.append( [core.START_OF_INPUT] )
	lines.extend( [l+"\n" for l in text.splitlines()] )
	lines.append( [core.END_OF_INPUT] )
	height = len(lines)-2
	width = max([len(x) for x in lines])-1

	complete_matches = []
	complete_meta = {}
	for pclass in patternlist:
		print pclass.__name__
		ongoing = MatchLookup()	
		for j,line in enumerate(lines):
			j -= 1
			for i,char in enumerate(line):	
				meta = complete_meta.get((j,i),core.M_NONE)
				newp = pclass()
				ongoing.add_match(newp)
				for match in ongoing.get_all_matches():
					if not match in ongoing.get_all_matches():
						continue
					try:
						matchmeta = match.test(CurrentChar(j,i,char,meta))
					except core.PatternRejected:
						ongoing.remove_match(match)
					except StopIteration:
						complete_matches.append(match)
						for p,m in ongoing.get_meta_for(match).items():
							complete_meta[p] = complete_meta.get(p,core.M_NONE) | m
						ongoing.remove_cooccupants(match)
						ongoing.remove_match(match)
					else:
						ongoing.add_meta(match,(j,i),matchmeta)
		
	content = sum([m.render() for m in complete_matches],[])
	
	return Diagram((width,height),content)
	
	
def colour(s):
	if s.lower() in NAMED_COLOURS: return NAMED_COLOURS[s.lower()]
	bits = s.split(",")
	if len(bits) != 3: raise ValueError(s)
	for b in bits:
		if not( 0 <= float(b) <= 1):
			raise ValueError(s)
	return tuple(map(float,bits))
	

if __name__ == "__main__":

	ap = argparse.ArgumentParser()
	ap.add_argument("-o","--outfile",default=None,help="output file")
	ap.add_argument("-f","--foreground",default="black",type=colour,help="foreground colour")
	ap.add_argument("-b","--background",default="white",type=colour,help="background colour")
	ap.add_argument("-c","--charheight",default="24",type=int,help="character height in pixels")
	ap.add_argument("infile",default="-",nargs="?",help="input file")
	args = ap.parse_args()

	if args.infile == "-":
		instream = sys.stdin
	else:
		instream = open(args.infile,"r")

	with instream:
		input = instream.read()
	
	renderitems = process_diagram(input,patterns.PATTERNS)

	if args.outfile is None and args.infile == "-":
		outstream = sys.stdout
	elif args.outfile is None and args.infile != "-":
		name = args.infile
		extpos = name.rfind(".")
		if extpos != -1: name = name[:extpos]
		name += ".svg"
		outstream = open(name,"w")
	elif args.outfile == "-":
		outstream = sys.stdout
	else:
		outstream = open(args.outfile,"w")
		
	prefs = OutputPrefs(args.foreground,args.background,args.charheight)
	#prefs = OutputPrefs((0,0,0),(1,1,1),24)
	
	with outstream:
		SvgOutput.output(renderitems,outstream,prefs)
		#PngOutput.output(renderitems,outstream,prefs)
	
	

