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
"""
"""	
TODO:
	* Release
	* Complete readme TODOs
	* Note/document (folded corner, cutoff)
	* Transparent background
	* Box shadows
	* Raster unit tests - find image library
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
	* Python 3
	* Stacked boxes
	* Terminal
	* Hexagon boxes
	* Sketch rendering (random distortion, cursive font)
	* Diagonal lines to boxes
	* Pgram box separators
	* Diamond box separators
	* Circle box separators	
	* Rounded corner box separators
	* Slash-corner box separators
	* Cloud box separators
	* 3d box separators
	* Disallow alphas beside down arrows
	* Open diagram format (which?)
	* Box/Cylinder shadows
	* Hexagon box separators
	* Dashed Paralellogram boxes
	* Diagonal arrowheads
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
	"brown":	(0.5,0.3,0.1),
}


class OutputPrefs(object):
	def __init__(self, 
			fgcolour=(0,0,0), 
			bgcolour=(1,1,1),
			charheight=24):
		for k,v in locals().items():		
			if k!="self": setattr(self,k,v)
			

class PngOutput(object):
	
	EXTS = ("png",)
	
	STROKE_W = 2.5 # currently fixed
	FONT_SIZE = 0.667 # of character heigt
	DASH_PATTERN = 8,8
	TEXT_BASELINE = 0.75
	
	diagram = None
	stream = None
	prefs = None
	ctx = None
	
	@staticmethod
	def output(diagram,stream,prefs):
		PngOutput(diagram,stream,prefs)._output()
		
	def __init__(self,diagram,stream,prefs):
		self.diagram = diagram
		self.stream = stream
		self.prefs = prefs
		
	def _output(self):
		surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
			self._x(self.diagram.size[0]),self._y(self.diagram.size[1]))
		self.ctx = cairo.Context(surface)
		self._do_Rectangle(core.Rectangle(a=(0,0),b=self.diagram.size,z=0,stroke=None,
			salpha=1,w=10,stype=core.STROKE_DASHED,fill=self.prefs.bgcolour,falpha=1))
		for item in sorted(self.diagram.content,key=lambda i: i.z):
			hname = "_do_%s" % type(item).__name__
			getattr(self,hname,lambda i: None)(item)
		surface.write_to_png(self.stream)

	def _do_Line(self,line):		
		if self._should_stroke(line):
			self.ctx.move_to(self._x(line.a[0]),self._y(line.a[1]))
			self.ctx.line_to(self._x(line.b[0]),self._y(line.b[1]))
			self._stroke(line)
		
	def _do_Rectangle(self,rect):
		r = (self._x(rect.a[0]),self._y(rect.a[1]),
			self._x(rect.b[0]-rect.a[0]),self._y(rect.b[1]-rect.a[1]))
		if self._should_fill(rect):
			self.ctx.rectangle(*r)
			self._fill(rect)
		if self._should_stroke(rect):
			self.ctx.rectangle(*r)
			self._stroke(rect)
		
	def _do_Ellipse(self,ellipse):
		w = self._x( ellipse.b[0] - ellipse.a[0] )
		h = self._y( ellipse.b[1] - ellipse.a[1] )
		x = self._x(ellipse.a[0]) + w/2.0
		y = self._y(ellipse.a[1]) + h/2.0
		if self._should_fill(ellipse):
			self._arc_path(w,h,x,y,0,2*math.pi)
			self._fill(ellipse)
		if self._should_stroke(ellipse):
			self._arc_path(w,h,x,y,0,2*math.pi)
			self._stroke(ellipse)
		
	def _arc_path(self,w,h,cx,cy,start,end):
		self.ctx.save()
		self.ctx.translate(cx,cy)
		self.ctx.scale(w/2.0,h/2.0)
		self.ctx.arc(0,0, 1.0, start,end)
		self.ctx.restore()
		
	def _do_Arc(self,arc):
		w = self._x( arc.b[0] - arc.a[0] )
		h = self._y( arc.b[1] - arc.a[1] )
		x = self._x(arc.a[0]) + w/2.0
		y = self._y(arc.a[1]) + h/2.0
		if self._should_fill(arc):
			self._arc_path(w,h,x,y,arc.start,arc.end)
			self._fill(arc)
		if self._should_stroke(arc):
			self._arc_path(w,h,x,y,arc.start,arc.end)
			self._stroke(arc)
		
	def _do_QuadCurve(self,quad):
		c1 = ( self._x(quad.a[0]) + ( self._x(quad.c[0]) - self._x(quad.a[0]) )*(2.0/3.0),
				self._y(quad.a[1]) + ( self._y(quad.c[1]) - self._y(quad.a[1]) )*(2.0/3.0) )
		c2 = ( self._x(quad.b[0]) + ( self._x(quad.c[0]) - self._x(quad.b[0]) )*(2.0/3.0),
				self._y(quad.b[1]) + ( self._y(quad.c[1]) - self._y(quad.b[1]) )*(2.0/3.0) )
		if self._should_stroke(quad):
			self.ctx.move_to(self._x(quad.a[0]),self._y(quad.a[1]))
			self.ctx.curve_to(c1[0],c1[1],c2[0],c2[1],self._x(quad.b[0]),self._y(quad.b[1]))
			self._stroke(quad)
		
	def _poly_path(self,points):
		self.ctx.move_to(self._x(points[0][0]),self._y(points[0][1]))
		for point in points[1:]:
			self.ctx.line_to(self._x(point[0]),self._y(point[1]))
		self.ctx.close_path()
		
	def _do_Polygon(self,poly):
		if self._should_fill(poly):
			self._poly_path(poly.points)
			self._fill(poly)
		if self._should_stroke(poly):
			self._poly_path(poly.points)
			self._stroke(poly)
		
	def _do_Text(self,text):
		self.ctx.select_font_face("monospace")
		self.ctx.set_font_size(self.prefs.charheight*PngOutput.FONT_SIZE)
		self.ctx.set_source_rgba(*self._colour(text.colour,text.alpha))
		self.ctx.move_to(self._x(text.pos[0]),self._y(text.pos[1]+PngOutput.TEXT_BASELINE))
		self.ctx.show_text(text.text)
		self.ctx.new_path()
		
	def _should_fill(self,item):
		return item.fill is not None and item.falpha > 0
		
	def _fill(self,item):
		if not self._should_fill(item): return
		self.ctx.set_source_rgba(*self._colour(item.fill,item.falpha))
		self.ctx.fill()

	def _should_stroke(self,item):
		return item.stroke is not None and item.salpha > 0
	
	def _stroke(self,item):
		if not self._should_stroke(item): return
		self.ctx.set_source_rgba(*self._colour(item.stroke,item.salpha))
		self.ctx.set_line_width(item.w*PngOutput.STROKE_W)
		self.ctx.set_dash(PngOutput.DASH_PATTERN if item.stype==core.STROKE_DASHED else [])
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

	EXTS = ("svg","xml")

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

def process_diagram(text,patternlist,proglsnr=lambda x: None):

	lines = []
	lines.append( [core.START_OF_INPUT] )
	lines.extend( [l+"\n" for l in text.splitlines()] )
	lines.append( [core.END_OF_INPUT] )
	height = len(lines)-2
	width = max([len(x) for x in lines])-1

	complete_matches = []
	complete_meta = {}
	for pnum,pclass in enumerate(patternlist):
		proglsnr(float(pnum)/len(patternlist))
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

	proglsnr(1.0)			
	content = sum([m.render() for m in complete_matches],[])

	return Diagram((width,height),content)
	

