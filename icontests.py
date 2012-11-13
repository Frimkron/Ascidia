#!/usr/bin/python2
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

import unittest
import core
import main
import patterns

from ptests import *


class TestLiteralPattern(unittest.TestCase,PatternTests):

	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.LiteralPattern
		
	def test_accepts_non_whitespace(self):
		p = self.pclass()
		p.test(main.CurrentChar(3,2,"a",core.M_NONE))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,3," ",core.M_NONE))
		
	def test_accepts_only_single_non_whitespace(self):
		p = self.pclass()
		p.test(main.CurrentChar(3,2,"a",core.M_NONE))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,3,"a",core.M_NONE))
			
	def test_rejects_if_whitespace(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2," ",core.M_NONE))
	
	def test_rejects_if_occupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"a",core.M_OCCUPIED))
			
	def test_accepts_other_meta(self):
		p = self.pclass()
		p.test(main.CurrentChar(2,3,"a",core.M_BOX_START_E))

	def test_rejects_if_start_of_input(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(-1,0,core.START_OF_INPUT,core.M_NONE))
		
	def test_rejects_if_end_of_input(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,core.END_OF_INPUT,core.M_NONE))
		
	def do_render(self,row,col,char):
		p = self.pclass()
		p.test(main.CurrentChar(row,col,char,core.M_NONE))
		try:
			p.test(main.CurrentChar(row,col+1,"b",core.M_NONE))
		except StopIteration: pass
		return p.render()
			
	def test_render_returns_text(self):
		result = self.do_render(0,0,"a")
		self.assertEquals(1,len(result))
		self.assertTrue(isinstance(result[0],core.Text))
		
	def test_render_coordinates(self):
		text = self.do_render(3,2,"a")[0]
		self.assertEquals((2,3), text.pos)
	
	def test_render_z(self):
		text = self.do_render(3,2,"a")[0]
		self.assertEquals(0, text.z)
		
	def test_render_text(self):
		text = self.do_render(2,1,"H")[0]
		self.assertEquals("H", text.text)
		
	def test_render_colour(self):
		text = self.do_render(2,1,"a")[0]
		self.assertEquals(core.C_FOREGROUND, text.colour)
		
	def test_render_size(self):
		text = self.do_render(2,1,"a")[0]
		self.assertEquals(1, text.size)


class TestStickManPattern(unittest.TestCase,PatternTests):

	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.StickManPattern
	
	def test_accepts_stick_man(self):
		p = self.pclass()
		feed_input(p,0,1, "O  \n")
		feed_input(p,1,0,"-|- \n")
		feed_input(p,2,0,"/ \\")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,3," ",core.M_NONE))
			
	def test_expects_head(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,1," ",core.M_NONE))
			
	def test_expects_head_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,1,"O",core.M_OCCUPIED))
	
	def test_allows_zero_as_head(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,1,"0",core.M_NONE))
		
	def test_allows_lowercase_oh_as_head(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,1,"o",core.M_NONE))
		
	def test_allows_rest_of_head_line(self):
		p = self.pclass()
		feed_input(p,0,1,"O")
		p.test(main.CurrentChar(0,2,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,3,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,4,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_arms_line(self):
		p = self.pclass()
		feed_input(p,0,3,"Oab\n")
		p.test(main.CurrentChar(1,0,"c",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"d",core.M_OCCUPIED))
		
	def test_expects_left_arm_hyphen(self):
		p = self.pclass()
		feed_input(p,0,2,  "O\n")
		feed_input(p,1,0,"z")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,1,"?",core.M_NONE))
			
	def test_expects_left_arm_hyphen_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "Oz\n")
		feed_input(p,1,0,"z")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,1,"-",core.M_OCCUPIED))
			
	def test_expects_body_pipe(self):
		p = self.pclass()
		feed_input(p,0,2,  "O\n")
		feed_input(p,1,0,"z-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"X",core.M_NONE))
			
	def test_expects_body_pipe_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "O\n")
		feed_input(p,1,0,"z-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"|",core.M_OCCUPIED))
			
	def test_expects_right_arm_hyphen(self):
		p = self.pclass()
		feed_input(p,0,2,  "O\n")
		feed_input(p,1,0,"z-|")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,3,"7",core.M_NONE))
			
	def test_expects_right_arm_hyphen_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "O\n")
		feed_input(p,1,0,"z-|")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,3,"-",core.M_OCCUPIED))
	
	def test_allows_rest_of_arm_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "O\n")
		feed_input(p,1,0,"z-|-")
		p.test(main.CurrentChar(1,4,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,5,"q",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,6,"\n",core.M_OCCUPIED))
	
	def test_allows_start_of_leg_line(self):
		p = self.pclass()
		feed_input(p,0,3,   "O\n")
		feed_input(p,1,0,"  -|-\n")
		p.test(main.CurrentChar(2,0,"y",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,1,"&",core.M_OCCUPIED))
	
	def test_expects_left_leg_forwardslash(self):
		p = self.pclass()
		feed_input(p,0,3,   "O\n")
		feed_input(p,1,0,"  -|-\n")
		feed_input(p,2,0,"ab")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"g",core.M_NONE))
			
	def test_expects_left_leg_forwardslash_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,3,   "O\n")
		feed_input(p,1,0,"  -|-\n")
		feed_input(p,2,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"/",core.M_OCCUPIED))
	
	def test_expects_space_between_legs(self):
		p = self.pclass()
		feed_input(p,0,3,   "O\n")
		feed_input(p,1,0,"  -|-\n")
		feed_input(p,2,0,"  /")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,3,"'",core.M_NONE))
			
	def test_expects_space_between_legs_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,3,   "O\n")
		feed_input(p,1,0,"  -|-\n")
		feed_input(p,2,0,"  /")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,3," ",core.M_OCCUPIED))
		
	def test_expects_right_leg_backslash(self):
		p = self.pclass()
		feed_input(p,0,3,   "O\n")
		feed_input(p,1,0,"  -|-\n")
		feed_input(p,2,0,"  / ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4,"U",core.M_NONE))
			
	def test_expects_right_leg_backslash_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,3,   "O\n")
		feed_input(p,1,0,"  -|-\n")
		feed_input(p,2,0,"  / ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4,"\\",core.M_OCCUPIED))
			
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((3,   "O   \n",),
				 (0,"  -|-  \n",),
				 (0,"  / \\",   ),)
		o = core.M_OCCUPIED
		n = core.M_NONE
		meta =  ((      o,n,n,n,n,),
				 (n,n,o,o,o,n,n,n,),
				 (n,n,o,o,o,      ),)
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,startcol+i,char,core.M_NONE))
				self.assertEquals(meta[j][i], m)

	def do_render(self,x,y):
		p = self.pclass()
		feed_input(p,y,x,     "O\n")
		feed_input(p,y+1,x-1,"-|-\n")
		feed_input(p,y+2,x-1,"/ \\")
		try:
			p.test(main.CurrentChar(y+2,x+2," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_correct_shapes(self):
		r = self.do_render(3,2)
		self.assertEquals(5,len(r))
		self.assertEquals(1,len(filter(lambda x: isinstance(x,core.Ellipse), r)))
		self.assertEquals(4,len(filter(lambda x: isinstance(x,core.Line), r)))
		
	def test_render_coordinates(self):
		r = self.do_render(3,2)
		head = filter(lambda x: isinstance(x,core.Ellipse), r)[0]
		self.assertEquals((3,2.5),head.a)
		self.assertEquals((4,3),head.b)
		arms = self.find_with(filter(lambda x: isinstance(x,core.Line), r),"a",(2,3.25))
		self.assertEquals((2,3.25),arms.a)
		self.assertEquals((5,3.25),arms.b)
		lleg = self.find_with(filter(lambda x: isinstance(x,core.Line), r),"b",(2.5,4.8))
		self.assertEquals((3.5,3.8),lleg.a)
		self.assertEquals((2.5,4.8),lleg.b)
		rleg = self.find_with(filter(lambda x: isinstance(x,core.Line), r),"b",(4.5,4.8))
		self.assertEquals((3.5,3.8),rleg.a)
		self.assertEquals((4.5,4.8),rleg.b)

	def test_render_z(self):
		r = self.do_render(3,2)
		for shape in r:
			self.assertEquals(0,shape.z)
			
	def test_render_stroke_colour(self):
		r = self.do_render(3,2)
		for shape in r:
			self.assertEquals(core.C_FOREGROUND,shape.stroke)
			
	def test_render_stroke_width(self):
		r = self.do_render(3,2)
		for shape in r:
			self.assertEquals(1,shape.w)
			
	def test_render_stroke_style(self):
		r = self.do_render(3,2)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID, shape.stype)
			
	def test_render_fill_colour(self):
		r = self.do_render(3,2)
		e = filter(lambda x: isinstance(x,core.Ellipse), r)[0]
		self.assertEquals(None, e.fill)


if __name__ == "__main__":
	unittest.main()
