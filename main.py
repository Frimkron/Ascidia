#!/usr/bin/python2

import sys
import argparse
import xml.dom
import xml.dom.minidom
import math
from collections import defaultdict
from collections import namedtuple

import core
import patterns



class OutputPrefs(object):
	def __init__(self, 
			fgcolour="black", 
			bgcolour="white" ):
		for k,v in locals().items():		
			if k!="self": setattr(self,k,v)
			

class SvgOutput(object):

	CHAR_W = 12.0
	CHAR_H = CHAR_W * core.CHAR_H_RATIO
	STROKE_W = 2.5
	FONT_SIZE = 16.0
	DASH_PATTERN = 8,8

	@staticmethod
	def output(items,stream,prefs):
		SvgOutput.INST._output(items,stream,prefs)
			
	def _output(self,items,stream,prefs):
		doc = xml.dom.minidom.getDOMImplementation().createDocument(None,"svg",None)
		root = doc.documentElement
		root.setAttribute("xmlns","http://www.w3.org/2000/svg")
		root.setAttribute("version","1.1")
		for item in sorted(items,key=lambda i: i.z):
			hname = "_do_%s" % type(item).__name__
			getattr(self,hname,lambda i,d,p: None)(item,doc,root,prefs)
		doc.writexml(stream,addindent="\t",newl="\n")
			
	def _colour(self,colour,prefs):
		if colour is None:
			return "none"
		elif colour == core.C_FOREGROUND:
			return prefs.fgcolour
		elif colour == core.C_BACKGROUND:
			return prefs.bgcolour
		else:
			return colour
	
	def _x(self,x):
		return str(int(x * SvgOutput.CHAR_W))
		
	def _y(self,y):
		return str(int(y * SvgOutput.CHAR_H))
		
	def _w(self,w):
		return str(float(w * SvgOutput.STROKE_W))
			
	def _style_attrs(self,item,el,prefs):
		if hasattr(item,"stroke"):
			el.setAttribute("stroke",self._colour(item.stroke,prefs))
		if hasattr(item,"w"):
			el.setAttribute("stroke-width",self._w(item.w))
		if hasattr(item,"stype"):
			if item.stype == core.STROKE_DASHED:
				el.setAttribute("stroke-dasharray",",".join(
						map(str,SvgOutput.DASH_PATTERN)))
		if hasattr(item,"fill"):
			el.setAttribute("fill",self._colour(item.fill,prefs))
			
	def _do_Line(self,line,doc,parent,prefs):
		el = doc.createElement("line")
		el.setAttribute("x1",self._x(line.a[0]))
		el.setAttribute("y1",self._y(line.a[1]))
		el.setAttribute("x2",self._x(line.b[0]))
		el.setAttribute("y2",self._y(line.b[1]))
		self._style_attrs(line,el,prefs)
		parent.appendChild(el)
	
	def _do_Rectangle(self,rect,doc,parent,prefs):
		el = doc.createElement("rect")
		el.setAttribute("x",self._x(rect.a[0]))
		el.setAttribute("y",self._y(rect.a[1]))
		el.setAttribute("width",self._x(rect.b[0]-rect.a[0]))
		el.setAttribute("height",self._y(rect.b[1]-rect.a[1]))
		self._style_attrs(rect,el,prefs)
		parent.appendChild(el)
		
	def _do_Ellipse(self,ellipse,doc,parent,prefs):
		w = ellipse.b[0]-ellipse.a[0]
		h = ellipse.b[1]-ellipse.a[1]
		el = doc.createElement("ellipse")
		el.setAttribute("cx",self._x(ellipse.a[0]+w/2.0))
		el.setAttribute("cy",self._y(ellipse.a[1]+h/2.0))
		el.setAttribute("rx",self._x(w/2.0))
		el.setAttribute("ry",self._y(h/2.0))
		self._style_attrs(ellipse,el,prefs)
		parent.appendChild(el)
		
	def _do_Arc(self,arc,doc,parent,prefs):
		rx = (arc.b[0]-arc.a[0])/2.0
		ry = (arc.b[1]-arc.a[1])/2.0
		cx,cy = arc.a[0]+rx, arc.a[1]+ry
		sx = cx+math.cos(arc.start)*rx
		sy = cy+math.sin(arc.start)*ry
		ex = cx+math.cos(arc.end)*rx
		ey = cy+math.sin(arc.end)*ry
		el = doc.createElement("path")
		el.setAttribute("d","M %s,%s A %s,%s 0 %d 1 %s,%s" % (
			self._x(sx),self._y(sy), self._x(rx),self._y(ry), 
			1, self._x(ex),self._y(ey)))
		self._style_attrs(arc,el,prefs)
		parent.appendChild(el)
		
	def _do_QuadCurve(self,curve,doc,parent,prefs):
		el = doc.createElement("path")
		el.setAttribute("d","M %s,%s Q %s,%s %s,%s" % (
			self._x(curve.a[0]),self._y(curve.a[1]), self._x(curve.c[0]),self._y(curve.c[1]),
			self._x(curve.b[0]),self._y(curve.b[1]) ))
		self._style_attrs(curve,el,prefs)
		el.setAttribute("fill","none")
		parent.appendChild(el)
		
	def _do_Text(self,text,doc,parent,prefs):
		el = doc.createElement("text")
		el.setAttribute("x",self._x(text.pos[0]))
		el.setAttribute("y",self._y(text.pos[1]+0.75))
		el.setAttribute("font-family","monospace")
		el.appendChild(doc.createTextNode(text.text))
		el.setAttribute("fill",self._colour(text.colour,prefs))
		el.setAttribute("font-size",str(int(text.size*SvgOutput.FONT_SIZE)))
		parent.appendChild(el)
		
	
SvgOutput.INST = SvgOutput()



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


def process_diagram(text,patternlist):

	lines = [l+"\n" for l in text.splitlines()]
	lines.append( [core.END_OF_INPUT] )
	height = len(lines)-1
	width = max([len(x) for x in lines])-1

	complete_matches = []
	complete_meta = {}
	for pclass in patternlist:
		#print pclass.__name__
		ongoing = MatchLookup()	
		for j,line in enumerate(lines):
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
		
	result = sum([m.render() for m in complete_matches],[])
	result.append( core.Rectangle((0,0),(width,height),-1,None,1,core.STROKE_SOLID,core.C_BACKGROUND) )
	return result
	

if __name__ == "__main__":

	ap = argparse.ArgumentParser()
	ap.add_argument("-o","--outfile",default=None,help="output file")
	ap.add_argument("-f","--foreground",default="black",help="foreground colour")
	ap.add_argument("-b","--background",default="white",help="background colour")
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
		
	prefs = OutputPrefs(args.foreground,args.background)
	
	with outstream:
		SvgOutput.output(renderitems,outstream,prefs)
	
	

