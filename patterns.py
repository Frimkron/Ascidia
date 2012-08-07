""" 
Pattern classes go here
"""
import math
from core import *


class LiteralPattern(Pattern):

	pos = None
	char = None
	
	def matcher(self):
		self.curr = yield
		self.pos = self.curr.col,self.curr.row
		self.char = self.curr.char
		if( not self.occupied() and not self.curr.char.isspace()
				and self.curr.char != END_OF_INPUT ):
			yield M_OCCUPIED
		else:
			self.reject()
		return
		
	def render(self):
		Pattern.render(self)
		return [ Text(self.pos,0,self.char,"black",1) ]
		
		
class DbCylinderPattern(Pattern):

	tl = None
	br = None
	
	def matcher(self):
		w,h = 0,0
		self.curr = yield
		self.tl = (self.curr.col,self.curr.row)
		self.curr = yield self.expect(".")
		self.curr = yield self.expect("-")
		while self.curr.char != ".":
			self.curr = yield self.expect("-")
		w = self.curr.col-self.tl[0]+1
		self.curr = yield self.expect(".")
		for meta in self.await_pos(self.offset(-w,1)):
			self.curr = yield meta
		self.curr = yield self.expect("'")
		for n in range(w-2):
			self.curr = yield self.expect("-")
		self.curr = yield self.expect("'")
		for meta in self.await_pos(self.offset(-w,1)):
			self.curr = yield meta
		while True:	
			self.curr = yield self.expect("|")
			for meta in self.await_pos(self.offset(w-2,0)):
				self.curr = yield meta
			self.curr = yield self.expect("|")
			for meta in self.await_pos(self.offset(-w,1)):
				self.curr = yield meta
			if self.curr.char == "'": break
		self.curr = yield self.expect("'")
		for n in range(w-2):
			self.curr = yield self.expect("-")
		self.br = (self.curr.col,self.curr.row)
		self.curr = yield self.expect("'")
		return
		
	def render(self):
		Pattern.render(self)
		return [
			Ellipse((self.tl[0]+0.5,self.tl[1]+0.5),
				(self.br[0]+0.5,self.tl[1]+1.0+0.5),
				1,"purple",1,STROKE_SOLID,None),
			Line((self.tl[0]+0.5,self.tl[1]+1.0),
				(self.tl[0]+0.5,self.br[1]), 1,"purple",1,STROKE_SOLID),
			Line((self.br[0]+0.5,self.tl[1]+1.0),
				(self.br[0]+0.5,self.br[1]), 1,"purple",1,STROKE_SOLID),
			Arc((self.tl[0]+0.5,self.br[1]-1.0+0.5),
				(self.br[0]+0.5,self.br[1]+0.5),
				1, 0.0, math.pi, "purple",1,STROKE_SOLID,None)	]
				

class BoxPattern(Pattern):
	
	tl = None
	br = None
	
	def matcher(self):
		w,h = 0,0
		self.curr = yield
		self.tl = (self.curr.col,self.curr.row)
		rowstart = self.curr.col,self.curr.row
		self.curr = yield self.expect("+",meta=M_OCCUPIED|M_BOX_START_S|M_BOX_START_E)
		self.curr = yield self.expect("-",meta=M_OCCUPIED|M_BOX_START_S)
		while self.curr.char != "+":
			self.curr = yield self.expect("-",meta=M_OCCUPIED|M_BOX_START_S)
		w = self.curr.col-self.tl[0]+1
		self.curr = yield self.expect("+",meta=M_OCCUPIED|M_BOX_START_S)
		self.curr = yield M_BOX_AFTER_E
		for meta in self.await_pos(self.offset(0,1,rowstart)): 
			self.curr = yield meta
		while True:
			rowstart = self.curr.col,self.curr.row
			self.curr = yield self.expect("|",meta=M_OCCUPIED|M_BOX_START_E)
			for meta in self.await_pos(self.offset(w-2,0)):
				self.curr = yield meta
			self.curr = yield self.expect("|",meta=M_OCCUPIED)
			self.curr = yield M_BOX_AFTER_E
			for meta in self.await_pos(self.offset(0,1,rowstart)):
				self.curr = yield meta
			if self.curr.char == "+": break
		rowstart = self.curr.col,self.curr.row
		self.curr = yield self.expect("+",meta=M_OCCUPIED|M_BOX_START_E)
		for n in range(w-2):
			self.curr = yield self.expect("-",meta=M_OCCUPIED)
		self.br = (self.curr.col,self.curr.row)
		self.curr = yield self.expect("+",meta=M_OCCUPIED)
		self.curr = yield M_BOX_AFTER_E
		try:
			for meta in self.await_pos(self.offset(0,1,rowstart)):
				self.curr = yield meta
			rowstart = self.curr.col,self.curr.row
			for n in range(w):
				if self.curr.char=="\n": break
				self.curr = yield M_BOX_AFTER_S
		except NoSuchPosition: pass
		return
		
	def render(self):
		Pattern.render(self)
		return [Rectangle((self.tl[0]+0.5,self.tl[1]+0.5),
			(self.br[0]+0.5,self.br[1]+0.5),1,"red",1,STROKE_SOLID,None)]
			
			
class LineSqCornerPattern(Pattern):

	pos = None
	ends = None
	
	def matcher(self):
		self.curr = yield
		if self.occupied(): self.reject()
		self.pos = self.curr.col,self.curr.row
		self.ends = []
		for m,dm,x,y in [
				(M_LINE_AFTER_E, M_DASH_AFTER_E, -1,0),
				(M_LINE_AFTER_S, M_DASH_AFTER_S, 0,-1),
				(M_LINE_AFTER_SE,M_DASH_AFTER_SE,-1,-1),
				(M_LINE_AFTER_SW,M_DASH_AFTER_SW,1,-1) ]:
			if self.curr.meta & m: 
				self.ends.append((x,y,bool(self.curr.meta & dm)))			
		self.curr = yield self.expect("+")
		for m,dm,x,y in [
				(M_LINE_START_E, M_DASH_START_E, 1,0),
				(M_LINE_START_SW,M_DASH_START_SW,-1,1),
				(M_LINE_START_S, M_DASH_START_S, 0,1),
				(M_LINE_START_SE,M_DASH_START_SE,1,1) ]:
			try:
				for meta in self.await_pos(self.offset(x,y,self.pos)):
					self.curr = yield meta
				if self.curr.meta & m:
					self.ends.append((x,y,bool(self.curr.meta & dm)))	
			except NoSuchPosition: pass
		if len(self.ends) < 2: self.reject()			
		return 
		
	def render(self):
		Pattern.render(self)
		centre = self.pos[0]+0.5,self.pos[1]+0.5
		retval = []
		for x,y,dsh in self.ends:
			retval.append( Line(centre,(centre[0]+x*0.5,centre[1]+y*0.5),
					1,"pink",1,STROKE_DASHED if dsh else STROKE_SOLID) )
		return retval


class LineRdCornerPattern(Pattern):
	
	pos = None
	ends = None
	
	def matcher(self):
		self.curr = yield
		
		if self.occupied(): self.reject()
		
		self.pos = self.curr.col,self.curr.row
		
		up,down = False,False
		if self.curr.char == ".": 
			down = True
		elif self.curr.char == "'": 
			up = True
		elif self.curr.char == ":": 
			up,down = True,True
		else: self.reject()
		
		self.ends = []
		for m,dm,x,y in [ 
				(M_LINE_AFTER_E, M_DASH_AFTER_E, -1, 0),
				(M_LINE_AFTER_SW,M_DASH_AFTER_SW, 1,-1),
				(M_LINE_AFTER_S, M_DASH_AFTER_S,  0,-1),
				(M_LINE_AFTER_SE,M_DASH_AFTER_SE,-1,-1) ]:		
			if y < 0 and not up: continue
			if self.curr.meta & m: self.ends.append((x,y,self.curr.meta & dm))
			
		self.curr = yield M_OCCUPIED
		
		for m,dm,x,y in [
				(M_LINE_START_E, M_DASH_START_E,  1, 0),
				(M_LINE_START_SW,M_DASH_START_SW,-1, 1),
				(M_LINE_START_S, M_DASH_START_S,  0, 1),
				(M_LINE_START_SE,M_DASH_START_SE, 1, 1), ]:
			try:
				if y > 0 and not down: continue
				for meta in self.await_pos(self.offset(x,y,self.pos)):
					self.curr = yield meta
				if self.curr.meta & m: self.ends.append((x,y,self.curr.meta & dm))
			except NoSuchPosition: pass
		
		if len(self.ends) < 2: self.reject()
		return 
		
	def render(self):
		Pattern.render(self)
		centre = self.pos[0]+0.5,self.pos[1]+0.5
		retval = []
		rest = self.ends[:]
		while len(rest)>0:
			end = rest[0]
			rest = rest[1:]
			for oth in rest:
				a = centre[0]+end[0]*0.5, centre[1]+end[1]*0.5
				b = centre[0]+oth[0]*0.5, centre[1]+oth[1]*0.5
				retval.append( QuadCurve(a,b,centre,1,"pink",1,
					STROKE_DASHED if end[2] and oth[2] else STROKE_SOLID) )		
		return retval


class ArrowheadPattern(Pattern):

	pos = None
	tobox = False
	dashed = False
	chars = None
	linemeta = None
	boxmeta = None
	dashmeta = None
	flipped = False
	xdir = None
	ydir = None
	
	def matcher(self):
		self.curr = yield
		self.pos = self.curr.col,self.curr.row
		if self.occupied() or not self.curr.char in self.chars: self.reject()
		if self.flipped:
			if self.curr.meta & self.boxmeta: self.tobox = True
		else:
			if not self.curr.meta & self.linemeta: self.reject()
		self.curr = yield M_OCCUPIED
		try:
			for meta in self.await_pos(self.offset(self.xdir-1,self.ydir)):
				self.curr = yield meta
			if self.flipped:
				if not self.curr.meta & self.linemeta: self.reject()
			else:
				if self.curr.meta & self.boxmeta: self.tobox = True	
		except NoSuchPosition:
			if self.flipped: raise
		return
		
	def render(self):
		flip = -1 if self.flipped else 1
		centre = (self.pos[0]+0.5,self.pos[1]+0.5)
		spos = (centre[0]-0.5*self.xdir*flip,centre[1]-0.5*self.ydir*flip)
		apos2 = (centre[0]+(0.5+0.5*self.tobox)*self.xdir*flip,centre[1]+(0.5+0.5*self.tobox)*self.ydir*flip)
		apos1 = (apos2[0]-0.8*self.xdir*flip-0.5*self.ydir*flip,apos2[1]-0.8*self.ydir*flip/CHAR_H_RATIO-0.5*self.xdir*flip/CHAR_H_RATIO)
		apos3 = (apos2[0]-0.8*self.xdir*flip+0.5*self.ydir*flip,apos2[1]-0.8*self.ydir*flip/CHAR_H_RATIO+0.5*self.xdir*flip/CHAR_H_RATIO)
		return [
			Line(apos1,apos2,1,"darkred",1,STROKE_SOLID),
			Line(apos3,apos2,1,"darkred",1,STROKE_SOLID),
			Line(spos,apos2,1,"darkred",1,STROKE_DASHED if self.dashed else STROKE_SOLID) ]
		

class LArrowheadPattern(ArrowheadPattern):

	chars = "<"
	linemeta = M_LINE_START_E
	boxmeta = M_BOX_AFTER_E
	dashmeta = M_DASH_START_E
	xdir = 1
	ydir = 0
	flipped = True
	
		
class RArrowheadPattern(ArrowheadPattern):
	
	chars = ">"
	linemeta = M_LINE_AFTER_E
	boxmeta = M_BOX_START_E
	dashmeta = M_DASH_AFTER_E
	xdir = 1
	ydir = 0
	flipped = False
	

class DArrowheadPattern(ArrowheadPattern):

	chars = "Vv"
	linemeta = M_LINE_AFTER_S
	boxmeta = M_BOX_START_S
	dashmeta = M_DASH_AFTER_S
	xdir = 0
	ydir = 1
	flipped = False
	# TODO: disallow word context


class UArrowheadPattern(ArrowheadPattern):
	
	chars = "^"
	linemeta = M_LINE_START_S
	boxmeta = M_BOX_AFTER_S
	dashmeta = M_DASH_START_S
	xdir = 0
	ydir = 1
	flipped = True

	
class CrowsFeetPattern(Pattern):

	pos = None
	xdir = 0
	ydir = 0
	chars = None
	startmeta = None
	endmeta = None
	flipped = True
	dashed = False

	def matcher(self):
		self.curr = yield
		self.pos = self.curr.col,self.curr.row
		if( self.occupied() or not self.curr.char in self.chars
				or not self.curr.meta & self.startmeta ): 
			self.reject()
		if not self.flipped and self.curr.meta & self.dashmeta: 
			self.dashed = True
		self.curr = yield M_OCCUPIED
		for meta in self.await_pos(self.offset(self.xdir-1,self.ydir)):
			self.curr = yield meta
		if not self.curr.meta & self.endmeta: self.reject()
		if self.flipped and self.curr.meta & self.dashmeta:
			self.dashed = True
		return
		
	def render(self):
		
		flip = -1 if self.flipped else 1
		centre = ( self.pos[0]+0.5, self.pos[1]+0.5 )
		spos = ( centre[0]-self.xdir*0.5*flip, centre[1]-self.ydir*0.5*flip )
		fpos1 = ( centre[0]+self.xdir*1.0*flip - 0.6*(not self.xdir),
					centre[1]+self.ydir*1.0*flip - 0.6*(not self.ydir)/CHAR_H_RATIO )
		fpos2 = ( centre[0]+self.xdir*1.0*flip, centre[1]+self.ydir*1.0*flip )
		fpos3 = ( centre[0]+self.xdir*1.0*flip + 0.6*(not self.xdir), 
					centre[1]+self.ydir*1.0*flip + 0.6*(not self.ydir)/CHAR_H_RATIO )
		fpos0 = ( fpos2[0]-self.xdir*1.0*flip, fpos2[1]-self.ydir*1.0*flip/CHAR_H_RATIO )
		return [ 
			Line(fpos0,fpos1,1,"gray",1,STROKE_SOLID),
			Line(fpos0,fpos2,1,"gray",1,STROKE_SOLID),
			Line(fpos0,fpos3,1,"gray",1,STROKE_SOLID),
			Line(spos,fpos0,1,"gray",1,STROKE_DASHED if self.dashed else STROKE_SOLID) ]

	
class LCrowsFeetPattern(CrowsFeetPattern):

	xdir = 1
	ydir = 0
	chars = ">"
	flipped = True
	startmeta = M_BOX_AFTER_E
	endmeta = M_LINE_START_E
	dashmeta = M_DASH_START_E


class RCrowsFeetPattern(CrowsFeetPattern):
	
	xdir = 1
	ydir = 0
	chars = "<"
	flipped = False
	startmeta = M_LINE_AFTER_E
	endmeta = M_BOX_START_E
	dashmeta = M_DASH_AFTER_E
	
	
class UCrowsFeetPattern(CrowsFeetPattern):

	xdir = 0
	ydir = 1
	chars = "Vv"
	flipped = True
	startmeta = M_BOX_AFTER_S
	endmeta = M_LINE_START_S
	dashmeta = M_DASH_START_S
	
	
class DCrowsFeetPattern(CrowsFeetPattern):

	xdir = 0
	ydir = 1
	chars = "^"
	flipped = False
	startmeta = M_LINE_AFTER_S
	endmeta = M_BOX_START_S
	dashmeta = M_DASH_AFTER_S


class LinePattern(Pattern):

	xdir = 0	
	ydir = 0
	startchars = None
	midchars = None
	startpos = None
	endpos = None
	startmeta = None
	endmeta = None
	stroketype = None
	
	def matcher(self):
		self.curr = yield
		pos = self.curr.col,self.curr.row
		self.startpos = pos
		for i,startchar in enumerate(self.startchars):
			pos = self.curr.col,self.curr.row
			self.curr = yield self.expect(startchar,
				meta=M_OCCUPIED|(self.startmeta if i==0 else 0))
		try:
			breaknow = False
			while not breaknow:
				for i,midchar in enumerate(self.midchars):
					for meta in self.await_pos(self.offset(self.xdir-1,self.ydir)):
						self.curr = yield meta
					if( self.curr.char != midchar or self.occupied() 
							or self.curr.char == END_OF_INPUT ): 
						if i==0: 
							breaknow = True
							break
						else:
							self.reject()
					pos = self.curr.col,self.curr.row
					self.curr = yield self.expect(midchar,meta=M_OCCUPIED)
			self.endpos = pos
			yield self.endmeta
		except NoSuchPosition:
			self.endpos = pos
		return
		
	def render(self):
		Pattern.render(self)
		return [ Line((self.startpos[0]+0.5+self.xdir*-0.5,self.startpos[1]+0.5+self.ydir*-0.5),
				(self.endpos[0]+0.5+self.xdir*0.5,self.endpos[1]+0.5+self.ydir*0.5),1,"blue",1,self.stroketype) ]
		


class UpDiagLinePattern(LinePattern):
	
	xdir = -1
	ydir = 1
	startchars = ["/"]
	midchars = startchars
	startmeta = M_LINE_START_SW
	endmeta = M_LINE_AFTER_SW
	stroketype = STROKE_SOLID


class UpDiagDashedLinePattern(LinePattern):
	
	xdir = -1
	ydir = 1
	startchars = [","]
	midchars = startchars
	startmeta = M_LINE_START_SW | M_DASH_START_SW
	endmeta = M_LINE_AFTER_SW | M_DASH_AFTER_SW
	stroketype = STROKE_DASHED
	
		
class DownDiagLinePattern(LinePattern):

	xdir = 1
	ydir = 1
	startchars = ["\\"]
	midchars = startchars
	startmeta = M_LINE_START_SE
	endmeta = M_LINE_AFTER_SE
	stroketype = STROKE_SOLID
	
		
class DownDiagDashedLinePattern(LinePattern):
	
	xdir = 1
	ydir = 1
	startchars = ["`"]
	midchars = startchars
	startmeta = M_LINE_START_SE | M_DASH_START_SE
	endmeta = M_LINE_AFTER_SE | M_DASH_AFTER_SE
	stroketype = STROKE_DASHED
	
		
class VertLinePattern(LinePattern):

	xdir = 0
	ydir = 1
	startchars = ["|"]
	midchars = startchars
	startmeta = M_LINE_START_S
	endmeta = M_LINE_AFTER_S
	stroketype = STROKE_SOLID
	
	
class VertDashedLinePattern(LinePattern):

	xdir = 0
	ydir = 1
	startchars = [";"]
	midchars = startchars
	startmeta = M_LINE_START_S | M_DASH_START_S
	endmeta = M_LINE_AFTER_S | M_DASH_AFTER_S
	stroketype = STROKE_DASHED
	
	
class HorizLinePattern(LinePattern):

	xdir = 1
	ydir = 0
	startchars = ["-"]
	midchars = startchars
	startmeta = M_LINE_START_E
	endmeta = M_LINE_AFTER_E
	stroketype = STROKE_SOLID


class HorizDashedLinePattern(LinePattern):
	
	xdir = 1
	ydir = 0
	startchars = ["-"," ","-"," "]
	midchars = ["-"," "]
	startmeta = M_LINE_START_E | M_DASH_START_E
	endmeta = M_LINE_AFTER_E | M_DASH_AFTER_E
	stroketype = STROKE_DASHED


class TinyCirclePattern(Pattern):

	pos = None
	
	def matcher(self):
		self.curr = yield
		if self.curr.char.isalpha(): self.reject()
		self.curr = yield M_NONE
		self.pos = self.curr.col,self.curr.row
		self.curr = yield self.expect("O")
		if self.curr.char.isalpha(): self.reject()
		return
		
	def render(self):
		Pattern.render(self)
		return [ Ellipse((self.pos[0]+0.5-0.4,self.pos[1]+0.5-0.4/CHAR_H_RATIO), 
				(self.pos[0]+0.5+0.4,self.pos[1]+0.5+0.4/CHAR_H_RATIO), 1, 
				"magenta", 1, STROKE_SOLID, None) ]
				
				
class SmallCirclePattern(Pattern):
	
	left = None
	right = None
	y = None
	
	def matcher(self):
		self.curr = yield
		self.left = self.curr.col
		self.y = self.curr.row
		self.curr = yield self.expect("(")
		for n in range(3):
			if self.curr.char == ")": break
			self.curr = yield M_NONE
		else:
			self.reject()
		self.right = self.curr.col
		self.curr = yield self.expect(")")
		return
		
	def render(self):
		Pattern.render(self)
		d = self.right-self.left
		return [ Ellipse((self.left+0.5,self.y+0.5-d/2.0/CHAR_H_RATIO),
				(self.right+0.5,self.y+0.5+d/2.0/CHAR_H_RATIO), 1, "green",
				1,STROKE_SOLID,None) ]


class JumpPattern(Pattern):

	pos = None
	hdash = False
	vdash = False
	char = None

	def matcher(self):
		self.curr = yield
		ndash,edash,sdash,wdash = [False]*4
		if( self.curr.char != self.char or self.occupied() 
				or not self.curr.meta & M_LINE_AFTER_E 
				or not self.curr.meta & M_LINE_AFTER_S ):
			self.reject()
		if self.curr.meta & M_DASH_AFTER_E: wdash = True
		if self.curr.meta & M_DASH_AFTER_S: ndash = True
		self.pos = self.curr.col,self.curr.row
		self.curr = yield M_OCCUPIED
		for meta in self.await_pos(self.offset(1,0,self.pos)):
			self.curr = yield meta
		if not self.curr.meta & M_LINE_START_E: self.reject()
		if self.curr.meta & M_DASH_START_E: edash = True
		for meta in self.await_pos(self.offset(0,1,self.pos)):
			self.curr = yield meta
		if not self.curr.meta & M_LINE_START_S: self.reject()
		if self.curr.meta & M_DASH_START_S: sdash = True
		self.hdash = edash and wdash
		self.vdash = ndash and sdash 
		return
		
		
class LJumpPattern(JumpPattern):

	char = "("
		
	def render(self):
		return [ 
			Line((self.pos[0],self.pos[1]+0.5),(self.pos[0]+1.0,self.pos[1]+0.5),
				1,"cyan",1,STROKE_DASHED if self.hdash else STROKE_SOLID),
			Arc((self.pos[0]+0.5-0.6,self.pos[1]),(self.pos[0]+0.5+0.6,self.pos[1]+1.0),
				1,math.pi*0.5,math.pi*1.5,"cyan",1,STROKE_DASHED if self.vdash else STROKE_SOLID, None), ]
	
	
class RJumpPattern(JumpPattern):

	char = ")"
	
	def render(self):
		return [
			Line((self.pos[0],self.pos[1]+0.5),(self.pos[0]+1.0,self.pos[1]+0.5),
				1,"cyan",1,STROKE_DASHED if self.hdash else STROKE_SOLID),
			Arc((self.pos[0]+0.5-0.6,self.pos[1]),(self.pos[0]+0.5+0.6,self.pos[1]+1.0),
				1,math.pi*-0.5,math.pi*0.5,"cyan",1,STROKE_DASHED if self.vdash else STROKE_SOLID,None), ]
	
	
class UJumpPattern(JumpPattern):

	char = "^"
	
	def render(self):
		return [
			Line((self.pos[0]+0.5,self.pos[1]),(self.pos[0]+0.5,self.pos[1]+1.0),
				1,"cyan",1,STROKE_DASHED if self.vdash else STROKE_SOLID),
			Arc((self.pos[0],self.pos[1]+0.5-0.4),(self.pos[0]+1.0,self.pos[1]+0.5+0.4),
				1,math.pi,math.pi*2,"cyan",1,STROKE_DASHED if self.hdash else STROKE_SOLID,None), ]


class StickManPattern(Pattern):

	pos = None
	
	def matcher(self):
		self.curr = yield
		self.pos = self.curr.col,self.curr.row
		self.curr = yield self.expect("oO0")
		for meta in self.await_pos(self.offset(-2,1)):
			self.curr = yield meta
		self.curr = yield self.expect("-")
		self.curr = yield self.expect("|")
		self.curr = yield self.expect("-")
		for meta in self.await_pos(self.offset(-3,1)):
			self.curr = yield meta
		self.curr = yield self.expect("/")
		self.curr = yield self.expect(" ")
		self.curr = yield self.expect("\\")
		return
		
	def render(self):
		return [
			Ellipse(self.offset(0,1-1.0/CHAR_H_RATIO,self.pos),self.offset(1,1,self.pos),1,"yellow",1,STROKE_SOLID,None),
			Line(self.offset(0.5,1,self.pos),self.offset(0.5,1.8,self.pos),1,"yellow",1,STROKE_SOLID),
			Line(self.offset(-1,1.25,self.pos),self.offset(2,1.25,self.pos),1,"yellow",1,STROKE_SOLID),
			Line(self.offset(0.5,1.8,self.pos),self.offset(-0.5,2.8,self.pos),1,"yellow",1,STROKE_SOLID),
			Line(self.offset(0.5,1.8,self.pos),self.offset(1.5,2.8,self.pos),1,"yellow",1,STROKE_SOLID), ]

		
PATTERNS = [
	StickManPattern,
	DbCylinderPattern,
	BoxPattern,
	SmallCirclePattern,
	TinyCirclePattern,
	HorizDashedLinePattern,
	HorizLinePattern,
	VertLinePattern,
	VertDashedLinePattern,
	UpDiagLinePattern,
	UpDiagDashedLinePattern,
	DownDiagLinePattern,
	DownDiagDashedLinePattern,
	LineSqCornerPattern,
	LineRdCornerPattern,
	LJumpPattern,
	RJumpPattern,
	UJumpPattern,
	LArrowheadPattern,
	RArrowheadPattern,
	DArrowheadPattern,
	UArrowheadPattern,
	LCrowsFeetPattern,
	RCrowsFeetPattern,
	UCrowsFeetPattern,
	DCrowsFeetPattern,
	LiteralPattern
]

