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
import patterns
import main
import math

from ptests import *


class TestDbCylinderPattern(unittest.TestCase,PatternTests):

	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.DbCylinderPattern
	
	def test_accepts_cylinder(self):
		input = [
			".--.\n",
			"'--'\n",
			"|  |\n",
			"'--'\n",
			"    " ]
		p = self.pclass()
		for j,line in enumerate(input):
			for i,char in enumerate(line):
				p.test(main.CurrentChar(j,i,char,core.M_NONE))
		try:
			p.test(main.CurrentChar(len(input),0," ",core.M_NONE))
		except StopIteration: pass
		
	def test_expects_top_start_period(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,0,"p",core.M_NONE))
			
	def test_expects_top_start_period_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,0,".",core.M_OCCUPIED))
			
	def test_expects_top_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,0,".",core.M_NONE))
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,1,".",core.M_NONE))
			
	def test_expects_top_line_unoccupied(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,0,".",core.M_NONE))
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,0,"-",core.M_OCCUPIED))
			
	def test_expects_top_end_period(self):
		p = self.pclass()
		feed_input(p,0,0,".-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"?",core.M_NONE))
			
	def test_expects_top_end_period_unoccupie(self):
		p = self.pclass()
		feed_input(p,0,0,".-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,".",core.M_OCCUPIED))
		
	def test_allows_long_top_line(self):
		p = self.pclass()
		feed_input(p,0,1,".---.")

	def test_allows_rest_of_top_line(self):
		p = self.pclass()
		feed_input(p,0,1,".-.")
		p.test(main.CurrentChar(0,2,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,3,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,4,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_second_line(self):
		p = self.pclass()
		feed_input(p,0,2,".-.\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))		
	
	def test_expects_top_start_apos(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,0,"|",core.M_NONE))
			
	def test_expects_top_start_apos_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,0,"'",core.M_OCCUPIED))
	
	def test_expects_top_underline(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,1,"'",core.M_NONE))
	
	def test_expects_top_underline_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,1,"-",core.M_OCCUPIED))
	
	def test_rejects_top_underline_too_short(self):
		p = self.pclass()
		feed_input(p,0,0,".--.\n")
		feed_input(p,1,0,"'-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"'",core.M_NONE))
			
	def test_rejects_top_underline_too_lone(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"-",core.M_NONE))
	
	def test_expects_top_end_apos(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"a",core.M_NONE))
			
	def test_expects_top_end_apos_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"'",core.M_OCCUPIED))
	
	def test_allows_rest_of_second_line(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'")
		p.test(main.CurrentChar(1,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,4,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,5,"\n",core.M_OCCUPIED))
	
	def test_allows_start_of_third_line(self):
		p = self.pclass()
		feed_input(p,0,2,".-.\n")
		feed_input(p,1,0,"  '-'\n")
		p.test(main.CurrentChar(2,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,1,"x",core.M_OCCUPIED))
	
	def test_expects_mid_start_pipe(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,0,"'",core.M_NONE))
						
	def test_expects_mid_start_pipe_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,0,"|",core.M_OCCUPIED))
			
	def test_allows_mid_space(self):
		p = self.pclass()
		feed_input(p,0,0,".--.\n")
		feed_input(p,1,0,"'--'\n")
		feed_input(p,2,0,"|")
		p.test(main.CurrentChar(2,1,"p",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,2,"q",core.M_OCCUPIED))

	def test_rejects_short_mid_space_line(self):
		p = self.pclass()
		feed_input(p,0,0,".--.\n")
		feed_input(p,1,0,"'--'\n")
		feed_input(p,2,0,"| \n")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,0," ",core.M_NONE))
	
	def test_expects_mid_end_pipe(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"p",core.M_NONE))
			
	def test_expects_mid_end_pipe_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"|",core.M_OCCUPIED))
			
	def test_allows_end_of_third_line(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| |")
		p.test(main.CurrentChar(2,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,4,"z",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,5,"\n",core.M_OCCUPIED))	
	
	def test_allows_start_of_last_line(self):
		p = self.pclass()
		feed_input(p,0,2,  ".-.\n")
		feed_input(p,1,0,"  '-'\n")
		feed_input(p,2,0,"  | |\n")
		p.test(main.CurrentChar(3,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(3,1,"x",core.M_OCCUPIED))
		
	def test_expects_bottom_start_apos(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| |\n")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,0,"z",core.M_NONE))
		
	def test_expects_bottom_start_apos_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| |\n")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,0,"'",core.M_OCCUPIED))
			
	def test_expects_bottom_line(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| |\n")
		feed_input(p,3,0,"'")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,1,"'",core.M_NONE))
			
	def test_expects_bottom_line_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| |\n")
		feed_input(p,3,0,"'")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,1,"-",core.M_OCCUPIED))
	
	def test_rejects_bottom_line_too_short(self):
		p = self.pclass()
		feed_input(p,0,0,".--.\n")
		feed_input(p,1,0,"'--'\n")
		feed_input(p,2,0,"|  |\n")
		feed_input(p,3,0,"'-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,2,"'",core.M_NONE))
	
	def test_rejects_bottom_line_too_long(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| |\n")
		feed_input(p,3,0,"'-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,2,"-",core.M_NONE))
			
	def test_expects_bottom_end_apos(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| |\n")
		feed_input(p,3,0,"'-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,2,"z",core.M_NONE))
			
	def test_expects_bottom_end_apos_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| |\n")
		feed_input(p,3,0,"'-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,2,"'",core.M_OCCUPIED))
			
	def test_allows_rest_of_last_line(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| |\n")
		feed_input(p,3,0,"'-'ab\n")
		
	def test_accepts_partial_line_after(self):
		p = self.pclass()
		feed_input(p,0,0,".--.\n")
		feed_input(p,1,0,"'--'\n")
		feed_input(p,2,0,"|  |\n")
		feed_input(p,3,0,"'--'\n")
		feed_input(p,4,0,"ab\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(5,0,"c",core.M_NONE))
			
	def test_accepts_no_line_after(self):
		p = self.pclass()
		feed_input(p,0,0,".--.\n")
		feed_input(p,1,0,"'--'\n")
		feed_input(p,2,0,"|  |\n")
		feed_input(p,3,0,"'--'\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(4,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_multiple_mid_lines(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| |\n")
		feed_input(p,3,0,"| |\n")
		feed_input(p,4,0,"| |\n")
		
	def test_sets_correct_meta_flags(self):
		input = ((2,  ".---.  \n",),
		         (0,"  '---'  \n",),
		         (0,"  |   |  \n",),
		         (0,"  '---'  \n",),
		         (0,"       "    ,))
		c = core.M_OCCUPIED | core.M_BOX_START_S | core.M_BOX_START_E
		t = core.M_OCCUPIED | core.M_BOX_START_S
		l = core.M_OCCUPIED | core.M_BOX_START_E
		n = core.M_NONE
		o = core.M_OCCUPIED
		r = core.M_BOX_AFTER_E
		b = core.M_BOX_AFTER_S
		meta =  ((    c,t,t,t,t,r,n,n,),
				 (n,n,l,o,o,o,o,r,n,n,),
				 (n,n,l,n,n,n,o,r,n,n,),
				 (n,n,l,o,o,o,o,r,n,n,),
				 (n,n,b,b,b,b,b       ))
		p = self.pclass()
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,startcol+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)

	def do_render(self,x,y,w,h):
		p = self.pclass()
		feed_input(p,y,x,                "." + "-"*w + ".\n")
		feed_input(p,y+1,0,      " "*x + "'" + "-"*w + "'\n")
		for i in range(h):
			feed_input(p,y+2+i,0," "*x + "|" + " "*w + "|\n")
		feed_input(p,y+2+h,0,    " "*x + "'" + "-"*w + "'\n")
		feed_input(p,y+2+h+1,0,  " "*x + " " + " "*w + " "  )
		try:
			p.test(main.CurrentChar(y+2+h+1,x+1+w+1,"\n",core.M_NONE))
		except StopIteration: pass
		return p.render()
			
	def test_render_returns_correct_shapes(self):
		result = self.do_render(2,2,3,1)
		self.assertEquals(4,len(result))
		self.assertEquals(1,len(filter(lambda x: isinstance(x,core.Ellipse), result)))
		self.assertEquals(1,len(filter(lambda x: isinstance(x,core.Arc), result)))
		self.assertEquals(2,len(filter(lambda x: isinstance(x,core.Line), result)))
			
	def test_render_line_coordinates(self):
		lines = filter(lambda x: isinstance(x,core.Line), self.do_render(2,2,3,1))
		linea = self.find_with(lines,"a",(2.5,3))
		self.assertEquals((2.5,5),linea.b)
		lineb = self.find_with(lines,"a",(6.5,3))
		self.assertEquals((6.5,5),lineb.b)
		
	def test_render_line_coordinates_wider(self):
		lines = filter(lambda x: isinstance(x,core.Line), self.do_render(5,1,5,1))
		linea = self.find_with(lines,"a",(5.5,2))
		self.assertEquals((5.5,4),linea.b)
		lineb = self.find_with(lines,"a",(11.5,2))
		self.assertEquals((11.5,4),lineb.b)
		
	def test_render_line_coordinates_taller(self):
		lines = filter(lambda x: isinstance(x,core.Line), self.do_render(3,2,3,3))
		linea = self.find_with(lines,"a",(3.5,3))
		self.assertEquals((3.5,7), linea.b)
		lineb = self.find_with(lines,"a",(7.5,3))
		self.assertEquals((7.5,7), lineb.b)
		
	def test_render_ellipse_coordinates(self):
		ellipse = filter(lambda x: isinstance(x,core.Ellipse), self.do_render(2,2,3,1))[0]
		self.assertEquals((2.5,2.5),ellipse.a)
		self.assertEquals((6.5,3.5),ellipse.b)
		
	def test_render_ellipse_coordinates_wider(self):
		ellipse = filter(lambda x: isinstance(x,core.Ellipse), self.do_render(3,2,4,1))[0]
		self.assertEquals((3.5,2.5),ellipse.a)
		self.assertEquals((8.5,3.5),ellipse.b)

	def test_render_ellipse_coordinates_taller(self):
		ellipse = filter(lambda x: isinstance(x,core.Ellipse), self.do_render(4,1,3,3))[0]
		self.assertEquals((4.5,1.5),ellipse.a)
		self.assertEquals((8.5,2.5),ellipse.b)
		
	def test_render_arc_coordinates(self):
		arc = filter(lambda x: isinstance(x,core.Arc), self.do_render(2,2,3,1))[0]
		self.assertEquals((2.5,4.5),arc.a)
		self.assertEquals((6.5,5.5),arc.b)
		self.assertEquals(0,arc.start)
		self.assertEquals(math.pi,arc.end)
		
	def test_render_arc_coordinates_wider(self):
		arc = filter(lambda x: isinstance(x,core.Arc), self.do_render(3,1,4,1))[0]
		self.assertEquals((3.5,3.5),arc.a)
		self.assertEquals((8.5,4.5),arc.b)
		self.assertEquals(0,arc.start)
		self.assertEquals(math.pi,arc.end)
	
	def test_render_arc_coordinates_taller(self):
		arc = filter(lambda x: isinstance(x,core.Arc), self.do_render(2,2,3,4))[0]
		self.assertEquals((2.5,7.5),arc.a)
		self.assertEquals((6.5,8.5),arc.b)
		self.assertEquals(0,arc.start)
		self.assertEquals(math.pi,arc.end)
	
	def test_render_z(self):
		result = self.do_render(2,2,3,4)
		for r in result:
			self.assertEquals(0,r.z)
				
	def test_render_stroke_colour(self):
		result = self.do_render(2,2,3,4)
		for r in result:
			self.assertEquals(core.C_FOREGROUND,r.stroke)
			
	def test_render_stroke_width(self):
		result = self.do_render(2,2,3,4)
		for r in result:
			self.assertEquals(1,r.w)

	def test_render_stroke_style(self):
		result = self.do_render(2,2,3,4)
		for r in result:
			self.assertEquals(core.STROKE_SOLID,r.stype)
			
	def test_render_fill_colour(self):
		result = filter(lambda x: not isinstance(x,core.Line), self.do_render(2,2,3,4))
		for r in result:
			self.assertEquals(None,r.fill)



class TestStraightRectangularBoxPattern(unittest.TestCase,PatternTests):

	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.StraightRectangularBoxPattern	
	
	def test_accepts_box(self):
		p = self.pclass()
		feed_input(p,0,2,  "+-----+ \n")
		feed_input(p,1,0,"  |     | \n")
		feed_input(p,2,0,"  |     | \n")
		feed_input(p,3,0,"  +-----+ \n")
		feed_input(p,4,0,"         ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,9," ",core.M_NONE))
			
	def test_expects_top_left_plus(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"?",core.M_NONE))
			
	def test_expects_top_left_plus_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"+",core.M_OCCUPIED))
			
	def test_expects_top_hyphen(self):
		p = self.pclass()
		feed_input(p,0,2,"+")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"+",core.M_NONE))
			
	def test_expects_top_hyphen_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,"+")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"-",core.M_OCCUPIED))
			
	def test_allows_single_char_width(self):
		p = self.pclass()
		feed_input(p,0,2,"+-+")
			
	def test_expects_top_right_plus(self):
		p = self.pclass()
		feed_input(p,0,2,"+-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"?",core.M_NONE))
			
	def test_expects_top_right_plus_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,"+-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"+",core.M_OCCUPIED))
			
	def test_allows_long_width(self):
		p = self.pclass()
		feed_input(p,0,2,"+-------------+")
	
	def test_allows_rest_of_first_line(self):
		p = self.pclass()
		feed_input(p,0,2,"+---+")
		p.test(main.CurrentChar(0,7,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,8,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,9,"\n",core.M_OCCUPIED))
	
	def test_allows_start_of_second_line(self):
		p = self.pclass()
		feed_input(p,0,2,"+---+\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		
	def test_expects_left_pipe(self):
		p = self.pclass()
		feed_input(p,0,2,"+---+\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"+",core.M_NONE))
			
	def test_expects_left_pipe_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,"+---+\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"|",core.M_OCCUPIED))
	
	def test_allows_box_contents(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |")
		p.test(main.CurrentChar(1,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,4,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,5,"c",core.M_OCCUPIED))
		
	def test_rejects_short_content_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,5,"\n",core.M_NONE))
		
	def test_expects_right_pipe(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,6,"a",core.M_NONE))
			
	def test_expects_right_pipe_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,6,"|",core.M_OCCUPIED))
			
	def test_allows_rest_of_second_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |")
		p.test(main.CurrentChar(1,7,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,8,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,9,"\n",core.M_OCCUPIED))
	
	def test_allows_start_of_bottom_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		p.test(main.CurrentChar(2,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,1,"b",core.M_OCCUPIED))
		
	def test_allows_single_char_height(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  +")
		
	def test_expects_bottom_left_plus(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"?",core.M_NONE))
	
	def test_expects_bottom_left_plus_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"+",core.M_OCCUPIED))
			
	def test_allows_long_height(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  |   |\n")
		feed_input(p,3,0,"  |   |\n")
		feed_input(p,4,0,"  +")
		
	def test_expects_bottom_hyphen(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  +")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,3,"+",core.M_NONE))
	
	def test_expects_bottom_hyphen_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  +")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,3,"-",core.M_OCCUPIED))
			
	def test_expects_bottom_right_plus(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  +---")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,6,"-",core.M_NONE))
			
	def test_expects_bottom_right_plus_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  +---")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,6,"+",core.M_OCCUPIED))
			
	def test_allows_rest_of_bottom_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  +---+")
		p.test(main.CurrentChar(2,7,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,8,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,9,"\n",core.M_OCCUPIED))
		
	def test_allows_final_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  +---+\n")
		for i in range(7):
			p.test(main.CurrentChar(3,i,"z",core.M_OCCUPIED))
			
	def test_allows_no_final_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  +---+\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_short_final_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  +---+\n")
		feed_input(p,3,0,"    ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,4,"\n",core.M_NONE))

	def test_allowed_to_touch_left_edge(self):
		p = self.pclass()
		feed_input(p,0,0,"+---+\n")
		feed_input(p,1,0,"|   |\n")
		feed_input(p,2,0,"+---+\n")
		feed_input(p,3,0,"     ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,5,"\n",core.M_NONE))
			
	def test_allowed_to_touch_bottom_left_corner(self):
		p = self.pclass()
		feed_input(p,0,0,"+---+\n")
		feed_input(p,1,0,"|   |\n")
		feed_input(p,2,0,"+---+\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
	
	def test_allows_h_separator(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |----|\n")
			
	def test_expects_continuation_of_h_separator(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4," ",core.M_NONE))
			
	def test_expects_continuation_of_h_separator_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4,"-",core.M_OCCUPIED))
			
	def test_allows_non_separator_h_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  | ---|\n")
		
	def test_allows_h_non_separator_start_if_occupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |")
		p.test(main.CurrentChar(2,3,"-",core.M_OCCUPIED))
		feed_input(p,2,4,"---|\n")
	
	def test_doesnt_assume_h_separator_if_first_row(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |--- |\n")
		
	def test_doesnt_assume_h_separator_if_section_too_small(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |----|\n")
		feed_input(p,3,0,"  |--  |\n")
		
	def test_allows_multiple_h_separators(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |----|\n")
		feed_input(p,3,0,"  |    |\n")
		feed_input(p,4,0,"  |----|\n")
	
	def test_allows_v_separator(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |  | |\n")
		feed_input(p,3,0,"  +----+\n")
		
	def test_expects_continuation_of_v_separator(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,5," ",core.M_NONE))
			
	def test_expects_continuation_of_v_separator_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,5,"|",core.M_OCCUPIED))
	
	def test_allows_non_separator_v_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |  | |\n")
		feed_input(p,3,0,"  |  | |\n")
		feed_input(p,4,0,"  +----+\n")
	
	def test_allows_v_non_separator_start_if_occupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  ")
		p.test(main.CurrentChar(1,5,"|",core.M_OCCUPIED))
		feed_input(p,1,6," |\n")
	
	def test_allows_multiple_v_separators(self):
		p = self.pclass()
		feed_input(p,0,2,  "+-----+\n")
		feed_input(p,1,0,"  | | | |\n")
		feed_input(p,2,0,"  | | | |\n")
		feed_input(p,3,0,"  +-----+\n")
	
	def test_doesnt_assume_v_separator_if_first_col(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  ||   |\n")
		feed_input(p,2,0,"  ||   |\n")
		feed_input(p,3,0,"  |    |\n")
		
	def test_doesnt_assume_v_separator_if_section_too_small(self):
		p = self.pclass()
		feed_input(p,0,2,  "+-----+\n")
		feed_input(p,1,0,"  |  || |\n")
		feed_input(p,2,0,"  |  || |\n")
		feed_input(p,3,0,"  |  |  |\n")
	
	def test_allows_crossing_separators(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |----|\n")
		feed_input(p,3,0,"  |  | |\n")
		feed_input(p,4,0,"  +----+\n")
		
	def test_expects_line_at_separator_intersection(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |--")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,5,"+",core.M_NONE))
			
	def test_expects_line_at_separator_intersection_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |--")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,5,"-",core.M_OCCUPIED))

	def test_allows_vertical_line_at_separator_intersection(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |--|-|\n")

	def test_allows_single_character_sections(self):
		p = self.pclass()
		feed_input(p,0,2,  "+-----+\n")
		feed_input(p,1,0,"  | | | |\n")
		feed_input(p,2,0,"  |-----|\n")
		feed_input(p,3,0,"  | | | |\n")
		feed_input(p,4,0,"  |-----|\n")
		feed_input(p,5,0,"  | | | |\n")
		feed_input(p,6,0,"  +-----+\n")

	def test_allows_dashed_box(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - - - +\n")
		feed_input(p,1,0,"  ;        ;\n")
		feed_input(p,2,0,"  ;        ;\n")
		feed_input(p,3,0,"  +- - - - +\n")
		feed_input(p,4,0,"            ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(4,12," ",core.M_NONE))
	
	def test_expects_top_dash_continuation(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- -")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,6,"-",core.M_NONE))
			
	def test_expects_top_dash_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4," ",core.M_OCCUPIED))
	
	def test_top_expects_complete_dashes(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- -")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,6,"+",core.M_NONE))
	
	def test_expects_dashed_left_side(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - +\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"|",core.M_NONE))
	
	def test_expects_dashed_left_side_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,   "+- - +\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,";",core.M_OCCUPIED))
	
	def test_expects_dashed_right_side(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - +\n")
		feed_input(p,1,0,"  ;    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,7,"|",core.M_NONE))
			
	def test_expects_dashed_right_side_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - +\n")
		feed_input(p,1,0,"  ;    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,7,";",core.M_OCCUPIED))
			
	def test_expects_dashed_left_side_second_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - +\n")
		feed_input(p,1,0,"  ;    ;\n")
		feed_input(p,2,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"|",core.M_NONE))
			
	def test_expects_dashed_left_side_second_line_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - +\n")
		feed_input(p,1,0,"  ;    ;\n")
		feed_input(p,2,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,";",core.M_OCCUPIED))
			
	def test_expects_dashed_right_side_second_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - +\n")
		feed_input(p,1,0,"  ;    ;\n")
		feed_input(p,2,0,"  ;    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,7,"|",core.M_NONE))
		
	def test_expects_dashed_right_side_second_line_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - +\n")
		feed_input(p,1,0,"  ;    ;\n")
		feed_input(p,2,0,"  ;    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,7,";",core.M_OCCUPIED))
			
	def test_expects_dashed_bottom_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - +\n")
		feed_input(p,1,0,"  ;    ;\n")
		feed_input(p,2,0,"  +-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4,"-",core.M_NONE))
	
	def test_expects_dashed_bottom_line_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - +\n")
		feed_input(p,1,0,"  ;    ;\n")
		feed_input(p,2,0,"  +-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4," ",core.M_OCCUPIED))
	
	def test_expects_dashed_bottom_line_continuation(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - - - +\n")
		feed_input(p,1,0,"  ;        ;\n")
		feed_input(p,2,0,"  +- -")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,6,"-",core.M_NONE))
			
	def test_expects_dashed_bottom_line_continuation_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - - - +\n")
		feed_input(p,1,0,"  ;        ;\n")
		feed_input(p,2,0,"  +- -")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,6," ",core.M_OCCUPIED))
	
	def test_dashed_box_allows_separators(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - - - - - +\n")
		feed_input(p,1,0,"  ;   |    |   ;\n")
		feed_input(p,2,0,"  ;--------|---;\n")
		feed_input(p,3,0,"  ;   |    |   ;\n")
		feed_input(p,4,0,"  +- - - - - - +\n")
	
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((2,  "+---+  \n",),
				 (0,"  |+|||  \n",),
				 (0,"  |---|  \n",),
				 (0,"  |-| |  \n",),
				 (0,"  +---+  \n",),
				 (0,"       ",    ),)
		c = core.M_BOX_START_S | core.M_BOX_START_E | core.M_OCCUPIED
		t = core.M_BOX_START_S | core.M_OCCUPIED
		l = core.M_BOX_START_E | core.M_OCCUPIED
		o = core.M_OCCUPIED
		n = core.M_NONE
		r = core.M_BOX_AFTER_E
		b = core.M_BOX_AFTER_S
		outmeta = ((    c,t,t,t,t,r,n,n,),
				   (n,n,l,n,o,n,o,r,n,n,),
				   (n,n,l,o,o,o,o,r,n,n,),
				   (n,n,l,n,o,n,o,r,n,n,),
				   (n,n,l,o,o,o,o,r,n,n,),
				   (n,n,b,b,b,b,b,      ),)
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				m = outmeta[j][i]
				self.assertEquals(m, p.test(main.CurrentChar(j,startcol+i,char,core.M_NONE)))
		 
	def do_render(self,x,y,w,h,hs=[],vs=[],dash=False):
		p = self.pclass()
		feed_input(p,y,x,"+" + (("- "*(w//2)) if dash else ("-"*w)) + "+\n")
		for i in range(h):
			feed_input(p,y+1+i,0," "*x + (";" if dash else "|"))
			for n in range(w):
				chr = { 
					(True,True): "-",
				  	(True,False): "-",
				  	(False,True): "|",
				  	(False,False): " " 
				}[(i in hs,n in vs)]
				feed_input(p,y+1+i,x+1+n, chr)
			feed_input(p,y+1+i,x+1+w, (";" if dash else "|")+"\n")
		feed_input(p,y+1+h+0,0," "*x + "+" + (("- "*(w//2)) if dash else ("-"*w)) + "+\n")
		feed_input(p,y+1+h+1,0," "*x + " " + " "*w + " ")
		try:
			p.test(main.CurrentChar(y+h+2,x+w+2," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
			
	def test_render_returns_correct_shapes(self):
		r = self.do_render(2,3,5,6)
		self.assertEquals(1, len(r))
		self.assertTrue( isinstance(r[0],core.Rectangle) )
		
	def test_render_coordinates(self):
		r = self.do_render(2,3,5,6)[0]
		self.assertEquals((2.5,3.5),r.a)
		self.assertEquals((8.5,10.5),r.b)
		
	def test_render_coordinates_width(self):
		r = self.do_render(2,3,7,6)[0]
		self.assertEquals((2.5,3.5),r.a)
		self.assertEquals((10.5,10.5),r.b)
		
	def test_render_coordinates_height(self):
		r = self.do_render(2,3,5,8)[0]
		self.assertEquals((2.5,3.5),r.a)
		self.assertEquals((8.5,12.5),r.b)
		
	def test_render_coordinates_position(self):
		r = self.do_render(7,5,5,6)[0]
		self.assertEquals((7.5,5.5),r.a)
		self.assertEquals((13.5,12.5),r.b)
	
	def test_render_z(self):
		r = self.do_render(2,3,5,6)[0]
		self.assertEquals(0,r.z)
		
	def test_render_stroke_colour(self):
		r = self.do_render(2,3,5,6)[0]
		self.assertEquals(core.C_FOREGROUND,r.stroke)

	def test_render_stroke_alpha(self):
		r = self.do_render(2,3,5,6)[0]
		self.assertEquals(1.0,r.salpha)
		
	def test_render_stroke_width(self):
		r = self.do_render(2,3,5,6)[0]
		self.assertEquals(1,r.w)
		
	def test_render_stroke_style_solid(self):
		r = self.do_render(2,3,6,6,dash=False)[0]
		self.assertEquals(core.STROKE_SOLID,r.stype)
		
	def test_render_stroke_style_dashed(self):
		r = self.do_render(2,3,6,6,dash=True)[0]
		self.assertEquals(core.STROKE_DASHED,r.stype)
		
	def test_render_fill_colour(self):
		r = self.do_render(2,3,5,6)[0]
		self.assertEquals(None,r.fill)
		
	def test_render_fill_alpha(self):
		r = self.do_render(2,3,5,6)[0]
		self.assertEquals(1.0,r.falpha)
		
	def test_render_h_sections_returns_background_shapes(self):
		r = self.do_render(3,2,12,4,[],[4,8])
		self.assertEquals(4,len(self.find_type(r,core.Rectangle)))
			
	def test_render_h_sections_coordinates(self):
		r = self.do_render(3,2,12,4,[],[4,8])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(b1.a,(3.5,2.5))
		b2 = self.find_with(r,"b",(12.5,7.5))
		self.assertEquals(b2.a,(8.5,2.5))
		b3 = self.find_with(r,"a",(12.5,2.5))
		self.assertEquals(b3.b,(16.5,7.5))
		
	def test_render_h_sections_stroke_colour(self):
		r = self.do_render(3,2,12,4,[],[4,8])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(None,b1.stroke)
		b2 = self.find_with(r,"b",(12.5,7.5))
		self.assertEquals(None,b2.stroke)
		b3 = self.find_with(r,"a",(12.5,2.5))
		self.assertEquals(None,b3.stroke)
		
	def test_render_h_sections_fill_colour(self):
		r = self.do_render(3,2,12,4,[],[4,8])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(core.C_FOREGROUND,b1.fill)
		b2 = self.find_with(r,"b",(12.5,7.5))
		self.assertEquals(core.C_FOREGROUND,b2.fill)
		b3 = self.find_with(r,"a",(12.5,2.5))
		self.assertEquals(core.C_FOREGROUND,b3.fill)
		
	def test_render_h_sections_fill_alpha(self):
		r = self.do_render(3,2,12,4,[],[4,8])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(0.25,b1.falpha)
		b2 = self.find_with(r,"b",(12.5,7.5))
		self.assertEquals(0.0,b2.falpha)
		b3 = self.find_with(r,"a",(12.5,2.5))
		self.assertEquals(0.25,b3.falpha)
		
	def test_render_h_sections_z(self):
		r = self.do_render(3,2,12,4,[],[4,8])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(-0.5,b1.z)
		b2 = self.find_with(r,"b",(12.5,7.5))
		self.assertEquals(-0.5,b2.z)
		b3 = self.find_with(r,"a",(12.5,2.5))
		self.assertEquals(-0.5,b3.z)
	
	def test_render_v_sections_returns_correct_shapes(self):
		r = self.do_render(3,2,4,12,[4,8],[])
		self.assertEquals(4,len(self.find_type(r,core.Rectangle)))
		
	def test_render_v_sections_coordinates(self):
		r = self.do_render(3,2,4,12,[4,8],[])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(b1.a,(3.5,2.5))
		b2 = self.find_with(r,"b",(8.5,11.5))
		self.assertEquals(b2.a,(3.5,7.5))
		b3 = self.find_with(r,"a",(3.5,11.5))
		self.assertEquals(b3.b,(8.5,15.5))
		
	def test_render_v_sections_stroke_colour(self):
		r = self.do_render(3,2,4,12,[4,8],[])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(b1.stroke,None)
		b2 = self.find_with(r,"b",(8.5,11.5))
		self.assertEquals(b2.stroke,None)
		b3 = self.find_with(r,"a",(3.5,11.5))
		self.assertEquals(b3.stroke,None)
		
	def test_render_v_sections_fill_colour(self):
		r = self.do_render(3,2,4,12,[4,8],[])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(b1.fill,core.C_FOREGROUND)
		b2 = self.find_with(r,"b",(8.5,11.5))
		self.assertEquals(b2.fill,core.C_FOREGROUND)
		b3 = self.find_with(r,"a",(3.5,11.5))
		self.assertEquals(b3.fill,core.C_FOREGROUND)
			
	def test_render_v_sections_fill_alpha(self):
		r = self.do_render(3,2,4,12,[4,8],[])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(b1.falpha,0.25)
		b2 = self.find_with(r,"b",(8.5,11.5))
		self.assertEquals(b2.falpha,0.0)
		b3 = self.find_with(r,"a",(3.5,11.5))
		self.assertEquals(b3.falpha,0.25)
		
	def test_render_v_sections_z(self):
		r = self.do_render(3,2,4,12,[4,8],[])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(-0.5,b1.z)
		b2 = self.find_with(r,"b",(8.5,11.5))
		self.assertEquals(-0.5,b2.z)
		b3 = self.find_with(r,"a",(3.5,11.5))
		self.assertEquals(-0.5,b3.z)
			
	def test_render_hv_sections_returns_correct_shapes(self):
		r = self.do_render(3,2,12,13,[4,8],[4,8])
		self.assertEquals(10,len(self.find_type(r,core.Rectangle)))
		
	def test_render_hv_sections_coordinates(self):
		r = self.do_render(3,2,12,13,[4,8],[4,8])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(b1.a,(3.5,2.5))
		b2 = self.find_with(r,"b",(8.5,11.5))
		self.assertEquals(b2.a,(3.5,7.5))
		b3 = self.find_with(r,"a",(3.5,11.5))
		self.assertEquals(b3.b,(8.5,16.5))
		b4 = self.find_with(r,"b",(12.5,7.5))
		self.assertEquals(b4.a,(8.5,2.5))
		b5 = self.find_with(r,"b",(12.5,11.5))
		self.assertEquals(b5.a,(8.5,7.5))
		b6 = self.find_with(r,"a",(8.5,11.5))
		self.assertEquals(b6.b,(12.5,16.5))		
		b7 = self.find_with(r,"b",(16.5,7.5))
		self.assertEquals(b7.a,(12.5,2.5))
		b8 = self.find_with(r,"b",(16.5,11.5))
		self.assertEquals(b8.a,(12.5,7.5))
		b9 = self.find_with(r,"a",(12.5,11.5))
		self.assertEquals(b9.b,(16.5,16.5))
			
	def test_render_hv_sections_stroke_colour(self):
		r = self.do_render(3,2,12,13,[4,8],[4,8])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(None,b1.stroke)
		b2 = self.find_with(r,"b",(8.5,11.5))
		self.assertEquals(None,b2.stroke)
		b3 = self.find_with(r,"a",(3.5,11.5))
		self.assertEquals(None,b3.stroke)
		b4 = self.find_with(r,"b",(12.5,7.5))
		self.assertEquals(None,b4.stroke)
		b5 = self.find_with(r,"b",(12.5,11.5))
		self.assertEquals(None,b5.stroke)
		b6 = self.find_with(r,"a",(8.5,11.5))
		self.assertEquals(None,b6.stroke)		
		b7 = self.find_with(r,"b",(16.5,7.5))
		self.assertEquals(None,b7.stroke)
		b8 = self.find_with(r,"b",(16.5,11.5))
		self.assertEquals(None,b8.stroke)
		b9 = self.find_with(r,"a",(12.5,11.5))
		self.assertEquals(None,b9.stroke)
			
	def test_render_hv_sections_fill_colour(self):
		r = self.do_render(3,2,12,13,[4,8],[4,8])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(core.C_FOREGROUND,b1.fill)
		b2 = self.find_with(r,"b",(8.5,11.5))
		self.assertEquals(core.C_FOREGROUND,b2.fill)
		b3 = self.find_with(r,"a",(3.5,11.5))
		self.assertEquals(core.C_FOREGROUND,b3.fill)
		b4 = self.find_with(r,"b",(12.5,7.5))
		self.assertEquals(core.C_FOREGROUND,b4.fill)
		b5 = self.find_with(r,"b",(12.5,11.5))
		self.assertEquals(core.C_FOREGROUND,b5.fill)
		b6 = self.find_with(r,"a",(8.5,11.5))
		self.assertEquals(core.C_FOREGROUND,b6.fill)		
		b7 = self.find_with(r,"b",(16.5,7.5))
		self.assertEquals(core.C_FOREGROUND,b7.fill)
		b8 = self.find_with(r,"b",(16.5,11.5))
		self.assertEquals(core.C_FOREGROUND,b8.fill)
		b9 = self.find_with(r,"a",(12.5,11.5))
		self.assertEquals(core.C_FOREGROUND,b9.fill)
			
	def test_render_hv_sections_fill_alpha(self):
		r = self.do_render(3,2,12,13,[4,8],[4,8])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(0.25,b1.falpha)
		b2 = self.find_with(r,"b",(8.5,11.5))
		self.assertEquals(0.125,b2.falpha)
		b3 = self.find_with(r,"a",(3.5,11.5))
		self.assertEquals(0.25,b3.falpha)
		b4 = self.find_with(r,"b",(12.5,7.5))
		self.assertEquals(0.125,b4.falpha)
		b5 = self.find_with(r,"b",(12.5,11.5))
		self.assertEquals(0.0,b5.falpha)
		b6 = self.find_with(r,"a",(8.5,11.5))
		self.assertEquals(0.125,b6.falpha)		
		b7 = self.find_with(r,"b",(16.5,7.5))
		self.assertEquals(0.25,b7.falpha)
		b8 = self.find_with(r,"b",(16.5,11.5))
		self.assertEquals(0.125,b8.falpha)
		b9 = self.find_with(r,"a",(12.5,11.5))
		self.assertEquals(0.25,b9.falpha)
		
	def test_render_hv_sections_z(self):
		r = self.do_render(3,2,12,13,[4,8],[4,8])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(-0.5,b1.z)
		b2 = self.find_with(r,"b",(8.5,11.5))
		self.assertEquals(-0.5,b2.z)
		b3 = self.find_with(r,"a",(3.5,11.5))
		self.assertEquals(-0.5,b3.z)
		b4 = self.find_with(r,"b",(12.5,7.5))
		self.assertEquals(-0.5,b4.z)
		b5 = self.find_with(r,"b",(12.5,11.5))
		self.assertEquals(-0.5,b5.z)
		b6 = self.find_with(r,"a",(8.5,11.5))
		self.assertEquals(-0.5,b6.z)		
		b7 = self.find_with(r,"b",(16.5,7.5))
		self.assertEquals(-0.5,b7.z)
		b8 = self.find_with(r,"b",(16.5,11.5))
		self.assertEquals(-0.5,b8.z)
		b9 = self.find_with(r,"a",(12.5,11.5))
		self.assertEquals(-0.5,b9.z)


class TestParagmBoxPattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.ParagmBoxPattern
		
	def test_accepts_box(self):
		p = self.pclass()
		feed_input(p,0,4,    "+----+\n")
		feed_input(p,1,0,"   /    / \n")
		feed_input(p,2,0,"  /    /  \n")
		feed_input(p,3,0," +----+   \n")
		feed_input(p,4,0,"       ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(4,7," ",core.M_NONE))

	def test_expects_start_plus(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4," ",core.M_NONE))
			
	def test_expects_start_plus_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"+",core.M_OCCUPIED))

	def test_expects_top_line_hyphen(self):
		p = self.pclass()
		feed_input(p,0,4,"+")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,5,"+",core.M_NONE))
			
	def test_expects_top_line_hyphen_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,4,"+")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,5,"-",core.M_OCCUPIED))
			
	def test_expects_top_right_plus(self):
		p = self.pclass()
		feed_input(p,0,4,"+-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,6," ",core.M_NONE))
			
	def test_expects_top_right_plus_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,4,"+-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,6,"+",core.M_OCCUPIED))

	def test_allows_long_top_line(self):
		p = self.pclass()
		feed_input(p,0,4,"+----+")

	def test_allows_rest_of_top_line(self):
		p = self.pclass()
		feed_input(p,0,4,"+--+")
		p.test(main.CurrentChar(0,8,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,9,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,10,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_second_line(self):
		p = self.pclass()
		feed_input(p,0,4,"+--+\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,2,"c",core.M_OCCUPIED))
		
	def test_expects_second_line_left_forwardslash(self):
		p = self.pclass()
		feed_input(p,0,4,    "+--+\n")
		feed_input(p,1,0,"   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,3,"|",core.M_NONE))
			
	def test_expects_second_line_left_forwardslash_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,4,    "+--+\n")
		feed_input(p,1,0,"   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,3,"/",core.M_OCCUPIED))

	def test_allows_box_contents(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /")
		p.test(main.CurrentChar(1,4,"x",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,5,"y",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,6,"z",core.M_OCCUPIED))

	def test_rejects_short_content_line(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   / ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,5,"\n",core.M_NONE))
			p.test(main.CurrentChar(2,0," ",core.M_NONE))

	def test_expects_second_line_right_forwardslash(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,7," ",core.M_NONE))
			
	def test_expects_second_line_right_forwardslash(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,7,"/",core.M_OCCUPIED))

	def test_allows_rest_of_content_line(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   /")
		p.test(main.CurrentChar(1,8,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,9,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,10,"\n",core.M_OCCUPIED))

	def test_allows_start_of_third_line(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   / \n")
		p.test(main.CurrentChar(2,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,1,"b",core.M_OCCUPIED))

	def test_expects_bottom_left_plus(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   /\n")
		feed_input(p,2,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"-",core.M_NONE))
			
	def test_expects_bottom_left_plus_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   /\n")
		feed_input(p,2,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"+",core.M_OCCUPIED))

	def test_expects_left_forwardslash_unoccupied_for_second_content_line(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   /\n")
		feed_input(p,2,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"/",core.M_OCCUPIED))

	def test_allows_second_content_line(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   /\n")
		feed_input(p,2,0,"  /")
		p.test(main.CurrentChar(2,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,4,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,5,"c",core.M_OCCUPIED))

	def test_expects_right_forwardslash_for_second_content_line(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   /\n")
		feed_input(p,2,0,"  /   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,6,"-",core.M_NONE))

	def test_expects_right_forwardslash_unoccupied_for_second_content_line(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   /\n")
		feed_input(p,2,0,"  /   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,6,"/",core.M_OCCUPIED))

	def test_expects_bottom_line_hyphen(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   /\n")
		feed_input(p,2,0,"  +")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,3," ",core.M_NONE))
			
	def test_expects_bottom_line_hyphen_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   /\n")
		feed_input(p,2,0,"  +")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,3,"-",core.M_OCCUPIED))
			
	def test_expects_end_plus(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   /\n")
		feed_input(p,2,0,"  +---")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,6,"-",core.M_NONE))
			
	def test_expects_end_plus_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   /\n")
		feed_input(p,2,0,"  +---")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,6,"+",core.M_OCCUPIED))
			
	def test_allows_final_line(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   /\n")
		feed_input(p,2,0,"  +---+ \n")
		for i in range(7):
			p.test(main.CurrentChar(3,i,"z",core.M_OCCUPIED))
			
	def test_allows_no_final_line(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   /\n")
		feed_input(p,2,0,"  +---+ \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_short_final_line(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   /\n")
		feed_input(p,2,0,"  +---+ \n")
		feed_input(p,3,0,"    ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,4,"\n",core.M_NONE))
			
	def test_allowed_to_touch_left_edge(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0," /   /\n")
		feed_input(p,2,0,"+---+\n")
		feed_input(p,3,0,"     ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,5," ",core.M_NONE))
	
	def test_allowed_to_touch_bottom_left_corner(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0," /   /\n")
		feed_input(p,2,0,"+---+\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
	
	"""	
	def test_allows_h_separator(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   /\n")
		feed_input(p,2,0,"  /---/\n")
			
	def test_expects_continuation_of_h_separator(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   /\n")
		feed_input(p,2,0,"  /-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4," ",core.M_NONE))
			
	def test_expects_continuation_of_h_separator_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   /\n")
		feed_input(p,2,0,"  /-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4,"-",core.M_OCCUPIED))
			
	def test_allows_non_separator_h_line(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   /\n")
		feed_input(p,2,0,"  / --/\n")
		
	def test_allows_h_non_separator_start_if_occupied(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /   /\n")
		feed_input(p,2,0,"  /")
		p.test(main.CurrentChar(2,3,"-",core.M_OCCUPIED))
		feed_input(p,2,4,"--/\n")
	
	def test_doesnt_assume_h_separator_if_first_row(self):
		p = self.pclass()
		feed_input(p,0,4,    "+---+\n")
		feed_input(p,1,0,"   /-- /\n")
		
	def test_doesnt_assume_h_separator_if_section_too_small(self):
		p = self.pclass()
		feed_input(p,0,6,      "+---+\n")
		feed_input(p,1,0,"     /   /\n")
		feed_input(p,2,0,"    /---/\n")
		feed_input(p,3,0,"   /-- /\n")
		
	def test_allows_multiple_h_separators(self):
		p = self.pclass()
		feed_input(p,0,6,      "+---+\n")
		feed_input(p,1,0,"     /   /\n")
		feed_input(p,2,0,"    /---/\n")
		feed_input(p,3,0,"   /   /\n")
		feed_input(p,4,0,"  /---/\n")

	def test_allows_v_separator(self):
		p = self.pclass()
		feed_input(p,0,4,    "+----+\n")
		feed_input(p,1,0,"   / |  /\n")
		feed_input(p,2,0,"  /  | /\n")
		feed_input(p,3,0," +----/\n")
		
	def test_expects_continuation_of_v_separator(self):
		p = self.pclass()
		feed_input(p,0,4,    "+----+\n")
		feed_input(p,1,0,"   / |  /\n")
		feed_input(p,2,0,"  /  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,5," ",core.M_NONE))
			
	def test_expects_continuation_of_v_separator_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,4,    "+----+\n")
		feed_input(p,1,0,"   / |  /\n")
		feed_input(p,2,0,"  /  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,5,"|",core.M_OCCUPIED))
	
	def test_allows_non_separator_v_line(self):
		p = self.pclass()
		feed_input(p,0,4,    "+-----+\n")
		feed_input(p,1,0,"   /     /\n")
		feed_input(p,2,0,"  /  |  /\n")
		feed_input(p,3,0," /   | /\n")
		feed_input(p,4,0,"+-----+\n")
	
	def test_allows_v_non_separator_start_if_occupied(self):
		p = self.pclass()
		feed_input(p,0,4,    "+----+\n")
		feed_input(p,1,0,"   / ")
		p.test(main.CurrentChar(1,5,"|",core.M_OCCUPIED))
		feed_input(p,1,6," |\n")
	
	def test_allows_multiple_v_separators(self):
		p = self.pclass()
		feed_input(p,0,4,    "+------+\n")
		feed_input(p,1,0,"   / | |  /\n")
		feed_input(p,2,0,"  /  | | /\n")
		feed_input(p,3,0," +------+\n")
	
	def test_doesnt_assume_v_separator_if_first_col(self):
		p = self.pclass()
		feed_input(p,0,4,    "+----+\n")
		feed_input(p,1,0,"   /|   /\n")
		feed_input(p,2,0,"  / |  /\n")
		feed_input(p,3,0," /    /\n")
		
	def test_doesnt_assume_v_separator_if_section_too_small(self):
		p = self.pclass()
		feed_input(p,0,4,    "+------+\n")
		feed_input(p,1,0,"   / ||   /\n")
		feed_input(p,2,0,"  /  ||  /\n")
		feed_input(p,3,0," /   |  /\n")
	
	def test_allows_crossing_separators(self):
		p = self.pclass()
		feed_input(p,0,4,    "+-----+\n")
		feed_input(p,1,0,"   / |   /\n")
		feed_input(p,2,0,"  /-----/\n")
		feed_input(p,3,0," /   | /\n")
		feed_input(p,4,0,"+-----+\n")
		
	def test_expects_line_at_separator_intersection(self):
		p = self.pclass()
		feed_input(p,0,4,    "+----+\n")
		feed_input(p,1,0,"   / |  /\n")
		feed_input(p,2,0,"  /--")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,5,"+",core.M_NONE))
			
	def test_expects_line_at_separator_intersection_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,4,    "+----+\n")
		feed_input(p,1,0,"   / |  /\n")
		feed_input(p,2,0,"  /--")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,5,"-",core.M_OCCUPIED))

	def test_allows_vertical_line_at_separator_intersection(self):
		p = self.pclass()
		feed_input(p,0,4,    "+----+\n")
		feed_input(p,1,0,"   / |  /\n")
		feed_input(p,2,0,"  /--|-/\n")

	def test_allows_single_character_sections(self):
		p = self.pclass()
		feed_input(p,0,6,      "+---------+\n")
		feed_input(p,1,0,"     / | | | | /\n")
		feed_input(p,2,0,"    /---------/\n")
		feed_input(p,3,0,"   / | | | | /\n")
		feed_input(p,4,0,"  /---------/\n")
		feed_input(p,5,0," / | | | | /\n")
		feed_input(p,6,0,"+---------+\n")
	"""
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((5,     "+-----+ \n",),
				 (0,"    /     /  \n",),
				 (0,"   /     /   \n",),
				 (0,"  /     /    \n",),
				 (0," +-----+     \n",),
				 (0,"        ",       ),)
		c = core.M_BOX_START_S | core.M_BOX_START_E | core.M_OCCUPIED
		t = core.M_BOX_START_S | core.M_OCCUPIED
		l = core.M_BOX_START_E | core.M_OCCUPIED
		o = core.M_OCCUPIED
		n = core.M_NONE
		r = core.M_BOX_AFTER_E
		b = core.M_BOX_AFTER_S
		outmeta = (	(          c,t,t,t,t,t,t,r,n,),
					(n,n,n,n,l,n,n,n,n,n,o,r,n,n,),
					(n,n,n,l,n,n,n,n,n,o,r,n,n,n,),
					(n,n,l,n,n,n,n,n,o,r,n,n,n,n,),
					(n,l,o,o,o,o,o,o,r,n,n,n,n,n,),
					(n,b,b,b,b,b,b,b,            ),)
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				m = outmeta[j][i]
				self.assertEquals(m, p.test(main.CurrentChar(j,startcol+i,char,core.M_NONE)))

	def do_render(self,x,y,w,h):
		p = self.pclass()
		feed_input(p,y,x,"+" + "-"*w + "+\n")
		for j in range(h):
			feed_input(p,y+1+j,0," "*(x-1-j) + "/" + " "*w + "/\n")
		feed_input(p,y+h+1,0," "*(x-h-1) + "+" + "-"*w + "+\n")
		feed_input(p,y+h+2,0," "*(x-h-1) + " "*(w+2))
		try:
			p.test(main.CurrentChar(y+h+2,x-h-1+w+2," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_correct_shapes(self):
		r = self.do_render(10,12,6,5)
		self.assertEquals(4,len(r))
		self.assertEquals(4,len(filter(lambda x: isinstance(x,core.Line),r)))
			
	def test_render_coordinates(self):
		r = self.do_render(10,12,6,5)
		ts = self.find_with(r,"a",(10.5,12.5))
		self.assertEquals((17.5,12.5),ts.b)
		bs = self.find_with(r,"a",(4.5,18.5))
		self.assertEquals((11.5,18.5),bs.b)
		rs = self.find_with(r,"a",(17.5,12.5))
		self.assertEquals((11.5,18.5),rs.b)
		ls = self.find_with(r,"b",(4.5,18.5))
		self.assertEquals((10.5,12.5),ls.a)
		
	def test_render_coordinates_position(self):
		r = self.do_render(12,4,6,5)
		ts = self.find_with(r,"a",(12.5,4.5))
		self.assertEquals((19.5,4.5),ts.b)
		bs = self.find_with(r,"a",(6.5,10.5))
		self.assertEquals((13.5,10.5),bs.b)
		rs = self.find_with(r,"a",(19.5,4.5))
		self.assertEquals((13.5,10.5),rs.b)
		ls = self.find_with(r,"b",(6.5,10.5))
		self.assertEquals((12.5,4.5),ls.a)
		
	def test_render_coordinates_size(self):
		r = self.do_render(10,12,8,2)
		ts = self.find_with(r,"a",(10.5,12.5))
		self.assertEquals((19.5,12.5),ts.b)
		bs = self.find_with(r,"a",(7.5,15.5))
		self.assertEquals((16.5,15.5),bs.b)
		rs = self.find_with(r,"a",(19.5,12.5))
		self.assertEquals((16.5,15.5),rs.b)
		ls = self.find_with(r,"b",(7.5,15.5))
		self.assertEquals((10.5,12.5),ls.a)
		
	def test_render_z(self):
		for line in self.do_render(10,12,6,5):
			self.assertEquals(0,line.z)

	def test_render_stroke_colour(self):
		for line in self.do_render(10,12,6,5):
			self.assertEquals(core.C_FOREGROUND,line.stroke)

	def test_render_stroke_alpha(self):
		for line in self.do_render(10,12,6,5):
			self.assertEquals(1.0,line.salpha)

	def test_render_stroke_width(self):
		for line in self.do_render(10,12,6,5):
			self.assertEquals(1,line.w)

	def test_render_stroke_style_solid(self):
		for line in self.do_render(10,12,6,5):
			self.assertEquals(core.STROKE_SOLID,line.stype)


class TestDiamondBoxPattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.DiamondBoxPattern
							
	def test_accepts_box(self):
		p = self.pclass()
		feed_input(p,0,4,    ".    \n")
		feed_input(p,1,0,"  .' '.  \n")
		feed_input(p,2,0," <     > \n")
		feed_input(p,3,0,"  '. .'  \n")
		feed_input(p,4,0,"    '    \n")
		feed_input(p,5,0,"     ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(5,5," ",core.M_NONE))
			
	def test_expects_first_period(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4,"?",core.M_NONE))
			
	def test_expects_first_period_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4,".",core.M_OCCUPIED))
			
	def test_allows_rest_of_top_line(self):
		p = self.pclass()
		feed_input(p,0,4,    ".")
		p.test(main.CurrentChar(0,5,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,6,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,7,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_second_line(self):
		p = self.pclass()
		feed_input(p,0,4,    ". \n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		
	def test_doesnt_necessarily_expect_left_side_period(self):
		p = self.pclass()
		feed_input(p,0,4,     ".  \n")
		feed_input(p,1,0,"  ")
		p.test(main.CurrentChar(1,2,"'",core.M_NONE))
		
	def test_doesnt_necessarily_expect_left_side_period_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,4,    ".  \n")
		feed_input(p,1,0,"  ")
		p.test(main.CurrentChar(1,2,".",core.M_OCCUPIED))
		
	def test_expects_left_side_apos(self):
		p = self.pclass()
		feed_input(p,0,4,    ".  \n")
		feed_input(p,1,0,"  .")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,3,".",core.M_NONE))
	
	def test_expects_left_side_apos_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,4,    ".  \n")
		feed_input(p,1,0,"  .")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,3,"'",core.M_OCCUPIED))
			
	def test_allows_first_content_line(self):
		p = self.pclass()
		feed_input(p,0,4,    ".  \n")
		feed_input(p,1,0,"  .'")
		p.test(main.CurrentChar(1,4,"q",core.M_OCCUPIED))
		
	def test_expects_right_side_apos(self):
		p = self.pclass()
		feed_input(p,0,4,    ".  \n")
		feed_input(p,1,0,"  .' ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,5,".",core.M_NONE))
			
	def test_expects_right_side_apos_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,4,    ".  \n")
		feed_input(p,1,0,"  .' ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,5,"'",core.M_OCCUPIED))
	
	def test_expects_right_side_period(self):
		p = self.pclass()
		feed_input(p,0,4,    ".   \n")
		feed_input(p,1,0,"  .' '")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,6,"'",core.M_NONE))
			
	def test_expects_right_side_period_unnoccupied(self):
		p = self.pclass()
		feed_input(p,0,4,    ".   \n")
		feed_input(p,1,0,"  .' '")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,6,".",core.M_OCCUPIED))
			
	def test_allows_rest_of_second_line(self):
		p = self.pclass()
		feed_input(p,0,4,    ".  \n")
		feed_input(p,1,0,"  .' '.")
		p.test(main.CurrentChar(1,7,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,8,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,9,"\n",core.M_OCCUPIED))

	def test_allows_start_of_third_line(self):
		p = self.pclass()
		feed_input(p,0,5,     ".   \n")
		feed_input(p,1,0,"   .' '. \n")
		p.test(main.CurrentChar(2,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,1,"b",core.M_OCCUPIED))

	def test_expects_left_angle_bracket(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '.\n")
		feed_input(p,2,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"'",core.M_NONE))
			
	def test_expects_left_angle_bracket_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '.\n")
		feed_input(p,2,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"<",core.M_OCCUPIED))
			
	def test_allows_middle_content_line(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '.\n")
		feed_input(p,2,0,"  <")
		p.test(main.CurrentChar(2,3,"v",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,4,"w",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,5,"x",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,6,"y",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,7,"z",core.M_OCCUPIED))
		
	def test_expects_right_angle_bracket(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '. \n")
		feed_input(p,2,0,"  <     ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,8,"'",core.M_NONE))
			
	def test_expects_right_angle_bracket_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '. \n")
		feed_input(p,2,0,"  <     ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,8,">",core.M_OCCUPIED))
			
	def test_allows_rest_of_middle_line(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '.\n")
		feed_input(p,2,0,"  <     >")
		p.test(main.CurrentChar(2,9,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,10,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,11,"\n",core.M_OCCUPIED))

	def test_allows_start_of_next_to_bottom_line(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '.\n")
		feed_input(p,2,0,"  <     >\n")
		p.test(main.CurrentChar(3,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(3,1,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(3,2,"c",core.M_OCCUPIED))

	def test_expects_bottom_left_apos(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '.\n")
		feed_input(p,2,0,"  <     >\n")
		feed_input(p,3,0,"   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,3,".",core.M_NONE))
			
	def test_expects_bottom_left_apos_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '.\n")
		feed_input(p,2,0,"  <     >\n")
		feed_input(p,3,0,"   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,3,"'",core.M_OCCUPIED))

	def test_expects_bottom_left_period(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '.\n")
		feed_input(p,2,0,"  <     >\n")
		feed_input(p,3,0,"   '")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,4,"'",core.M_NONE))

	def test_expects_bottom_left_period_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '.\n")
		feed_input(p,2,0,"  <     >\n")
		feed_input(p,3,0,"   '")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,4,".",core.M_OCCUPIED))

	def test_allows_next_to_bottom_content_line(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '.\n")
		feed_input(p,2,0,"  <     >\n")
		feed_input(p,3,0,"   '.")
		p.test(main.CurrentChar(3,5,"r",core.M_OCCUPIED))
		
	def test_expects_bottom_right_period(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '.\n")
		feed_input(p,2,0,"  <     >\n")
		feed_input(p,3,0,"   '. ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,6,"'",core.M_NONE))

	def test_expects_bottom_right_period_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '.\n")
		feed_input(p,2,0,"  <     >\n")
		feed_input(p,3,0,"   '. ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,6,".",core.M_OCCUPIED))

	def test_expects_bottom_right_apos(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '.\n")
		feed_input(p,2,0,"  <     >\n")
		feed_input(p,3,0,"   '. .")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,7,".",core.M_NONE))
	
	def test_expects_bottom_right_apos_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '.\n")
		feed_input(p,2,0,"  <     >\n")
		feed_input(p,3,0,"   '. .")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,7,"'",core.M_OCCUPIED))
			
	def test_allows_rest_of_next_to_bottom_line(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '.\n")
		feed_input(p,2,0,"  <     >\n")
		feed_input(p,3,0,"   '. .'")
		p.test(main.CurrentChar(3,8,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(3,9,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(3,10,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_bottom_line(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '.\n")
		feed_input(p,2,0,"  <     >\n")
		feed_input(p,3,0,"   '. .' \n")
		p.test(main.CurrentChar(4,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(4,1,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(4,2,"c",core.M_OCCUPIED))
		p.test(main.CurrentChar(4,3,"d",core.M_OCCUPIED))
		p.test(main.CurrentChar(4,4,"e",core.M_OCCUPIED))
		
	def test_expects_bottom_apos(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '.\n")
		feed_input(p,2,0,"  <     >\n")
		feed_input(p,3,0,"   '. .' \n")
		feed_input(p,4,0,"     ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(4,5,".",core.M_NONE))
			
	def test_expects_bottom_apos_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '.\n")
		feed_input(p,2,0,"  <     >\n")
		feed_input(p,3,0,"   '. .' \n")
		feed_input(p,4,0,"     ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(4,5,"'",core.M_OCCUPIED))

	def test_allows_rest_of_bottom_line(self):
		p = self.pclass()
		feed_input(p,0,5,     ".  \n")
		feed_input(p,1,0,"   .' '.\n")
		feed_input(p,2,0,"  <     >\n")
		feed_input(p,3,0,"   '. .' \n")
		feed_input(p,4,0,"     '")
		p.test(main.CurrentChar(4,6,"x",core.M_OCCUPIED))
		p.test(main.CurrentChar(4,7,"y",core.M_OCCUPIED))
		p.test(main.CurrentChar(4,8,"\n",core.M_OCCUPIED))

	def test_allows_missing_final_line(self):
		p = self.pclass()
		feed_input(p,0,5,     ".   \n")
		feed_input(p,1,0,"   .' '. \n")
		feed_input(p,2,0,"  <     >\n")
		feed_input(p,3,0,"   '. .' \n")
		feed_input(p,4,0,"     '   \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(5,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_short_final_line(self):
		p = self.pclass()
		feed_input(p,0,5,     ".   \n")
		feed_input(p,1,0,"   .' '. \n")
		feed_input(p,2,0,"  <     >\n")
		feed_input(p,3,0,"   '. .' \n")
		feed_input(p,4,0,"     '   \n")
		feed_input(p,5,0,"   \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(6,0," ",core.M_NONE))

	def test_allows_larger_size(self):
		p = self.pclass()
		feed_input(p,0,6,      ".      \n")
		feed_input(p,1,0,"    .' '.    \n")
		feed_input(p,2,0,"  .'     '.  \n")
		feed_input(p,3,0," <         > \n")
		feed_input(p,4,0,"  '.     .'  \n")
		feed_input(p,5,0,"    '. .'    \n")
		feed_input(p,6,0,"      '      \n")
		feed_input(p,7,0,"       ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(7,7," ",core.M_NONE))
			
	def test_allows_small_size(self):
		p = self.pclass()
		feed_input(p,0,5,     ".   \n")
		feed_input(p,1,0,"    < >  \n")
		feed_input(p,2,0,"     '   \n")
		feed_input(p,3,0,"      ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,6," ",core.M_NONE))

	def test_allows_to_start_with_apos(self):
		p = self.pclass()
		feed_input(p,0,4,    ".'.   \n")
		feed_input(p,1,0,"  .'   '. \n")
		feed_input(p,2,0," <       >\n")
		feed_input(p,3,0,"  '.   .' \n")
		feed_input(p,4,0,"    '.'   \n")
		feed_input(p,5,0,"      ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(5,7," ",core.M_NONE))
		
	def test_allowed_to_touch_left_edge(self):
		p = self.pclass()
		feed_input(p,0,3,   ".    \n")
		feed_input(p,1,0," .' '.  \n")
		feed_input(p,2,0,"<     > \n")
		feed_input(p,3,0," '. .'  \n")
		feed_input(p,4,0,"   '    \n")

	def test_allows_short_lines(self):
		p = self.pclass()
		feed_input(p,0,7,       ".\n")
		feed_input(p,1,0,"     .' '.\n")
		feed_input(p,2,0,"   .'     '.\n")
		feed_input(p,3,0,"  <         >\n")
		feed_input(p,4,0,"   '.     .'\n")
		feed_input(p,5,0,"     '. .'\n")
		feed_input(p,6,0,"       '\n")
		feed_input(p,7,0,"        ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(7,8," ",core.M_NONE))
		
	def test_allows_short_lines_apos_peak(self):
		p = self.pclass()
		feed_input(p,0,6,      ".'.\n")
		feed_input(p,1,0,"    .'   '.\n")
		feed_input(p,2,0,"  .'       '.\n")
		feed_input(p,3,0," <           >\n")
		feed_input(p,4,0,"  '.       .'\n")
		feed_input(p,5,0,"    '.   .'\n")
		feed_input(p,6,0,"      '.'\n")
		feed_input(p,7,0,"         ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(7,9," ",core.M_NONE))
		
	def test_sets_correct_meta_flags(self):
		input = ((6,      ".      \n"),
				 (0,"    .' '.    \n"),
				 (0,"  .'     '.  \n"),
				 (0," <         > \n"),
				 (0,"  '.     .'  \n"),
				 (0,"    '. .'    \n"),
				 (0,"      '      \n"),
				 (0,"       "        ),)     	
		o = core.M_OCCUPIED
		n = core.M_NONE
		a = core.M_OCCUPIED | core.M_BOX_START_S | core.M_BOX_START_E
		z = core.M_BOX_AFTER_E | core.M_BOX_AFTER_S
		l = core.M_OCCUPIED | core.M_BOX_START_E
		r = core.M_BOX_AFTER_E
		t = core.M_BOX_START_S | core.M_OCCUPIED
		b = core.M_BOX_AFTER_S
		meta = ((            a,r,n,n,n,n,n,n,),
			    (n,n,n,n,a,t,n,t,t,r,n,n,n,n,),
			    (n,n,a,t,n,n,n,n,n,t,t,r,n,n,),
			    (n,a,n,n,n,n,n,n,n,n,n,t,r,n,), # mid
			    (n,b,l,o,n,n,n,n,n,o,o,z,n,n,),
			    (n,n,b,b,l,o,n,o,o,z,b,n,n,n,),
			    (n,n,n,n,b,b,l,z,b,n,n,n,n,n,),
			    (n,n,n,n,n,n,b,              ),)
		p = self.pclass()
		for j,(linestart,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,linestart+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)
				
	def do_render(self,x,y,w):
		p = self.pclass()
		apeak = (w-3)%4 == 2
		h = 3+2*((w-3-2*int(apeak))//4)
		feed_input(p,y,x-int(apeak),".'. \n" if apeak else ". \n")
		for i in range((h-3)//2):
			feed_input(p,y+1+i,0,(x-int(apeak)-2*(i+1))*" " 
				+ ".'" + " "*(i*4+1+2*int(apeak)) + "'. \n")
		feed_input(p,y+(h+1)//2-1,0,(x-(w//2))*" " + "<" + " "*(w-2) + "> \n")
		for i in range(((h-3)//2)-1,-1,-1):
			feed_input(p,y+(h-3)//2+2+((h-3)//2-1-i),0,(x-int(apeak)-2*(i+1))*" "
				+ "'." + " "*(i*4+1+2*int(apeak)) + ".' \n")
		feed_input(p,y+h-1,0," "*(x-int(apeak)) + ("'.' \n" if apeak else "' \n"))
		feed_input(p,y+h,0," "*(x+1+int(apeak)))
		try:
			p.test(main.CurrentChar(y+h,x+1+int(apeak)," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_correct_shapes(self):
		r = self.do_render(10,12,7)
		self.assertEquals(4, len(r))
		self.assertEquals(4, len(filter(lambda x: isinstance(x,core.Line),r)))
		
	def test_render_position(self):
		r = self.do_render(10,12,7)
		nw = self.find_with(r,"b",(7.5,14.5))
		self.assertEquals((10.5,12.5),nw.a)
		ne = self.find_with(r,"b",(13.5,14.5))
		self.assertEquals((10.5,12.5),ne.a)
		sw = self.find_with(r,"a",(7.5,14.5))
		self.assertEquals((10.5,16.5),sw.b)
		se = self.find_with(r,"a",(13.5,14.5))
		self.assertEquals((10.5,16.5),se.b)
		
	def test_render_size(self):
		r = self.do_render(10,12,13)
		nw = self.find_with(r,"b",(4.5,15.5))
		self.assertEquals((10.5,12.5),nw.a)
		ne = self.find_with(r,"b",(16.5,15.5))
		self.assertEquals((10.5,12.5),ne.a)
		sw = self.find_with(r,"a",(4.5,15.5))
		self.assertEquals((10.5,18.5),sw.b)
		se = self.find_with(r,"a",(16.5,15.5))
		self.assertEquals((10.5,18.5),se.b)

	def test_render_z(self):
		for shape in self.do_render(10,12,7):
			self.assertEquals(1, shape.z)
			
	def test_render_stroke(self):
		for shape in self.do_render(10,12,7):
			self.assertEquals(core.C_FOREGROUND,shape.stroke)
			
	def test_render_stroke_alpha(self):
		for shape in self.do_render(10,12,7):
			self.assertEquals(1.0,shape.salpha)
			
	def test_render_stroke_width(self):
		for shape in self.do_render(10,12,7):
			self.assertEquals(1, shape.w)
			
	def test_render_stroke_style_solid(self):
		for shape in self.do_render(10,12,7):
			self.assertEquals(core.STROKE_SOLID,shape.stype)


class TestEllipticalBoxPattern(unittest.TestCase,PatternTests):

	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.EllipticalBoxPattern
		
	def test_accepts_small_ellipse(self):
		p = self.pclass()
		feed_input(p,1,2,  ".-.  \n")
		feed_input(p,2,0," |   | \n")
		feed_input(p,3,0,"  '-'  \n")
		feed_input(p,4,0,"     ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(4,5," ",core.M_NONE))
			
	def test_expects_top_left_period(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,5,"?",core.M_NONE))
			
	def test_expects_top_left_period_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,5,".",core.M_OCCUPIED))

	def test_expects_top_hyphen(self):
		p = self.pclass()
		feed_input(p,1,5,".")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,6,".",core.M_NONE))
			
	def test_expects_top_hyphen_unoccupied(self):
		p = self.pclass()
		feed_input(p,1,5,".")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,6,"-",core.M_OCCUPIED))

	def test_expects_top_right_period(self):
		p = self.pclass()
		feed_input(p,1,5,".-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,7,"?",core.M_NONE))
	
	def test_expects_top_right_period_unoccupied(self):
		p = self.pclass()
		feed_input(p,1,5,".-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,7,".",core.M_OCCUPIED))

	def test_allows_rest_of_top_line(self):
		p = self.pclass()
		feed_input(p,1,5,".-.")
		p.test(main.CurrentChar(1,8,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,9,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,10,"\n",core.M_OCCUPIED))

	def test_allows_start_of_second_line(self):
		p = self.pclass()
		feed_input(p,1,5,".-.  \n")
		p.test(main.CurrentChar(2,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,1,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,2,"c",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,3,"d",core.M_OCCUPIED))

	def test_expects_left_pipe(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.  \n")
		feed_input(p,2,0,"    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4,"?",core.M_NONE))
			
	def test_expects_left_pipe_unoccupied(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.  \n")
		feed_input(p,2,0,"    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4,"|",core.M_OCCUPIED))
			
	def test_allows_middle_content(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.  \n")
		feed_input(p,2,0,"    |")
		p.test(main.CurrentChar(2,5,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,6,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,7,"c",core.M_OCCUPIED))

	def test_rejects_short_content_line(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.  \n")
		feed_input(p,2,0,"    | \n")
		with self.assertRaises(core.PatternRejected):
			feed_input(p,3,0," ")

	def test_expects_right_pipe(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.  \n")
		feed_input(p,2,0,"    |   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,8,"'",core.M_NONE))
			
	def test_expects_right_pipe_unoccupied(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.  \n")
		feed_input(p,2,0,"    |   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,8,"|",core.M_OCCUPIED))
			
	def test_allows_rest_of_third_line(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.  \n")
		feed_input(p,2,0,"    |   |")
		p.test(main.CurrentChar(2,9,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,10,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,11,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_fourth_line(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.  \n")
		feed_input(p,2,0,"    |   | \n")
		p.test(main.CurrentChar(3,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(3,1,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(3,2,"c",core.M_OCCUPIED))
		p.test(main.CurrentChar(3,3,"d",core.M_OCCUPIED))
		p.test(main.CurrentChar(3,4,"e",core.M_OCCUPIED))
		
	def test_expects_bottom_left_apos(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.  \n")
		feed_input(p,2,0,"    |   | \n")
		feed_input(p,3,0,"     ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,5,"Q",core.M_NONE))
			
	def test_expects_bottom_left_apos_unoccupied(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.  \n")
		feed_input(p,2,0,"    |   | \n")
		feed_input(p,3,0,"     ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,5,"'",core.M_OCCUPIED))
			
	def test_expects_bottom_hyphen(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.  \n")
		feed_input(p,2,0,"    |   | \n")
		feed_input(p,3,0,"     '")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,6,"'",core.M_NONE))
			
	def test_expects_bottom_hyphen_unoccupied(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.  \n")
		feed_input(p,2,0,"    |   | \n")
		feed_input(p,3,0,"     '")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,6,"-",core.M_OCCUPIED))
			
	def test_expects_bottom_right_apos(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.  \n")
		feed_input(p,2,0,"    |   | \n")
		feed_input(p,3,0,"     '-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,7,"|",core.M_NONE))
			
	def test_expects_bottom_right_apos_unoccupied(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.  \n")
		feed_input(p,2,0,"    |   | \n")
		feed_input(p,3,0,"     '-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,7,"'",core.M_OCCUPIED))
	
	def test_allows_rest_of_fourth_line(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.  \n")
		feed_input(p,2,0,"    |   | \n")
		feed_input(p,3,0,"     '-'")
		p.test(main.CurrentChar(3,8,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(3,9,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(3,10,"\n",core.M_OCCUPIED))
		
	def test_allows_final_line(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.  \n")
		feed_input(p,2,0,"    |   | \n")
		feed_input(p,3,0,"     '-'  \n")
		p.test(main.CurrentChar(4,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(4,1,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(4,2,"c",core.M_OCCUPIED))
		p.test(main.CurrentChar(4,3,"d",core.M_OCCUPIED))
		p.test(main.CurrentChar(4,4,"e",core.M_OCCUPIED))
		p.test(main.CurrentChar(4,5,"f",core.M_OCCUPIED))
		p.test(main.CurrentChar(4,6,"g",core.M_OCCUPIED))
		p.test(main.CurrentChar(4,7,"h",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(4,8,"i",core.M_OCCUPIED))

	def test_allows_missing_final_line_due_to_eoi(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.  \n")
		feed_input(p,2,0,"    |   | \n")
		feed_input(p,3,0,"     '-'  \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(4,0,core.END_OF_INPUT,core.M_NONE))

	def test_allows_missing_final_line_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.  \n")
		feed_input(p,2,0,"    |   | \n")
		feed_input(p,3,0,"     '-'  \n")
		feed_input(p,4,0,"\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(5,0," ",core.M_NONE))
			
	def test_allows_partial_final_line(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.  \n")
		feed_input(p,2,0,"    |   | \n")
		feed_input(p,3,0,"     '-'  \n")
		feed_input(p,4,0,"      \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(5,0," ",core.M_NONE))

	def test_allows_wide_ellipse(self):
		p = self.pclass()
		feed_input(p,1,5,     ".----.  \n")
		feed_input(p,2,0,"    |      | \n")
		feed_input(p,3,0,"     '----'  \n")
		feed_input(p,4,0,"           ")
		with self.assertRaises(StopIteration):
			feed_input(p,4,11," ")
			
	def test_middle_width_must_match_top(self):
		p = self.pclass()
		feed_input(p,1,5,     ".----.  \n")
		feed_input(p,2,0,"    |      ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,11," ",core.M_NONE))

	def test_bottom_width_must_match_top(self):
		p = self.pclass()
		feed_input(p,1,5,     ".----.  \n")
		feed_input(p,2,0,"    |      | \n")
		feed_input(p,3,0,"     '----")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,10,"-",core.M_NONE))

	def test_allows_tall_ellipse(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.  \n")
		feed_input(p,2,0,"    |   | \n")
		feed_input(p,3,0,"    |   | \n")
		feed_input(p,4,0,"    |   | \n")
		feed_input(p,5,0,"     '-'  \n")
		feed_input(p,6,0,"        ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(6,8," ",core.M_NONE))
	
	def test_allows_slash_corners(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.   \n")
		feed_input(p,2,0,"    /   \\  \n")
		feed_input(p,3,0,"   |     | \n")
		feed_input(p,4,0,"    \\   /  \n")
		feed_input(p,5,0,"     '-'   \n")
		feed_input(p,6,0,"        ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(6,8," ",core.M_NONE))
			
	def test_expects_top_left_slash_unoccupied(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.   \n")
		feed_input(p,2,0,"    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4,"/",core.M_OCCUPIED))
		
	def test_expects_top_right_slash(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.   \n")
		feed_input(p,2,0,"    /   ")
		with self.assertRaises(core.PatternRejected):
				p.test(main.CurrentChar(2,8,"|",core.M_NONE))
		
	def test_expects_top_right_slash_unoccupied(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.   \n")
		feed_input(p,2,0,"    /   ")
		with self.assertRaises(core.PatternRejected):
				p.test(main.CurrentChar(2,8,"\\",core.M_OCCUPIED))
		
	def test_doesnt_allow_top_slashes_without_periods(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,5,"/",core.M_NONE))

	def test_expects_bottom_left_slash(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.   \n")
		feed_input(p,2,0,"    /   \\  \n")
		feed_input(p,3,0,"   |     | \n")
		feed_input(p,4,0,"    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(4,4,"'",core.M_NONE))
		
	def test_expecst_bottom_left_slash_unoccupied(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.   \n")
		feed_input(p,2,0,"    /   \\  \n")
		feed_input(p,3,0,"   |     | \n")
		feed_input(p,4,0,"    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(4,4,"\\",core.M_OCCUPIED))
		
	def test_expects_bottom_right_slash(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.   \n")
		feed_input(p,2,0,"    /   \\  \n")
		feed_input(p,3,0,"   |     | \n")
		feed_input(p,4,0,"    \\   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(4,8,"'",core.M_NONE))
	
	def test_expects_bottom_right_slash_unoccupied(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.   \n")
		feed_input(p,2,0,"    /   \\  \n")
		feed_input(p,3,0,"   |     | \n")
		feed_input(p,4,0,"    \\   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(4,8,"/",core.M_OCCUPIED))
		
	def test_doesnt_allow_bottom_slashes_without_apos(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.   \n")
		feed_input(p,2,0,"    /   \\  \n")
		feed_input(p,3,0,"   |     | \n")
		feed_input(p,4,0,"    \\   /  \n")
		feed_input(p,5,0,"     ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(5,5,"-",core.M_NONE))

	def test_allows_multiple_slashes(self):
		p = self.pclass()
		feed_input(p,1,5,      ".-.     \n")
		feed_input(p,2,0, "    /   \\    \n")
		feed_input(p,3,0, "   /     \\   \n")
		feed_input(p,4,0, "  /       \\  \n")
		feed_input(p,5,0, " |         | \n")
		feed_input(p,6,0, "  \\       /  \n")
		feed_input(p,7,0, "   \\     /   \n")
		feed_input(p,8,0, "    \\   /    \n")
		feed_input(p,9,0, "     '-'     \n")
		feed_input(p,10,0,"        ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(10,8," ",core.M_NONE))
		
	def test_expects_matching_top_right_slashes_short(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.     \n")
		feed_input(p,2,0,"    /   \\    \n")
		feed_input(p,3,0,"   /     ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,9,"|",core.M_NONE))
		
	def test_expects_matching_top_right_slashes_long(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.     \n")
		feed_input(p,2,0,"    /   \\    \n")
		feed_input(p,3,0,"   /     \\   \n")
		feed_input(p,4,0,"  |       ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(4,10,"\\",core.M_NONE))
		
	def test_expects_matching_bottom_left_slashes_short(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.     \n")
		feed_input(p,2,0,"    /   \\    \n")
		feed_input(p,3,0,"   /     \\   \n")
		feed_input(p,4,0,"  |       |  \n")
		feed_input(p,5,0,"   \\     /   \n")
		feed_input(p,6,0,"    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(6,4,"'",core.M_NONE))
		
	def test_expects_matching_bottom_left_slashes_long(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.     \n")
		feed_input(p,2,0,"    /   \\    \n")
		feed_input(p,3,0,"   /     \\   \n")
		feed_input(p,4,0,"  |       |  \n")
		feed_input(p,5,0,"   \\     /   \n")
		feed_input(p,6,0,"    \\   /    \n")
		feed_input(p,7,0,"     ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(7,5,"\\",core.M_NONE))
		
	def test_expects_matching_bottom_right_slashes_short(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.     \n")
		feed_input(p,2,0,"    /   \\    \n")
		feed_input(p,3,0,"   /     \\   \n")
		feed_input(p,4,0,"  |       |  \n")
		feed_input(p,5,0,"   \\     /   \n")
		feed_input(p,6,0,"    \\   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(6,8,"'",core.M_NONE))

	def test_expects_matching_bottom_right_slashes_long(self):
		p = self.pclass()
		feed_input(p,1,5,     ".-.     \n")
		feed_input(p,2,0,"    /   \\    \n")
		feed_input(p,3,0,"   /     \\   \n")
		feed_input(p,4,0,"  |       |  \n")
		feed_input(p,5,0,"   \\     /   \n")
		feed_input(p,6,0,"    \\   /    \n")
		feed_input(p,7,0,"     '-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(7,7,"/",core.M_NONE))

	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((4,    ".---.    \n"),
				 (0,"   /     \\   \n"),
				 (0,"  |       |  \n"),
				 (0,"  |       |  \n"),
				 (0,"   \\     /   \n"),
				 (0,"    '---'    \n"),
				 (0,"         "      ),)
		n = core.M_NONE
		o = core.M_OCCUPIED
		t = core.M_BOX_START_S | core.M_OCCUPIED
		a = core.M_BOX_START_S | core.M_BOX_START_E | core.M_OCCUPIED
		l = core.M_BOX_START_E | core.M_OCCUPIED
		r = core.M_BOX_AFTER_E
		b = core.M_BOX_AFTER_S
		z = core.M_BOX_AFTER_E | core.M_BOX_AFTER_S
		meta = ((        a,t,t,t,t,r,n,n,n,n,),
				(n,n,n,a,n,n,n,n,n,t,r,n,n,n,),
				(n,n,a,n,n,n,n,n,n,n,t,r,n,n,),
				(n,n,l,n,n,n,n,n,n,n,o,r,n,n,),
				(n,n,b,l,n,n,n,n,n,o,z,n,n,n,),
				(n,n,n,b,l,o,o,o,o,z,n,n,n,n,),
				(n,n,n,n,b,b,b,b,b           ),)
		for j,(linestart,line) in enumerate(input):
			for i,char in enumerate(line):
				self.assertEquals(meta[j][i], 
					p.test(main.CurrentChar(j,linestart+i,char,core.M_NONE)))
	
	def do_render(self,x,y,w,h):
		p = self.pclass()
		feed_input(p,y,x,"." + "-"*(w-6) + ". \n")
		feed_input(p,y+1,0," "*(x-1) + "/" + " "*(w-4) + "\\ \n")
		for i in range(h-4):
			feed_input(p,y+2+i,0," "*(x-2) + "|" + " "*(w-2) + "| \n")
		feed_input(p,y+(h-2),0," "*(x-1) + "\\" + " "*(w-4) + "/ \n")
		feed_input(p,y+(h-1),0," "*x + "'" + "-"*(w-6) + "' \n")
		feed_input(p,y+h,0," "*x + " "*(w-4))
		try:
			p.test(main.CurrentChar(y+h,x+(w-2)," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_correct_shapes(self):
		r = self.do_render(5,4,7,6)
		self.assertEquals(1,len(r))
		self.assertTrue( isinstance(r[0],core.Ellipse) )
		
	def test_render_coordinates(self):    
		e = self.do_render(5,4,7,6)[0]    
		self.assertEquals((3.5,4.5),e.a)
		self.assertEquals((9.5,9.5),e.b)
		
	def test_render_coordinates_position(self):
		e = self.do_render(11,20,7,6)[0]
		self.assertEquals((9.5,20.5),e.a)
		self.assertEquals((15.5,25.5),e.b)
		
	def test_render_coordinates_width(self):
		e = self.do_render(5,4,10,6)[0]
		self.assertEquals((3.5,4.5),e.a)
		self.assertEquals((12.5,9.5),e.b)
		
	def test_render_coordinates_height(self):
		e = self.do_render(5,4,7,8)[0]
		self.assertEquals((3.5,4.5),e.a)
		self.assertEquals((9.5,11.5),e.b)
		
	def test_render_z(self):
		e = self.do_render(5,4,7,6)[0]
		self.assertEquals(1,e.z)
		
	def test_render_stroke_colour(self):
		e = self.do_render(5,4,7,6)[0]
		self.assertEquals(core.C_FOREGROUND,e.stroke)
		
	def test_render_stroke_alpha(self):
		e = self.do_render(5,4,7,6)[0]
		self.assertEquals(1.0,e.salpha)
		
	def test_render_stroke_width(self):
		e = self.do_render(5,4,7,6)[0]
		self.assertEquals(1,e.w)
		
	def test_render_stroke_style(self):
		e = self.do_render(5,4,7,6)[0]
		self.assertEquals(core.STROKE_SOLID,e.stype)
		
	def test_render_fill_colour(self):
		e = self.do_render(5,4,7,6)[0]
		self.assertEquals(None,e.fill)
		
	def test_render_fill_alpha(self):
		e = self.do_render(5,4,7,6)[0]
		self.assertEquals(1.0,e.falpha)


class TestRoundedRectangularBoxPattern(unittest.TestCase,PatternTests):

	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.RoundedRectangularBoxPattern		

	def test_accepts_box(self):
		p = self.pclass()
		feed_input(p,0,2,  ".-----. \n")
		feed_input(p,1,0,"  |     | \n")
		feed_input(p,2,0,"  |     | \n")
		feed_input(p,3,0,"  '-----' \n")
		feed_input(p,4,0,"         ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,9," ",core.M_NONE))
			
	def test_expects_top_left_period(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"?",core.M_NONE))
			
	def test_expects_top_left_period_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,".",core.M_OCCUPIED))
			
	def test_expects_top_hyphen(self):
		p = self.pclass()
		feed_input(p,0,2,".")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,".",core.M_NONE))
			
	def test_expects_top_hyphen_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,".")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"-",core.M_OCCUPIED))
			
	def test_allows_single_char_width(self):
		p = self.pclass()
		feed_input(p,0,2,".-.")
			
	def test_expects_top_right_period(self):
		p = self.pclass()
		feed_input(p,0,2,".-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"?",core.M_NONE))
			
	def test_expects_top_right_period_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,".-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,".",core.M_OCCUPIED))
			
	def test_allows_long_width(self):
		p = self.pclass()
		feed_input(p,0,2,".-------------.")
	
	def test_allows_rest_of_first_line(self):
		p = self.pclass()
		feed_input(p,0,2,".---.")
		p.test(main.CurrentChar(0,7,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,8,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,9,"\n",core.M_OCCUPIED))
	
	def test_allows_start_of_second_line(self):
		p = self.pclass()
		feed_input(p,0,2,".---.\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		
	def test_expects_left_pipe(self):
		p = self.pclass()
		feed_input(p,0,2,".---.\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"+",core.M_NONE))
			
	def test_expects_left_pipe_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,".---.\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"|",core.M_OCCUPIED))
	
	def test_allows_box_contents(self):
		p = self.pclass()
		feed_input(p,0,2,  ".---.\n")
		feed_input(p,1,0,"  |")
		p.test(main.CurrentChar(1,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,4,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,5,"c",core.M_OCCUPIED))
		
	def test_rejects_short_content_line(self):
		p = self.pclass()
		feed_input(p,0,2,  ".---.\n")
		feed_input(p,1,0,"  |  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,5,"\n",core.M_NONE))
		
	def test_expects_right_pipe(self):
		p = self.pclass()
		feed_input(p,0,2,  ".---.\n")
		feed_input(p,1,0,"  |   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,6,"a",core.M_NONE))
			
	def test_expects_right_pipe_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  ".---.\n")
		feed_input(p,1,0,"  |   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,6,"|",core.M_OCCUPIED))
			
	def test_allows_rest_of_second_line(self):
		p = self.pclass()
		feed_input(p,0,2,  ".---.\n")
		feed_input(p,1,0,"  |   |")
		p.test(main.CurrentChar(1,7,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,8,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,9,"\n",core.M_OCCUPIED))
	
	def test_allows_start_of_bottom_line(self):
		p = self.pclass()
		feed_input(p,0,2,  ".---.\n")
		feed_input(p,1,0,"  |   |\n")
		p.test(main.CurrentChar(2,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,1,"b",core.M_OCCUPIED))
		
	def test_allows_single_char_height(self):
		p = self.pclass()
		feed_input(p,0,2,  ".---.\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  '")
		
	def test_expects_bottom_left_apos(self):
		p = self.pclass()
		feed_input(p,0,2,  ".---.\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"?",core.M_NONE))
	
	def test_expects_bottom_left_apos_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  ".---.\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"'",core.M_OCCUPIED))
			
	def test_allows_long_height(self):
		p = self.pclass()
		feed_input(p,0,2,  ".---.\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  |   |\n")
		feed_input(p,3,0,"  |   |\n")
		feed_input(p,4,0,"  '")
		
	def test_expects_bottom_hyphen(self):
		p = self.pclass()
		feed_input(p,0,2,  ".---.\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  '")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,3,"'",core.M_NONE))
	
	def test_expects_bottom_hyphen_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  ".---.\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  '")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,3,"-",core.M_OCCUPIED))
			
	def test_expects_bottom_right_apos(self):
		p = self.pclass()
		feed_input(p,0,2,  ".---.\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  '---")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,6,"-",core.M_NONE))
			
	def test_expects_bottom_right_apos_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  ".---.\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  '---")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,6,"'",core.M_OCCUPIED))
			
	def test_allows_rest_of_bottom_line(self):
		p = self.pclass()
		feed_input(p,0,2,  ".---.\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  '---'")
		p.test(main.CurrentChar(2,7,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,8,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,9,"\n",core.M_OCCUPIED))
		
	def test_allows_final_line(self):
		p = self.pclass()
		feed_input(p,0,2,  ".---.\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  '---'\n")
		for i in range(7):
			p.test(main.CurrentChar(3,i,"z",core.M_OCCUPIED))
			
	def test_allows_no_final_line(self):
		p = self.pclass()
		feed_input(p,0,2,  ".---.\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  '---'\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_short_final_line(self):
		p = self.pclass()
		feed_input(p,0,2,  ".---.\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  '---'\n")
		feed_input(p,3,0,"    ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,4,"\n",core.M_NONE))

	def test_allowed_to_touch_left_edge(self):
		p = self.pclass()
		feed_input(p,0,0,".---.\n")
		feed_input(p,1,0,"|   |\n")
		feed_input(p,2,0,"'---'\n")
		feed_input(p,3,0,"     ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,5,"\n",core.M_NONE))
			
	def test_allowed_to_touch_bottom_left_corner(self):
		p = self.pclass()
		feed_input(p,0,0,".---.\n")
		feed_input(p,1,0,"|   |\n")
		feed_input(p,2,0,"'---'\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_slash_corners(self):
		p = self.pclass()
		feed_input(p,0,2,  "/--\\ \n")
		feed_input(p,1,0,"  |  | \n")
		feed_input(p,2,0,"  \\--/ \n")
		feed_input(p,3,0,"      ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,6," ",core.M_NONE))
			
	def test_expects_top_right_backslash(self):
		p = self.pclass()
		feed_input(p,0,2,  "/--")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,5,".",core.M_NONE))
			
	def test_expects_top_right_backslash_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "/--")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,5,"\\",core.M_OCCUPIED))
			
	def test_expects_bottom_left_backslash(self):
		p = self.pclass()
		feed_input(p,0,2,  "/--\\ \n")
		feed_input(p,1,0,"  |  | \n")
		feed_input(p,2,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"'",core.M_NONE))
			
	def test_expects_bottom_left_backslash_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "/--\\ \n")
		feed_input(p,1,0,"  |  | \n")
		feed_input(p,2,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"\\",core.M_OCCUPIED))
			
	def test_expects_bottom_right_forwardslash(self):
		p = self.pclass()
		feed_input(p,0,2,  "/--\\ \n")
		feed_input(p,1,0,"  |  | \n")
		feed_input(p,2,0,"  \\--")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,5,"'",core.M_NONE))
			
	def test_expects_bottom_right_forwardslash_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "/--\\ \n")
		feed_input(p,1,0,"  |  | \n")
		feed_input(p,2,0,"  \\--")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,5,"/",core.M_OCCUPIED))
			
	"""	
	def test_allows_h_separator(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |----|\n")
			
	def test_expects_continuation_of_h_separator(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4," ",core.M_NONE))
			
	def test_expects_continuation_of_h_separator_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4,"-",core.M_OCCUPIED))
			
	def test_allows_non_separator_h_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  | ---|\n")
		
	def test_allows_h_non_separator_start_if_occupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |")
		p.test(main.CurrentChar(2,3,"-",core.M_OCCUPIED))
		feed_input(p,2,4,"---|\n")
	
	def test_doesnt_assume_h_separator_if_first_row(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |--- |\n")
		
	def test_doesnt_assume_h_separator_if_section_too_small(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |----|\n")
		feed_input(p,3,0,"  |--  |\n")
		
	def test_allows_multiple_h_separators(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |----|\n")
		feed_input(p,3,0,"  |    |\n")
		feed_input(p,4,0,"  |----|\n")
	
	def test_allows_v_separator(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |  | |\n")
		feed_input(p,3,0,"  +----+\n")
		
	def test_expects_continuation_of_v_separator(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,5," ",core.M_NONE))
			
	def test_expects_continuation_of_v_separator_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,5,"|",core.M_OCCUPIED))
	
	def test_allows_non_separator_v_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |  | |\n")
		feed_input(p,3,0,"  |  | |\n")
		feed_input(p,4,0,"  +----+\n")
	
	def test_allows_v_non_separator_start_if_occupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  ")
		p.test(main.CurrentChar(1,5,"|",core.M_OCCUPIED))
		feed_input(p,1,6," |\n")
	
	def test_allows_multiple_v_separators(self):
		p = self.pclass()
		feed_input(p,0,2,  "+-----+\n")
		feed_input(p,1,0,"  | | | |\n")
		feed_input(p,2,0,"  | | | |\n")
		feed_input(p,3,0,"  +-----+\n")
	
	def test_doesnt_assume_v_separator_if_first_col(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  ||   |\n")
		feed_input(p,2,0,"  ||   |\n")
		feed_input(p,3,0,"  |    |\n")
		
	def test_doesnt_assume_v_separator_if_section_too_small(self):
		p = self.pclass()
		feed_input(p,0,2,  "+-----+\n")
		feed_input(p,1,0,"  |  || |\n")
		feed_input(p,2,0,"  |  || |\n")
		feed_input(p,3,0,"  |  |  |\n")
	
	def test_allows_crossing_separators(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |----|\n")
		feed_input(p,3,0,"  |  | |\n")
		feed_input(p,4,0,"  +----+\n")
		
	def test_expects_line_at_separator_intersection(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |--")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,5,"+",core.M_NONE))
			
	def test_expects_line_at_separator_intersection_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |--")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,5,"-",core.M_OCCUPIED))

	def test_allows_vertical_line_at_separator_intersection(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |--|-|\n")

	def test_allows_single_character_sections(self):
		p = self.pclass()
		feed_input(p,0,2,  "+-----+\n")
		feed_input(p,1,0,"  | | | |\n")
		feed_input(p,2,0,"  |-----|\n")
		feed_input(p,3,0,"  | | | |\n")
		feed_input(p,4,0,"  |-----|\n")
		feed_input(p,5,0,"  | | | |\n")
		feed_input(p,6,0,"  +-----+\n")
	"""
	def test_allows_dashed_box(self):
		p = self.pclass()
		feed_input(p,0,2,  ".- - - - .\n")
		feed_input(p,1,0,"  ;        ;\n")
		feed_input(p,2,0,"  ;        ;\n")
		feed_input(p,3,0,"  '- - - - '\n")
		feed_input(p,4,0,"            ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(4,12," ",core.M_NONE))
	
	def test_expects_top_dash_continuation(self):
		p = self.pclass()
		feed_input(p,0,2,  ".- -")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,6,"-",core.M_NONE))
			
	def test_expects_top_dash_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  ".-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4," ",core.M_OCCUPIED))
	
	def test_top_expects_complete_dashes(self):
		p = self.pclass()
		feed_input(p,0,2,  ".- -")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,6,"+",core.M_NONE))
	
	def test_expects_dashed_left_side(self):
		p = self.pclass()
		feed_input(p,0,2,  ".- - .\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"|",core.M_NONE))
	
	def test_expects_dashed_left_side_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,   ".- - .\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,";",core.M_OCCUPIED))
	
	def test_expects_dashed_right_side(self):
		p = self.pclass()
		feed_input(p,0,2,  ".- - .\n")
		feed_input(p,1,0,"  ;    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,7,"|",core.M_NONE))
			
	def test_expects_dashed_right_side_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  ".- - .\n")
		feed_input(p,1,0,"  ;    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,7,";",core.M_OCCUPIED))
			
	def test_expects_dashed_left_side_second_line(self):
		p = self.pclass()
		feed_input(p,0,2,  ".- - .\n")
		feed_input(p,1,0,"  ;    ;\n")
		feed_input(p,2,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"|",core.M_NONE))
			
	def test_expects_dashed_left_side_second_line_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  ".- - .\n")
		feed_input(p,1,0,"  ;    ;\n")
		feed_input(p,2,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,";",core.M_OCCUPIED))
			
	def test_expects_dashed_right_side_second_line(self):
		p = self.pclass()
		feed_input(p,0,2,  ".- - .\n")
		feed_input(p,1,0,"  ;    ;\n")
		feed_input(p,2,0,"  ;    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,7,"|",core.M_NONE))
		
	def test_expects_dashed_right_side_second_line_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  ".- - .\n")
		feed_input(p,1,0,"  ;    ;\n")
		feed_input(p,2,0,"  ;    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,7,";",core.M_OCCUPIED))
			
	def test_expects_dashed_bottom_line(self):
		p = self.pclass()
		feed_input(p,0,2,  ".- - .\n")
		feed_input(p,1,0,"  ;    ;\n")
		feed_input(p,2,0,"  '-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4,"-",core.M_NONE))
	
	def test_expects_dashed_bottom_line_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  ".- - .\n")
		feed_input(p,1,0,"  ;    ;\n")
		feed_input(p,2,0,"  '-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4," ",core.M_OCCUPIED))
	
	def test_expects_dashed_bottom_line_continuation(self):
		p = self.pclass()
		feed_input(p,0,2,  ".- - - - .\n")
		feed_input(p,1,0,"  ;        ;\n")
		feed_input(p,2,0,"  '- -")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,6,"-",core.M_NONE))
			
	def test_expects_dashed_bottom_line_continuation_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  ".- - - - .\n")
		feed_input(p,1,0,"  ;        ;\n")
		feed_input(p,2,0,"  '- -")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,6," ",core.M_OCCUPIED))
	"""	
	def test_dashed_box_allows_separators(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - - - - - +\n")
		feed_input(p,1,0,"  ;   |    |   ;\n")
		feed_input(p,2,0,"  ;--------|---;\n")
		feed_input(p,3,0,"  ;   |    |   ;\n")
		feed_input(p,4,0,"  +- - - - - - +\n")
	"""
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		#input = ((2,  "+---+  \n",),
		#		 (0,"  |+|||  \n",),
		#		 (0,"  |---|  \n",),
		#		 (0,"  |-| |  \n",),
		#		 (0,"  +---+  \n",),
		#		 (0,"       ",    ),)
		input = ((2,  ".---.  \n",),
				 (0,"  |   |  \n",),
				 (0,"  |   |  \n",),
				 (0,"  |   |  \n",),
				 (0,"  '---'  \n",),
				 (0,"       ",    ),)
		c = core.M_BOX_START_S | core.M_BOX_START_E | core.M_OCCUPIED
		t = core.M_BOX_START_S | core.M_OCCUPIED
		l = core.M_BOX_START_E | core.M_OCCUPIED
		o = core.M_OCCUPIED
		n = core.M_NONE
		r = core.M_BOX_AFTER_E
		b = core.M_BOX_AFTER_S
		#outmeta = ((    c,t,t,t,t,r,n,n,),
		#		   (n,n,l,n,o,n,o,r,n,n,),
		#		   (n,n,l,o,o,o,o,r,n,n,),
		#		   (n,n,l,n,o,n,o,r,n,n,),
		#		   (n,n,l,o,o,o,o,r,n,n,),
		#		   (n,n,b,b,b,b,b,      ),)
		outmeta = ((    c,t,t,t,t,r,n,n,),
				   (n,n,l,n,n,n,o,r,n,n,),
				   (n,n,l,n,n,n,o,r,n,n,),
				   (n,n,l,n,n,n,o,r,n,n,),
				   (n,n,l,o,o,o,o,r,n,n,),
				   (n,n,b,b,b,b,b,      ),)
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				m = outmeta[j][i]
				self.assertEquals(m, p.test(main.CurrentChar(j,startcol+i,char,core.M_NONE)))
		 
	def do_render(self,x,y,w,h,hs=[],vs=[],dash=False):
		p = self.pclass()
		feed_input(p,y,x,"." + (("- "*(w//2)) if dash else ("-"*w)) + ".\n")
		for i in range(h):
			feed_input(p,y+1+i,0," "*x + (";" if dash else "|"))
			for n in range(w):
				chr = { 
					(True,True): "-",
				  	(True,False): "-",
				  	(False,True): "|",
				  	(False,False): " " 
				}[(i in hs,n in vs)]
				feed_input(p,y+1+i,x+1+n, chr)
			feed_input(p,y+1+i,x+1+w, (";" if dash else "|")+"\n")
		feed_input(p,y+1+h+0,0," "*x + "'" + (("- "*(w//2)) if dash else ("-"*w)) + "'\n")
		feed_input(p,y+1+h+1,0," "*x + " " + " "*w + " ")
		try:
			p.test(main.CurrentChar(y+h+2,x+w+2," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
	
	def test_render_returns_correct_shapes(self):
		r = self.do_render(2,3,5,6)
		self.assertEquals(8, len(r))
		self.assertEquals(4, len(filter(lambda x: isinstance(x,core.Line),r)))
		self.assertEquals(4, len(filter(lambda x: isinstance(x,core.Arc),r)))
		
	def test_render_coordinates(self):
		r = self.do_render(2,3,5,6)
		lines = self.find_type(r,core.Line)
		curves = self.find_type(r,core.Arc)
		                                          
		lt = self.find_with(lines,"a",(3.5,3.5))
		self.assertEquals((7.5,3.5),lt.b)   
		lb = self.find_with(lines,"a",(3.5,10.5))
		self.assertEquals((7.5,10.5),lb.b)   
		ll = self.find_with(lines,"a",(2.5,4.0)) 
		self.assertEquals((2.5,10.0),ll.b) 
		lr = self.find_with(lines,"a",(8.5,4.0))
		self.assertEquals((8.5,10.0),lr.b)
		
		ctl = self.find_with(curves,"a",(2.5,3.5))
		self.assertEquals((4.5,4.5),ctl.b)
		self.assertEquals(math.pi,ctl.start)
		self.assertEquals(math.pi*1.5,ctl.end)
		ctr = self.find_with(curves,"a",(6.5,3.5))
		self.assertEquals((8.5,4.5),ctr.b)
		self.assertEquals(math.pi*-0.5,ctr.start)
		self.assertEquals(0,ctr.end)
		cbl = self.find_with(curves,"a",(2.5,9.5))
		self.assertEquals((4.5,10.5),cbl.b)
		self.assertEquals(math.pi*0.5,cbl.start)
		self.assertEquals(math.pi,cbl.end)
		cbr = self.find_with(curves,"a",(6.5,9.5))
		self.assertEquals((8.5,10.5),cbr.b)
		self.assertEquals(0,cbr.start)
		self.assertEquals(math.pi*0.5,cbr.end)

	def test_render_coordinates_width(self):
		r = self.do_render(2,3,7,6)
		lines = self.find_type(r,core.Line)
		curves = self.find_type(r,core.Arc)
		                                          
		lt = self.find_with(lines,"a",(3.5,3.5))
		self.assertEquals((9.5,3.5),lt.b)   
		lb = self.find_with(lines,"a",(3.5,10.5))
		self.assertEquals((9.5,10.5),lb.b)   
		ll = self.find_with(lines,"a",(2.5,4.0)) 
		self.assertEquals((2.5,10.0),ll.b) 
		lr = self.find_with(lines,"a",(10.5,4.0))
		self.assertEquals((10.5,10.0),lr.b)
		
		ctl = self.find_with(curves,"a",(2.5,3.5))
		self.assertEquals((4.5,4.5),ctl.b)
		self.assertEquals(math.pi,ctl.start)
		self.assertEquals(math.pi*1.5,ctl.end)
		ctr = self.find_with(curves,"a",(8.5,3.5))
		self.assertEquals((10.5,4.5),ctr.b)
		self.assertEquals(math.pi*-0.5,ctr.start)
		self.assertEquals(0,ctr.end)
		cbl = self.find_with(curves,"a",(2.5,9.5))
		self.assertEquals((4.5,10.5),cbl.b)
		self.assertEquals(math.pi*0.5,cbl.start)
		self.assertEquals(math.pi,cbl.end)
		cbr = self.find_with(curves,"a",(8.5,9.5))
		self.assertEquals((10.5,10.5),cbr.b)
		self.assertEquals(0,cbr.start)
		self.assertEquals(math.pi*0.5,cbr.end)
	
	def test_render_coordinates_height(self):
		r = self.do_render(2,3,5,8)
		lines = self.find_type(r,core.Line)
		curves = self.find_type(r,core.Arc)
		                                          
		lt = self.find_with(lines,"a",(3.5,3.5))
		self.assertEquals((7.5,3.5),lt.b)   
		lb = self.find_with(lines,"a",(3.5,12.5))
		self.assertEquals((7.5,12.5),lb.b)   
		ll = self.find_with(lines,"a",(2.5,4.0)) 
		self.assertEquals((2.5,12.0),ll.b) 
		lr = self.find_with(lines,"a",(8.5,4.0))
		self.assertEquals((8.5,12.0),lr.b)
		
		ctl = self.find_with(curves,"a",(2.5,3.5))
		self.assertEquals((4.5,4.5),ctl.b)
		self.assertEquals(math.pi,ctl.start)
		self.assertEquals(math.pi*1.5,ctl.end)
		ctr = self.find_with(curves,"a",(6.5,3.5))
		self.assertEquals((8.5,4.5),ctr.b)
		self.assertEquals(math.pi*-0.5,ctr.start)
		self.assertEquals(0,ctr.end)
		cbl = self.find_with(curves,"a",(2.5,11.5))
		self.assertEquals((4.5,12.5),cbl.b)
		self.assertEquals(math.pi*0.5,cbl.start)
		self.assertEquals(math.pi,cbl.end)
		cbr = self.find_with(curves,"a",(6.5,11.5))
		self.assertEquals((8.5,12.5),cbr.b)
		self.assertEquals(0,cbr.start)
		self.assertEquals(math.pi*0.5,cbr.end)
		
	def test_render_coordinates_position(self):
		r = self.do_render(7,5,5,6)
		lines = self.find_type(r,core.Line)
		curves = self.find_type(r,core.Arc)
		                                          
		lt = self.find_with(lines,"a",(8.5,5.5))
		self.assertEquals((12.5,5.5),lt.b)   
		lb = self.find_with(lines,"a",(8.5,12.5))
		self.assertEquals((12.5,12.5),lb.b)   
		ll = self.find_with(lines,"a",(7.5,6.0)) 
		self.assertEquals((7.5,12.0),ll.b) 
		lr = self.find_with(lines,"a",(13.5,6.0))
		self.assertEquals((13.5,12.0),lr.b)
		
		ctl = self.find_with(curves,"a",(7.5,5.5))
		self.assertEquals((9.5,6.5),ctl.b)
		self.assertEquals(math.pi,ctl.start)
		self.assertEquals(math.pi*1.5,ctl.end)
		ctr = self.find_with(curves,"a",(11.5,5.5))
		self.assertEquals((13.5,6.5),ctr.b)
		self.assertEquals(math.pi*-0.5,ctr.start)
		self.assertEquals(0,ctr.end)
		cbl = self.find_with(curves,"a",(7.5,11.5))
		self.assertEquals((9.5,12.5),cbl.b)
		self.assertEquals(math.pi*0.5,cbl.start)
		self.assertEquals(math.pi,cbl.end)
		cbr = self.find_with(curves,"a",(11.5,11.5))
		self.assertEquals((13.5,12.5),cbr.b)
		self.assertEquals(0,cbr.start)
		self.assertEquals(math.pi*0.5,cbr.end)
		
	def test_render_z(self):
		for shape in self.do_render(2,3,5,6):
			self.assertEquals(0,shape.z)
		
	def test_render_stroke_colour(self):
		for shape in self.do_render(2,3,5,6):
			self.assertEquals(core.C_FOREGROUND,shape.stroke)
		
	def test_render_stroke_alpha(self):
		for shape in self.do_render(2,3,5,6):
			self.assertEquals(1.0, shape.salpha)
		
	def test_render_stroke_width(self):
		for shape in self.do_render(2,3,5,6):
			self.assertEquals(1,shape.w)
		
	def test_render_stroke_style_solid(self):
		for shape in self.do_render(2,3,6,6,dash=False):
			self.assertEquals(core.STROKE_SOLID,shape.stype)
		
	def test_render_stroke_style_dashed(self):
		for shape in self.do_render(2,3,6,6,dash=True):
			self.assertEquals(core.STROKE_DASHED,shape.stype)
		
	def test_render_fill_colour(self):
		for shape in self.find_type(self.do_render(2,3,5,6),core.Arc):
			self.assertEquals(None,shape.fill)
			
	def test_render_fill_alpha(self):
		for shape in self.find_type(self.do_render(2,3,5,6),core.Arc):
			self.assertEquals(1.0,shape.falpha)
			
	"""	
	def test_render_h_sections_returns_background_shapes(self):
		r = self.do_render(3,2,12,4,[],[4,8])
		self.assertEquals(4,len(self.find_type(r,core.Rectangle)))
			
	def test_render_h_sections_coordinates(self):
		r = self.do_render(3,2,12,4,[],[4,8])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(b1.a,(3.5,2.5))
		b2 = self.find_with(r,"b",(12.5,7.5))
		self.assertEquals(b2.a,(8.5,2.5))
		b3 = self.find_with(r,"a",(12.5,2.5))
		self.assertEquals(b3.b,(16.5,7.5))
		
	def test_render_h_sections_stroke_colour(self):
		r = self.do_render(3,2,12,4,[],[4,8])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(None,b1.stroke)
		b2 = self.find_with(r,"b",(12.5,7.5))
		self.assertEquals(None,b2.stroke)
		b3 = self.find_with(r,"a",(12.5,2.5))
		self.assertEquals(None,b3.stroke)
		
	def test_render_h_sections_fill_colour(self):
		r = self.do_render(3,2,12,4,[],[4,8])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(core.C_FOREGROUND,b1.fill)
		b2 = self.find_with(r,"b",(12.5,7.5))
		self.assertEquals(core.C_FOREGROUND,b2.fill)
		b3 = self.find_with(r,"a",(12.5,2.5))
		self.assertEquals(core.C_FOREGROUND,b3.fill)
		
	def test_render_h_sections_fill_alpha(self):
		r = self.do_render(3,2,12,4,[],[4,8])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(0.25,b1.falpha)
		b2 = self.find_with(r,"b",(12.5,7.5))
		self.assertEquals(0.0,b2.falpha)
		b3 = self.find_with(r,"a",(12.5,2.5))
		self.assertEquals(0.25,b3.falpha)
		
	def test_render_h_sections_z(self):
		r = self.do_render(3,2,12,4,[],[4,8])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(-0.5,b1.z)
		b2 = self.find_with(r,"b",(12.5,7.5))
		self.assertEquals(-0.5,b2.z)
		b3 = self.find_with(r,"a",(12.5,2.5))
		self.assertEquals(-0.5,b3.z)
	
	def test_render_v_sections_returns_correct_shapes(self):
		r = self.do_render(3,2,4,12,[4,8],[])
		self.assertEquals(4,len(self.find_type(r,core.Rectangle)))
		
	def test_render_v_sections_coordinates(self):
		r = self.do_render(3,2,4,12,[4,8],[])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(b1.a,(3.5,2.5))
		b2 = self.find_with(r,"b",(8.5,11.5))
		self.assertEquals(b2.a,(3.5,7.5))
		b3 = self.find_with(r,"a",(3.5,11.5))
		self.assertEquals(b3.b,(8.5,15.5))
		
	def test_render_v_sections_stroke_colour(self):
		r = self.do_render(3,2,4,12,[4,8],[])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(b1.stroke,None)
		b2 = self.find_with(r,"b",(8.5,11.5))
		self.assertEquals(b2.stroke,None)
		b3 = self.find_with(r,"a",(3.5,11.5))
		self.assertEquals(b3.stroke,None)
		
	def test_render_v_sections_fill_colour(self):
		r = self.do_render(3,2,4,12,[4,8],[])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(b1.fill,core.C_FOREGROUND)
		b2 = self.find_with(r,"b",(8.5,11.5))
		self.assertEquals(b2.fill,core.C_FOREGROUND)
		b3 = self.find_with(r,"a",(3.5,11.5))
		self.assertEquals(b3.fill,core.C_FOREGROUND)
			
	def test_render_v_sections_fill_alpha(self):
		r = self.do_render(3,2,4,12,[4,8],[])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(b1.falpha,0.25)
		b2 = self.find_with(r,"b",(8.5,11.5))
		self.assertEquals(b2.falpha,0.0)
		b3 = self.find_with(r,"a",(3.5,11.5))
		self.assertEquals(b3.falpha,0.25)
		
	def test_render_v_sections_z(self):
		r = self.do_render(3,2,4,12,[4,8],[])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(-0.5,b1.z)
		b2 = self.find_with(r,"b",(8.5,11.5))
		self.assertEquals(-0.5,b2.z)
		b3 = self.find_with(r,"a",(3.5,11.5))
		self.assertEquals(-0.5,b3.z)
			
	def test_render_hv_sections_returns_correct_shapes(self):
		r = self.do_render(3,2,12,13,[4,8],[4,8])
		self.assertEquals(10,len(self.find_type(r,core.Rectangle)))
		
	def test_render_hv_sections_coordinates(self):
		r = self.do_render(3,2,12,13,[4,8],[4,8])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(b1.a,(3.5,2.5))
		b2 = self.find_with(r,"b",(8.5,11.5))
		self.assertEquals(b2.a,(3.5,7.5))
		b3 = self.find_with(r,"a",(3.5,11.5))
		self.assertEquals(b3.b,(8.5,16.5))
		b4 = self.find_with(r,"b",(12.5,7.5))
		self.assertEquals(b4.a,(8.5,2.5))
		b5 = self.find_with(r,"b",(12.5,11.5))
		self.assertEquals(b5.a,(8.5,7.5))
		b6 = self.find_with(r,"a",(8.5,11.5))
		self.assertEquals(b6.b,(12.5,16.5))		
		b7 = self.find_with(r,"b",(16.5,7.5))
		self.assertEquals(b7.a,(12.5,2.5))
		b8 = self.find_with(r,"b",(16.5,11.5))
		self.assertEquals(b8.a,(12.5,7.5))
		b9 = self.find_with(r,"a",(12.5,11.5))
		self.assertEquals(b9.b,(16.5,16.5))
			
	def test_render_hv_sections_stroke_colour(self):
		r = self.do_render(3,2,12,13,[4,8],[4,8])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(None,b1.stroke)
		b2 = self.find_with(r,"b",(8.5,11.5))
		self.assertEquals(None,b2.stroke)
		b3 = self.find_with(r,"a",(3.5,11.5))
		self.assertEquals(None,b3.stroke)
		b4 = self.find_with(r,"b",(12.5,7.5))
		self.assertEquals(None,b4.stroke)
		b5 = self.find_with(r,"b",(12.5,11.5))
		self.assertEquals(None,b5.stroke)
		b6 = self.find_with(r,"a",(8.5,11.5))
		self.assertEquals(None,b6.stroke)		
		b7 = self.find_with(r,"b",(16.5,7.5))
		self.assertEquals(None,b7.stroke)
		b8 = self.find_with(r,"b",(16.5,11.5))
		self.assertEquals(None,b8.stroke)
		b9 = self.find_with(r,"a",(12.5,11.5))
		self.assertEquals(None,b9.stroke)
			
	def test_render_hv_sections_fill_colour(self):
		r = self.do_render(3,2,12,13,[4,8],[4,8])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(core.C_FOREGROUND,b1.fill)
		b2 = self.find_with(r,"b",(8.5,11.5))
		self.assertEquals(core.C_FOREGROUND,b2.fill)
		b3 = self.find_with(r,"a",(3.5,11.5))
		self.assertEquals(core.C_FOREGROUND,b3.fill)
		b4 = self.find_with(r,"b",(12.5,7.5))
		self.assertEquals(core.C_FOREGROUND,b4.fill)
		b5 = self.find_with(r,"b",(12.5,11.5))
		self.assertEquals(core.C_FOREGROUND,b5.fill)
		b6 = self.find_with(r,"a",(8.5,11.5))
		self.assertEquals(core.C_FOREGROUND,b6.fill)		
		b7 = self.find_with(r,"b",(16.5,7.5))
		self.assertEquals(core.C_FOREGROUND,b7.fill)
		b8 = self.find_with(r,"b",(16.5,11.5))
		self.assertEquals(core.C_FOREGROUND,b8.fill)
		b9 = self.find_with(r,"a",(12.5,11.5))
		self.assertEquals(core.C_FOREGROUND,b9.fill)
			
	def test_render_hv_sections_fill_alpha(self):
		r = self.do_render(3,2,12,13,[4,8],[4,8])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(0.25,b1.falpha)
		b2 = self.find_with(r,"b",(8.5,11.5))
		self.assertEquals(0.125,b2.falpha)
		b3 = self.find_with(r,"a",(3.5,11.5))
		self.assertEquals(0.25,b3.falpha)
		b4 = self.find_with(r,"b",(12.5,7.5))
		self.assertEquals(0.125,b4.falpha)
		b5 = self.find_with(r,"b",(12.5,11.5))
		self.assertEquals(0.0,b5.falpha)
		b6 = self.find_with(r,"a",(8.5,11.5))
		self.assertEquals(0.125,b6.falpha)		
		b7 = self.find_with(r,"b",(16.5,7.5))
		self.assertEquals(0.25,b7.falpha)
		b8 = self.find_with(r,"b",(16.5,11.5))
		self.assertEquals(0.125,b8.falpha)
		b9 = self.find_with(r,"a",(12.5,11.5))
		self.assertEquals(0.25,b9.falpha)
		
	def test_render_hv_sections_z(self):
		r = self.do_render(3,2,12,13,[4,8],[4,8])
		b1 = self.find_with(r,"b",(8.5,7.5))
		self.assertEquals(-0.5,b1.z)
		b2 = self.find_with(r,"b",(8.5,11.5))
		self.assertEquals(-0.5,b2.z)
		b3 = self.find_with(r,"a",(3.5,11.5))
		self.assertEquals(-0.5,b3.z)
		b4 = self.find_with(r,"b",(12.5,7.5))
		self.assertEquals(-0.5,b4.z)
		b5 = self.find_with(r,"b",(12.5,11.5))
		self.assertEquals(-0.5,b5.z)
		b6 = self.find_with(r,"a",(8.5,11.5))
		self.assertEquals(-0.5,b6.z)		
		b7 = self.find_with(r,"b",(16.5,7.5))
		self.assertEquals(-0.5,b7.z)
		b8 = self.find_with(r,"b",(16.5,11.5))
		self.assertEquals(-0.5,b8.z)
		b9 = self.find_with(r,"a",(12.5,11.5))
		self.assertEquals(-0.5,b9.z)	
	"""
	
if __name__ == "__main__":
	unittest.main()
