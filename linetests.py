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


class TestShortUpDiagLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.ShortUpDiagLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,2,  " /  \n")
		feed_input(p,1,0,"   ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_allows_occupied_left_context(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2," ",core.M_OCCUPIED))
		
	def test_rejects_alpha_as_left_context(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"b",core.M_NONE))
			
	def test_rejects_numeric_as_left_context(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"9",core.M_NONE))
		
	def test_expects_forwardslash(self):
		p = self.pclass()
		feed_input(p,0,2," ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
			
	def test_expects_forwardslash_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2," ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"/",core.M_OCCUPIED))

	def test_allows_occupied_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," /")
		p.test(main.CurrentChar(0,4," ",core.M_OCCUPIED))

	def test_rejects_alpha_as_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," /")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"d",core.M_NONE))
			
	def test_rejects_numeric_as_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," /")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"5",core.M_NONE))

	def test_allows_rest_of_first_line(self):
		p = self.pclass()
		feed_input(p,0,2," / ")
		p.test(main.CurrentChar(0,5,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,6,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,7,"\n",core.M_OCCUPIED))

	def test_allows_start_of_second_line(self):
		p = self.pclass()
		feed_input(p,0,3," /  \n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,2,"c",core.M_OCCUPIED))

	def test_allows_no_character_at_end_due_to_eoi(self):
		p = self.pclass()
		feed_input(p,0,3," /  \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,0,core.END_OF_INPUT,core.M_NONE))

	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,3,   " /  \n")
		feed_input(p,1,0,"\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0," ",core.M_NONE))

	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,2,  " /\n")
		feed_input(p,1,0,"  ")
		p.test(main.CurrentChar(1,2,"/",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))

	def test_allows_line_at_left_edge(self):
		p = self.pclass()
		feed_input(p,1,8,"\n")
		feed_input(p,2,0,"/  \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0," ",core.M_NONE))

	def test_allows_line_at_right_edge(self):
		p = self.pclass()
		feed_input(p,1,5,     " /\n")
		feed_input(p,2,0,"      ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,6," ",core.M_NONE))

	def test_allows_line_at_top_left_corner(self):
		p = self.pclass()
		p.test(main.CurrentChar(-1,0,core.START_OF_INPUT,core.M_NONE))
		feed_input(p,0,0,"/  \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,0," ",core.M_NONE))
			
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((4,    " /  \n"),
		         (0,"     "     ),)
		n = core.M_NONE
		s = core.M_OCCUPIED | core.M_LINE_START_SW
		a = core.M_LINE_AFTER_SW
		meta = ((        n,s,n,n,n,),
		        (n,n,n,n,a,        ),)
		for j,(linestart,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,linestart+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)
				
	def do_render(self,x,y):
		p = self.pclass()
		feed_input(p,y,x-1," / \n")
		feed_input(p,y+1,0," "*(x-1))
		try:
			p.test(main.CurrentChar(y+1,x," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_line(self):
		r = self.do_render(4,2)
		self.assertEquals(1,len(r))
		self.assertTrue(isinstance(r[0],core.Line))
	
	def test_render_coordinates(self):
		l = self.do_render(4,2)[0]
		self.assertEquals((5,2),l.a)
		self.assertEquals((4,3),l.b)
		
	def test_render_z(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(core.C_FOREGROUND,l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(core.STROKE_SOLID,l.stype)
		

class TestLongUpDiagLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.LongUpDiagLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,3,   "/\n")
		feed_input(p,1,0,"  / \n")
		feed_input(p,2,0," /  \n")
		feed_input(p,3,0," ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,1," ",core.M_NONE))

	def test_expects_start_forwardslash(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2," ",core.M_NONE))

	def test_expects_start_forwardslash_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"/",core.M_OCCUPIED))
			
	def test_allows_rest_of_start_line(self):
		p = self.pclass()
		feed_input(p,0,2,"/")
		p.test(main.CurrentChar(0,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,4,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,5,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,3,"/\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		
	def test_accepts_rest_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,3,   "/\n")
		feed_input(p,1,0,"  /")
		p.test(main.CurrentChar(1,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,4,"\n",core.M_OCCUPIED))
		
	def test_allows_no_character_at_end_due_to_eoi(self):
		p = self.pclass()
		feed_input(p,0,3,   "/  \n")
		feed_input(p,1,0,"  / \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,4,    "/  \n")
		feed_input(p,1,0,"   /   \n")
		feed_input(p,2,0,"\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0," ",core.M_NONE))
			
	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,3,   "/\n")
		feed_input(p,1,0,"  / \n")
		feed_input(p,2,0," ")
		p.test(main.CurrentChar(2,1,"/",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,2," ",core.M_NONE))
			
	def test_allows_line_to_end_at_left_edge(self):
		p = self.pclass()
		feed_input(p,0,2,  "/\n")
		feed_input(p,1,0," / \n")
		feed_input(p,2,0,"/  \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0," ",core.M_NONE))
			
	def test_allows_line_to_end_at_bottom_left_corner(self):
		p = self.pclass()
		feed_input(p,0,2,  "/\n")
		feed_input(p,1,0," / \n")
		feed_input(p,2,0,"/  \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))

	def test_rejects_length_one_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "/\n")
		feed_input(p,1,0," ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,1," ",core.M_NONE))

	def test_rejects_length_one_line_with_early_end(self):
		p = self.pclass()
		feed_input(p,0,2,  "/\n")
		feed_input(p,1,0,"\n")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,0," ",core.M_NONE))

	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((3,   "/  \n"),
				 (0,"  /   \n"),
				 (0," /    \n"),
				 (0," "       ))
		s = core.M_OCCUPIED|core.M_LINE_START_SW
		o = core.M_OCCUPIED
		n = core.M_NONE
		a = core.M_LINE_AFTER_SW
		meta =  ((      s,n,n,n,),
				 (n,n,o,n,n,n,n,),
				 (n,o,n,n,n,n,n,),
				 (a,            )) 
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,startcol+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)
				
	def do_render(self,x,y,l):
		p = self.pclass()
		for i in range(l):
			feed_input(p,y+i,x-i,"/\n")
			feed_input(p,y+i+1,0," "*(x-1-i))			
		feed_input(p,y+l,x-l," ")
		try:
			p.test(main.CurrentChar(y+l,x-l+1," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_line(self):
		r = self.do_render(4,2,2)
		self.assertEquals(1,len(r))
		self.assertTrue(isinstance(r[0],core.Line))
	
	def test_render_coordinates(self):
		l = self.do_render(4,2,2)[0]
		self.assertEquals((5,2),l.a)
		self.assertEquals((3,4),l.b)
		
	def test_render_coordinates_longer(self):
		l = self.do_render(5,1,3)[0]
		self.assertEquals((6,1),l.a)
		self.assertEquals((3,4),l.b)
	
	def test_render_z(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.C_FOREGROUND,l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.STROKE_SOLID,l.stype)
	
	
class TestShortDownDiagLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.ShortDownDiagLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,2,  " \\  \n")
		feed_input(p,1,0,"     ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,5," ",core.M_NONE))
			
	def test_allows_occupied_left_context(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2," ",core.M_OCCUPIED))
		
	def test_rejects_alpha_as_left_context(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"b",core.M_NONE))
			
	def test_rejects_numeric_as_left_context(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"9",core.M_NONE))
		
	def test_expects_backslash(self):
		p = self.pclass()
		feed_input(p,0,2," ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
			
	def test_expects_backslash_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2," ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"\\",core.M_OCCUPIED))

	def test_allows_occupied_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," \\")
		p.test(main.CurrentChar(0,4," ",core.M_OCCUPIED))

	def test_rejects_alpha_as_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," \\")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"d",core.M_NONE))
			
	def test_rejects_numeric_as_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," \\")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"5",core.M_NONE))

	def test_allows_rest_of_first_line(self):
		p = self.pclass()
		feed_input(p,0,2," \\ ")
		p.test(main.CurrentChar(0,5,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,6,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,7,"\n",core.M_OCCUPIED))

	def test_allows_start_of_second_line(self):
		p = self.pclass()
		feed_input(p,0,3," \\  \n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,2,"c",core.M_OCCUPIED))

	def test_allows_no_character_at_end_due_to_eoi(self):
		p = self.pclass()
		feed_input(p,0,3," \\  \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,0,core.END_OF_INPUT,core.M_NONE))

	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,3,   " \\  \n")
		feed_input(p,1,0,"\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0," ",core.M_NONE))

	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,2,  " \\  \n")
		feed_input(p,1,0,"    ")
		p.test(main.CurrentChar(1,4,"\\",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,5," ",core.M_NONE))

	def test_allows_line_at_left_edge(self):
		p = self.pclass()
		feed_input(p,1,8,"\n")
		feed_input(p,2,0,"\\  \n")
		feed_input(p,3,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,2," ",core.M_NONE))

	def test_allows_line_at_right_edge(self):
		p = self.pclass()
		feed_input(p,1,5,     " \\\n")
		feed_input(p,2,0,"       \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0," ",core.M_NONE))

	def test_allows_line_at_top_left_corner(self):
		p = self.pclass()
		p.test(main.CurrentChar(-1,0,core.START_OF_INPUT,core.M_NONE))
		feed_input(p,0,0,"\\  \n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2," ",core.M_NONE))
			
	def test_allows_bottom_right_corner(self):
		p = self.pclass()
		feed_input(p,2,2," \\  \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((4,    " \\  \n"),
		         (0,"       "    ),)
		n = core.M_NONE
		s = core.M_OCCUPIED | core.M_LINE_START_SE
		a = core.M_LINE_AFTER_SE
		meta = ((        n,s,n,n,n,),
		        (n,n,n,n,n,n,a,    ),)
		for j,(linestart,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,linestart+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)
				
	def do_render(self,x,y):
		p = self.pclass()
		feed_input(p,y,x-1," \\ \n")
		feed_input(p,y+1,0," "*(x+2))
		try:
			p.test(main.CurrentChar(y+1,x+2," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_line(self):
		r = self.do_render(4,2)
		self.assertEquals(1,len(r))
		self.assertTrue(isinstance(r[0],core.Line))
	
	def test_render_coordinates(self):
		l = self.do_render(4,2)[0]
		self.assertEquals((4,2),l.a)
		self.assertEquals((5,3),l.b)
		
	def test_render_z(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(core.C_FOREGROUND,l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(core.STROKE_SOLID,l.stype)	
	

class TestLongDownDiagLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.LongDownDiagLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "\\   \n")
		feed_input(p,1,0,"   \\  \n")
		feed_input(p,2,0,"    \\ \n")
		feed_input(p,3,0,"      ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,6," ",core.M_NONE))
			
	def test_expects_start_backslash(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
			
	def test_expects_start_backslash_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"\\",core.M_OCCUPIED))
			
	def test_allows_rest_of_start_line(self):
		p = self.pclass()
		feed_input(p,0,3,"\\")
		p.test(main.CurrentChar(0,4,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,5,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,6,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,2,"\\\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,2,"c",core.M_OCCUPIED))
		
	def test_rejects_length_one_line(self):
		p = self.pclass()
		feed_input(p,0,3,   "\\\n")
		feed_input(p,1,0,"    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,4," ",core.M_NONE))
	
	def test_rejects_length_one_line_with_early_end(self):
		p = self.pclass()
		feed_input(p,0,3,   "\\\n")
		feed_input(p,1,0,"\n")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,0," ",core.M_NONE))
	
	def test_accepts_rest_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,3,   "\\\n")
		feed_input(p,1,0,"    \\")
		p.test(main.CurrentChar(1,5,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,6,"\n",core.M_OCCUPIED))
		
	def test_allows_no_character_at_end_due_to_eoi(self):
		p = self.pclass()
		feed_input(p,0,3,   "\\  \n")
		feed_input(p,1,0,"    \\ \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,3,   "\\  \n")
		feed_input(p,1,0,"    \\ \n")
		feed_input(p,2,0," \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0," ",core.M_NONE))
			
	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,3,   "\\  \n")
		feed_input(p,1,0,"    \\ \n")
		feed_input(p,2,0,"     ")
		p.test(main.CurrentChar(2,5,"\\",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,6," ",core.M_NONE))
			
	def test_allows_line_to_end_at_right_edge(self):
		p = self.pclass()
		feed_input(p,0,3,   "\\  \n")
		feed_input(p,1,0,"    \\ \n")
		feed_input(p,2,0,"     \\\n")
		feed_input(p,3,0,"      \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(4,0," ",core.M_NONE))
			
	def test_allows_line_to_end_at_bottom_right_corner(self):
		p = self.pclass()
		feed_input(p,0,3,   "\\  \n")
		feed_input(p,1,0,"    \\ \n")
		feed_input(p,2,0,"     \\\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_line_to_start_at_left_edge(self):
		p = self.pclass()
		feed_input(p,1,0,"\\  \n")
		feed_input(p,2,0," \\ \n")
		feed_input(p,3,0,"   ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,3," ",core.M_NONE))
			
	def test_allows_line_to_start_at_top_left_corner(self):
		p = self.pclass()
		feed_input(p,0,0,"\\   \n")
		feed_input(p,1,0," \\  \n")
		feed_input(p,2,0,"   ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,3," ",core.M_NONE))
			
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((3,   "\\   \n"),
				 (0,"    \\  \n"),
				 (0,"     \\ \n"),
				 (0,"       "   ))
		s = core.M_OCCUPIED|core.M_LINE_START_SE
		o = core.M_OCCUPIED
		n = core.M_NONE
		a = core.M_LINE_AFTER_SE
		meta =  ((      s,n,n,n,n,),
				 (n,n,n,n,o,n,n,n,),
				 (n,n,n,n,n,o,n,n,),
				 (n,n,n,n,n,n,a,  )) 
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,startcol+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)
				
	def do_render(self,x,y,l):
		p = self.pclass()
		for i in range(l):
			feed_input(p,y+i,x+i,"\\\n")
			feed_input(p,y+i+1,0," "*(x-1+i))			
		feed_input(p,y+l,x+l," ")
		try:
			p.test(main.CurrentChar(y+l,x+l+1," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_line(self):
		r = self.do_render(4,2,2)
		self.assertEquals(1,len(r))
		self.assertTrue(isinstance(r[0],core.Line))
	
	def test_render_coordinates(self):
		l = self.do_render(4,2,2)[0]
		self.assertEquals((4,2),l.a)
		self.assertEquals((6,4),l.b)
		
	def test_render_coordinates_longer(self):
		l = self.do_render(5,1,3)[0]
		self.assertEquals((5,1),l.a)
		self.assertEquals((8,4),l.b)
	
	def test_render_z(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.C_FOREGROUND,l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.STROKE_SOLID,l.stype)	


class TestShortVertLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.ShortVertLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,2,  " |  \n")
		feed_input(p,1,0,"    ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,4," ",core.M_NONE))
			
	def test_allows_occupied_left_context(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2," ",core.M_OCCUPIED))
		
	def test_rejects_alpha_as_left_context(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"b",core.M_NONE))
			
	def test_rejects_numeric_as_left_context(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"9",core.M_NONE))
		
	def test_expects_pipe(self):
		p = self.pclass()
		feed_input(p,0,2," ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
			
	def test_expects_pipe_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2," ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"|",core.M_OCCUPIED))

	def test_allows_occupied_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," |")
		p.test(main.CurrentChar(0,4," ",core.M_OCCUPIED))

	def test_rejects_alpha_as_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," |")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"d",core.M_NONE))
			
	def test_rejects_numeric_as_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," |")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"5",core.M_NONE))

	def test_allows_rest_of_first_line(self):
		p = self.pclass()
		feed_input(p,0,2," | ")
		p.test(main.CurrentChar(0,5,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,6,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,7,"\n",core.M_OCCUPIED))

	def test_allows_start_of_second_line(self):
		p = self.pclass()
		feed_input(p,0,3," |  \n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,2,"c",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,3,"d",core.M_OCCUPIED))

	def test_allows_no_character_at_end_due_to_eoi(self):
		p = self.pclass()
		feed_input(p,0,3," |  \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,0,core.END_OF_INPUT,core.M_NONE))

	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,3,   " |  \n")
		feed_input(p,1,0,"\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0," ",core.M_NONE))

	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,2,  " |  \n")
		feed_input(p,1,0,"   ")
		p.test(main.CurrentChar(1,3,"|",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,4," ",core.M_NONE))

	def test_allows_line_at_left_edge(self):
		p = self.pclass()
		feed_input(p,1,8,"\n")
		feed_input(p,2,0,"|  \n")
		feed_input(p,3,0," ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,1," ",core.M_NONE))

	def test_allows_line_at_right_edge(self):
		p = self.pclass()
		feed_input(p,1,5,     " |\n")
		feed_input(p,2,0,"       ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,7,"\n",core.M_NONE))

	def test_allows_line_at_top_left_corner(self):
		p = self.pclass()
		p.test(main.CurrentChar(-1,0,core.START_OF_INPUT,core.M_NONE))
		feed_input(p,0,0,"|  \n")
		feed_input(p,1,0," ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,1," ",core.M_NONE))
			
	def test_allows_line_at_bottom_right_corner(self):
		p = self.pclass()
		feed_input(p,2,4, " |\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((4,    " |  \n"),
		         (0,"      "    ),)
		n = core.M_NONE
		s = core.M_OCCUPIED | core.M_LINE_START_S
		a = core.M_LINE_AFTER_S
		meta = ((        n,s,n,n,n,),
		        (n,n,n,n,n,a,      ),)
		for j,(linestart,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,linestart+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)
				
	def do_render(self,x,y,smeta=core.M_NONE,emeta=core.M_NONE):
		p = self.pclass()
		feed_input(p,y,x-1," ")
		p.test(main.CurrentChar(y,x,"|",smeta))
		feed_input(p,y,x+1,"| \n")
		feed_input(p,y+1,0," "*x)
		p.test(main.CurrentChar(y+1,x," ",emeta))
		try:
			p.test(main.CurrentChar(y+1,x+1," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_line(self):
		r = self.do_render(4,2)
		self.assertEquals(1,len(r))
		self.assertTrue(isinstance(r[0],core.Line))
	
	def test_render_coordinates(self):
		l = self.do_render(4,2)[0]
		self.assertEquals((4.5,2),l.a)
		self.assertEquals((4.5,3),l.b)
		
	def test_render_coordinates_start_box(self):
		l = self.do_render(4,2,smeta=core.M_BOX_AFTER_S)[0]
		self.assertEquals((4.5,1.5),l.a)
		self.assertEquals((4.5,3),l.b)

	def test_render_coordinates_end_box(self):
		l = self.do_render(4,2,emeta=core.M_BOX_START_S)[0]
		self.assertEquals((4.5,2),l.a)
		self.assertEquals((4.5,3.5),l.b)

	def test_render_coordinates_start_and_end_box(self):
		l = self.do_render(4,2,smeta=core.M_BOX_AFTER_S,emeta=core.M_BOX_START_S)[0]
		self.assertEquals((4.5,1.5),l.a)
		self.assertEquals((4.5,3.5),l.b)
		
	def test_render_z(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(core.C_FOREGROUND,l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(core.STROKE_SOLID,l.stype)	

	
class TestLongVertLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.LongVertLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,3,   "| \n")
		feed_input(p,1,0,"   | \n")
		feed_input(p,2,0,"   | \n")
		feed_input(p,3,0,"    ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,4," ",core.M_NONE))
			
	def test_expects_start_pipe(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
			
	def test_expects_start_pipe_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"|",core.M_OCCUPIED))
			
	def test_allows_rest_of_start_line(self):
		p = self.pclass()
		feed_input(p,0,3,"|")
		p.test(main.CurrentChar(0,4,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,5,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,6,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,3,"|\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,2,"c",core.M_OCCUPIED))
		
	def test_rejects_length_one_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "|\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2," ",core.M_NONE))
	
	def test_rejects_length_one_line_with_early_end(self):
		p = self.pclass()
		feed_input(p,0,2,  "|\n")
		feed_input(p,1,0,"\n")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,0," ",core.M_NONE))
	
	def test_accepts_rest_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "|\n")
		feed_input(p,1,0,"  |")
		p.test(main.CurrentChar(1,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,4,"\n",core.M_OCCUPIED))
		
	def test_allows_no_character_at_end_due_to_eoi(self):
		p = self.pclass()
		feed_input(p,0,2,  "| \n")
		feed_input(p,1,0,"  | \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,3,   "| \n")
		feed_input(p,1,0,"   | \n")
		feed_input(p,2,0,"\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0," ",core.M_NONE))
			
	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "| \n")
		feed_input(p,1,0,"  | \n")
		feed_input(p,2,0,"  ")
		p.test(main.CurrentChar(2,2,"|",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,3," ",core.M_NONE))
			
	def test_allows_line_to_end_at_bottom_left(self):
		p = self.pclass()
		feed_input(p,3,0,"| \n")
		feed_input(p,4,0,"| \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_line_to_end_at_bottom_right(self):
		p = self.pclass()
		feed_input(p,0,3,   "|\n")
		feed_input(p,1,0,"   |\n")
		feed_input(p,2,0,"   |\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
	
	def test_allows_line_to_start_at_left_edge(self):
		p = self.pclass()
		feed_input(p,2,0,"|\n")
		feed_input(p,3,0,"|\n")
		feed_input(p,4,0," ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(4,1," ",core.M_NONE))
	
	def test_allows_line_to_start_at_top_left_corner(self):
		p = self.pclass()
		feed_input(p,0,0,"|\n")
		feed_input(p,1,0,"|\n")
		feed_input(p,2,0," ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,1," ",core.M_NONE))
	
	def test_allows_line_to_start_at_bottom_left_corner(self):
		p = self.pclass()
		feed_input(p,4,0,"|\n")
		feed_input(p,5,0,"|\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(6,0,core.END_OF_INPUT,core.M_NONE))
		
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((3,   "|  \n"),
				 (0,"   |  \n"),
				 (0,"   |  \n"),
				 (0,"    "    ))
		s = core.M_OCCUPIED|core.M_LINE_START_S
		o = core.M_OCCUPIED
		n = core.M_NONE
		a = core.M_LINE_AFTER_S
		meta =  ((      s,n,n,n,),
				 (n,n,n,o,n,n,n,),
				 (n,n,n,o,n,n,n,),
				 (n,n,n,a,      )) 
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,startcol+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)
				
	def do_render(self,x,y,l,smeta=core.M_NONE,emeta=core.M_NONE):
		p = self.pclass()
		for i in range(l):
			p.test(main.CurrentChar(y+i,x,"|",smeta if i==0 else core.M_NONE))
			p.test(main.CurrentChar(y+i,x+1,"\n",core.M_NONE))
			feed_input(p,y+i+1,0," "*x)			
		p.test(main.CurrentChar(y+l,x," ",emeta))
		try:
			p.test(main.CurrentChar(y+l,x+1," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_line(self):
		r = self.do_render(4,2,2)
		self.assertEquals(1,len(r))
		self.assertTrue(isinstance(r[0],core.Line))
	
	def test_render_coordinates(self):
		l = self.do_render(4,2,2)[0]
		self.assertEquals((4.5,2),l.a)
		self.assertEquals((4.5,4),l.b)
		
	def test_render_coordinates_longer(self):
		l = self.do_render(5,1,3)[0]
		self.assertEquals((5.5,1),l.a)
		self.assertEquals((5.5,4),l.b)
	
	def test_render_coordinates_start_box(self):
		l = self.do_render(4,2,2,smeta=core.M_BOX_AFTER_S)[0]
		self.assertEquals((4.5,1.5),l.a)
		self.assertEquals((4.5,4),l.b)

	def test_render_coordinates_end_box(self):
		l = self.do_render(4,2,2,emeta=core.M_BOX_START_S)[0]
		self.assertEquals((4.5,2),l.a)
		self.assertEquals((4.5,4.5),l.b)

	def test_render_coordinates_start_and_end_box(self):
		l = self.do_render(4,2,2,smeta=core.M_BOX_AFTER_S,emeta=core.M_BOX_START_S)[0]
		self.assertEquals((4.5,1.5),l.a)
		self.assertEquals((4.5,4.5),l.b)

	def test_render_z(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.C_FOREGROUND,l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.STROKE_SOLID,l.stype)	


class TestShortHorizLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.ShortHorizLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,2, " - ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,5," ",core.M_NONE))
			
	def test_allows_occupied_left_context(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2," ",core.M_OCCUPIED))
		
	def test_rejects_alpha_as_left_context(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"b",core.M_NONE))
			
	def test_rejects_numeric_as_left_context(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"9",core.M_NONE))
		
	def test_expects_hyphen(self):
		p = self.pclass()
		feed_input(p,0,2," ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
			
	def test_expects_hyphen_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2," ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"-",core.M_OCCUPIED))

	def test_allows_occupied_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," -")
		p.test(main.CurrentChar(0,4," ",core.M_OCCUPIED))

	def test_rejects_alpha_as_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," -")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"d",core.M_NONE))
			
	def test_rejects_numeric_as_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," -")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"5",core.M_NONE))

	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,2,  " -")
		p.test(main.CurrentChar(0,4,"-",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,5," ",core.M_NONE))

	def test_allows_line_at_left_edge(self):
		p = self.pclass()
		feed_input(p,1,8,"\n")
		feed_input(p,2,0,"- ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,2," ",core.M_NONE))

	def test_allows_line_at_right_edge(self):
		p = self.pclass()
		feed_input(p,1,5,     " -\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0," ",core.M_NONE))

	def test_allows_line_at_top_left_corner(self):
		p = self.pclass()
		p.test(main.CurrentChar(-1,0,core.START_OF_INPUT,core.M_NONE))
		feed_input(p,0,0,"- ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,2," ",core.M_NONE))
			
	def test_allows_line_at_bottom_right_corner(self):
		p = self.pclass()
		feed_input(p,2,2,  " -\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((4,    " - "),)
		n = core.M_NONE
		s = core.M_OCCUPIED | core.M_LINE_START_E
		a = core.M_LINE_AFTER_E
		meta = ((        n,s,a,),)
		for j,(linestart,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,linestart+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)
				
	def do_render(self,x,y,smeta=core.M_NONE,emeta=core.M_NONE):
		p = self.pclass()
		p.test(main.CurrentChar(y,x-1," ",core.M_NONE))
		p.test(main.CurrentChar(y,x,"-",smeta))
		p.test(main.CurrentChar(y,x+1," ",emeta))		
		try:
			p.test(main.CurrentChar(y,x+2," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_line(self):
		r = self.do_render(4,2)
		self.assertEquals(1,len(r))
		self.assertTrue(isinstance(r[0],core.Line))
	
	def test_render_coordinates(self):
		l = self.do_render(4,2)[0]
		self.assertEquals((4,2.5),l.a)
		self.assertEquals((5,2.5),l.b)
		
	def test_render_coordinates_start_box(self):
		l = self.do_render(4,2,smeta=core.M_BOX_AFTER_E)[0]
		self.assertEquals((3.5,2.5),l.a)
		self.assertEquals((5,2.5),l.b)

	def test_render_coordinates_end_box(self):
		l = self.do_render(4,2,emeta=core.M_BOX_START_E)[0]
		self.assertEquals((4,2.5),l.a)
		self.assertEquals((5.5,2.5),l.b)

	def test_render_coordinates_start_and_end_box(self):
		l = self.do_render(4,2,smeta=core.M_BOX_AFTER_E,emeta=core.M_BOX_START_E)[0]
		self.assertEquals((3.5,2.5),l.a)
		self.assertEquals((5.5,2.5),l.b)
		
	def test_render_z(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(core.C_FOREGROUND,l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(core.STROKE_SOLID,l.stype)	

								
class TestLongHorizLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.LongHorizLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,3,  "--- ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,7," ",core.M_NONE))
			
	def test_expects_start_hyphen(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))

	def test_expects_start_hyphen_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"-",core.M_OCCUPIED))
			
	def test_rejects_length_one_line(self):
		p = self.pclass()
		feed_input(p,0,2, "-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
			
	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,2, "---")
		p.test(main.CurrentChar(0,5,"-",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,6," ",core.M_NONE))
			
	def test_allows_line_to_end_at_bottom_right(self):
		p = self.pclass()
		feed_input(p,2,3,"---\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
					
	def test_allows_line_to_start_at_left_edge(self):
		p = self.pclass()
		feed_input(p,1,0,"-- ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
	
	def test_allows_line_to_start_at_top_left_corner(self):
		p = self.pclass()
		feed_input(p,0,0,"-- ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
	
	def test_allows_line_to_start_at_bottom_left_corner(self):
		p = self.pclass()
		feed_input(p,4,0,"-- ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(4,3,"\n",core.M_NONE))
					
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((3,  "--- "),)
		s = core.M_OCCUPIED|core.M_LINE_START_E
		o = core.M_OCCUPIED
		a = core.M_LINE_AFTER_E
		meta =  ((s,o,o,a,),)
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,startcol+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)
				
	def do_render(self,x,y,l,smeta=core.M_NONE,emeta=core.M_NONE):
		p = self.pclass()
		p.test(main.CurrentChar(y,x,"-",smeta))
		feed_input(p,y,x+1,"-"*(l-1))
		p.test(main.CurrentChar(y,x+l," ",emeta))
		try:
			p.test(main.CurrentChar(y,x+l+1," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_line(self):
		r = self.do_render(4,2,2)
		self.assertEquals(1,len(r))
		self.assertTrue(isinstance(r[0],core.Line))
	
	def test_render_coordinates(self):
		l = self.do_render(4,2,2)[0]
		self.assertEquals((4,2.5),l.a)
		self.assertEquals((6,2.5),l.b)
		
	def test_render_coordinates_longer(self):
		l = self.do_render(5,1,3)[0]
		self.assertEquals((5,1.5),l.a)
		self.assertEquals((8,1.5),l.b)
	
	def test_render_coordinates_start_box(self):
		l = self.do_render(4,2,2,smeta=core.M_BOX_AFTER_E)[0]
		self.assertEquals((3.5,2.5),l.a)
		self.assertEquals((6,2.5),l.b)

	def test_render_coordinates_end_box(self):
		l = self.do_render(4,2,2,emeta=core.M_BOX_START_E)[0]
		self.assertEquals((4,2.5),l.a)
		self.assertEquals((6.5,2.5),l.b)
		
	def test_render_coordinates_start_and_end_box(self):
		l = self.do_render(4,2,2,smeta=core.M_BOX_AFTER_E,emeta=core.M_BOX_START_E)[0]
		self.assertEquals((3.5,2.5),l.a)
		self.assertEquals((6.5,2.5),l.b)

	def test_render_z(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.C_FOREGROUND,l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.STROKE_SOLID,l.stype)	


class TestShortUpDiagDashedLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.ShortUpDiagDashedLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,2,  " ,  \n")
		feed_input(p,1,0,"   ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_allows_occupied_left_context(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2," ",core.M_OCCUPIED))
		
	def test_rejects_alpha_as_left_context(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"b",core.M_NONE))
			
	def test_rejects_numeric_as_left_context(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"9",core.M_NONE))
		
	def test_expects_comma(self):
		p = self.pclass()
		feed_input(p,0,2," ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
			
	def test_expects_comma_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2," ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,",",core.M_OCCUPIED))

	def test_allows_occupied_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," ,")
		p.test(main.CurrentChar(0,4," ",core.M_OCCUPIED))

	def test_rejects_alpha_as_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," ,")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"d",core.M_NONE))
			
	def test_rejects_numeric_as_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," ,")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"5",core.M_NONE))

	def test_allows_rest_of_first_line(self):
		p = self.pclass()
		feed_input(p,0,2," , ")
		p.test(main.CurrentChar(0,5,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,6,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,7,"\n",core.M_OCCUPIED))

	def test_allows_start_of_second_line(self):
		p = self.pclass()
		feed_input(p,0,3," ,  \n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,2,"c",core.M_OCCUPIED))

	def test_allows_no_character_at_end_due_to_eoi(self):
		p = self.pclass()
		feed_input(p,0,3," ,  \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,0,core.END_OF_INPUT,core.M_NONE))

	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,3,   " ,  \n")
		feed_input(p,1,0,"\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0," ",core.M_NONE))

	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,2,  " ,\n")
		feed_input(p,1,0,"  ")
		p.test(main.CurrentChar(1,2,",",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))

	def test_allows_line_at_left_edge(self):
		p = self.pclass()
		feed_input(p,1,8,"\n")
		feed_input(p,2,0,",  \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0," ",core.M_NONE))

	def test_allows_line_at_right_edge(self):
		p = self.pclass()
		feed_input(p,1,5,     " ,\n")
		feed_input(p,2,0,"      ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,6," ",core.M_NONE))

	def test_allows_line_at_top_left_corner(self):
		p = self.pclass()
		p.test(main.CurrentChar(-1,0,core.START_OF_INPUT,core.M_NONE))
		feed_input(p,0,0,",  \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,0," ",core.M_NONE))
			
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((4,    " ,  \n"),
		         (0,"     "     ),)
		n = core.M_NONE
		s = core.M_OCCUPIED | core.M_LINE_START_SW | core.M_DASH_START_SW
		a = core.M_LINE_AFTER_SW | core.M_DASH_AFTER_SW
		meta = ((        n,s,n,n,n,),
		        (n,n,n,n,a,        ),)
		for j,(linestart,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,linestart+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)
				
	def do_render(self,x,y):
		p = self.pclass()
		feed_input(p,y,x-1," , \n")
		feed_input(p,y+1,0," "*(x-1))
		try:
			p.test(main.CurrentChar(y+1,x," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_line(self):
		r = self.do_render(4,2)
		self.assertEquals(1,len(r))
		self.assertTrue(isinstance(r[0],core.Line))
	
	def test_render_coordinates(self):
		l = self.do_render(4,2)[0]
		self.assertEquals((5,2),l.a)
		self.assertEquals((4,3),l.b)
		
	def test_render_z(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(core.C_FOREGROUND,l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(core.STROKE_DASHED,l.stype)


class TestLongUpDiagDashedLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.LongUpDiagDashedLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,3,   ",\n")
		feed_input(p,1,0,"  , \n")
		feed_input(p,2,0," ,  \n")
		feed_input(p,3,0," ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,1," ",core.M_NONE))

	def test_expects_start_comma(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2," ",core.M_NONE))

	def test_expects_start_comma_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,",",core.M_OCCUPIED))
			
	def test_allows_rest_of_start_line(self):
		p = self.pclass()
		feed_input(p,0,2,",")
		p.test(main.CurrentChar(0,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,4,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,5,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,3,",\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		
	def test_accepts_rest_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,3,   ",\n")
		feed_input(p,1,0,"  ,")
		p.test(main.CurrentChar(1,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,4,"\n",core.M_OCCUPIED))
		
	def test_allows_no_character_at_end_due_to_eoi(self):
		p = self.pclass()
		feed_input(p,0,3,   ",  \n")
		feed_input(p,1,0,"  , \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,4,    ",  \n")
		feed_input(p,1,0,"   ,   \n")
		feed_input(p,2,0,"\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0," ",core.M_NONE))
			
	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,3,   ",\n")
		feed_input(p,1,0,"  , \n")
		feed_input(p,2,0," ")
		p.test(main.CurrentChar(2,1,",",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,2," ",core.M_NONE))
			
	def test_allows_line_to_end_at_left_edge(self):
		p = self.pclass()
		feed_input(p,0,2,  ",\n")
		feed_input(p,1,0," , \n")
		feed_input(p,2,0,",  \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0," ",core.M_NONE))
			
	def test_allows_line_to_end_at_bottom_left_corner(self):
		p = self.pclass()
		feed_input(p,0,2,  ",\n")
		feed_input(p,1,0," , \n")
		feed_input(p,2,0,",  \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))

	def test_rejects_length_one_line(self):
		p = self.pclass()
		feed_input(p,0,2,  ",\n")
		feed_input(p,1,0," ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,1," ",core.M_NONE))

	def test_rejects_length_one_line_with_early_end(self):
		p = self.pclass()
		feed_input(p,0,2,  ",\n")
		feed_input(p,1,0,"\n")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,0," ",core.M_NONE))

	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((3,   ",  \n"),
				 (0,"  ,   \n"),
				 (0," ,    \n"),
				 (0," "       ))
		s = core.M_OCCUPIED|core.M_LINE_START_SW | core.M_DASH_START_SW
		o = core.M_OCCUPIED
		n = core.M_NONE
		a = core.M_LINE_AFTER_SW | core.M_DASH_AFTER_SW
		meta =  ((      s,n,n,n,),
				 (n,n,o,n,n,n,n,),
				 (n,o,n,n,n,n,n,),
				 (a,            )) 
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,startcol+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)
				
	def do_render(self,x,y,l):
		p = self.pclass()
		for i in range(l):
			feed_input(p,y+i,x-i,",\n")
			feed_input(p,y+i+1,0," "*(x-1-i))			
		feed_input(p,y+l,x-l," ")
		try:
			p.test(main.CurrentChar(y+l,x-l+1," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_line(self):
		r = self.do_render(4,2,2)
		self.assertEquals(1,len(r))
		self.assertTrue(isinstance(r[0],core.Line))
	
	def test_render_coordinates(self):
		l = self.do_render(4,2,2)[0]
		self.assertEquals((5,2),l.a)
		self.assertEquals((3,4),l.b)
		
	def test_render_coordinates_longer(self):
		l = self.do_render(5,1,3)[0]
		self.assertEquals((6,1),l.a)
		self.assertEquals((3,4),l.b)
	
	def test_render_z(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.C_FOREGROUND,l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.STROKE_DASHED,l.stype)


class TestShortDownDiagDashedLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.ShortDownDiagDashedLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,2,  " `  \n")
		feed_input(p,1,0,"     ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,5," ",core.M_NONE))
			
	def test_allows_occupied_left_context(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2," ",core.M_OCCUPIED))
		
	def test_rejects_alpha_as_left_context(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"b",core.M_NONE))
			
	def test_rejects_numeric_as_left_context(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"9",core.M_NONE))
		
	def test_expects_backtick(self):
		p = self.pclass()
		feed_input(p,0,2," ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
			
	def test_expects_backtick_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2," ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"`",core.M_OCCUPIED))

	def test_allows_occupied_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," `")
		p.test(main.CurrentChar(0,4," ",core.M_OCCUPIED))

	def test_rejects_alpha_as_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," `")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"d",core.M_NONE))
			
	def test_rejects_numeric_as_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," `")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"5",core.M_NONE))

	def test_allows_rest_of_first_line(self):
		p = self.pclass()
		feed_input(p,0,2," ` ")
		p.test(main.CurrentChar(0,5,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,6,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,7,"\n",core.M_OCCUPIED))

	def test_allows_start_of_second_line(self):
		p = self.pclass()
		feed_input(p,0,3," `  \n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,2,"c",core.M_OCCUPIED))

	def test_allows_no_character_at_end_due_to_eoi(self):
		p = self.pclass()
		feed_input(p,0,3," `  \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,0,core.END_OF_INPUT,core.M_NONE))

	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,3,   " `  \n")
		feed_input(p,1,0,"\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0," ",core.M_NONE))

	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,2,  " `  \n")
		feed_input(p,1,0,"    ")
		p.test(main.CurrentChar(1,4,"`",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,5," ",core.M_NONE))

	def test_allows_line_at_left_edge(self):
		p = self.pclass()
		feed_input(p,1,8,"\n")
		feed_input(p,2,0,"`  \n")
		feed_input(p,3,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,2," ",core.M_NONE))

	def test_allows_line_at_right_edge(self):
		p = self.pclass()
		feed_input(p,1,5,     " `\n")
		feed_input(p,2,0,"       \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0," ",core.M_NONE))

	def test_allows_line_at_top_left_corner(self):
		p = self.pclass()
		p.test(main.CurrentChar(-1,0,core.START_OF_INPUT,core.M_NONE))
		feed_input(p,0,0,"`  \n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2," ",core.M_NONE))
			
	def test_allows_bottom_right_corner(self):
		p = self.pclass()
		feed_input(p,2,2," `  \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((4,    " `  \n"),
		         (0,"       "    ),)
		n = core.M_NONE
		s = core.M_OCCUPIED | core.M_LINE_START_SE | core.M_DASH_START_SE
		a = core.M_LINE_AFTER_SE | core.M_DASH_AFTER_SE
		meta = ((        n,s,n,n,n,),
		        (n,n,n,n,n,n,a,    ),)
		for j,(linestart,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,linestart+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)
				
	def do_render(self,x,y):
		p = self.pclass()
		feed_input(p,y,x-1," ` \n")
		feed_input(p,y+1,0," "*(x+2))
		try:
			p.test(main.CurrentChar(y+1,x+2," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_line(self):
		r = self.do_render(4,2)
		self.assertEquals(1,len(r))
		self.assertTrue(isinstance(r[0],core.Line))
	
	def test_render_coordinates(self):
		l = self.do_render(4,2)[0]
		self.assertEquals((4,2),l.a)
		self.assertEquals((5,3),l.b)
		
	def test_render_z(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(core.C_FOREGROUND,l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(core.STROKE_DASHED,l.stype)	


class TestLongDownDiagDasheLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.LongDownDiagDashedLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "`   \n")
		feed_input(p,1,0,"   `  \n")
		feed_input(p,2,0,"    ` \n")
		feed_input(p,3,0,"      ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,6," ",core.M_NONE))
			
	def test_expects_start_backtick(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
			
	def test_expects_start_backtick_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"`",core.M_OCCUPIED))
			
	def test_allows_rest_of_start_line(self):
		p = self.pclass()
		feed_input(p,0,3,"`")
		p.test(main.CurrentChar(0,4,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,5,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,6,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,2,"`\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,2,"c",core.M_OCCUPIED))
		
	def test_rejects_length_one_line(self):
		p = self.pclass()
		feed_input(p,0,3,   "`\n")
		feed_input(p,1,0,"    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,4," ",core.M_NONE))
	
	def test_rejects_length_one_line_with_early_end(self):
		p = self.pclass()
		feed_input(p,0,3,   "`\n")
		feed_input(p,1,0,"\n")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,0," ",core.M_NONE))
	
	def test_accepts_rest_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,3,   "`\n")
		feed_input(p,1,0,"    `")
		p.test(main.CurrentChar(1,5,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,6,"\n",core.M_OCCUPIED))
		
	def test_allows_no_character_at_end_due_to_eoi(self):
		p = self.pclass()
		feed_input(p,0,3,   "`  \n")
		feed_input(p,1,0,"    ` \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,3,   "`  \n")
		feed_input(p,1,0,"    ` \n")
		feed_input(p,2,0," \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0," ",core.M_NONE))
			
	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,3,   "`  \n")
		feed_input(p,1,0,"    ` \n")
		feed_input(p,2,0,"     ")
		p.test(main.CurrentChar(2,5,"`",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,6," ",core.M_NONE))
			
	def test_allows_line_to_end_at_right_edge(self):
		p = self.pclass()
		feed_input(p,0,3,   "`  \n")
		feed_input(p,1,0,"    ` \n")
		feed_input(p,2,0,"     `\n")
		feed_input(p,3,0,"      \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(4,0," ",core.M_NONE))
			
	def test_allows_line_to_end_at_bottom_right_corner(self):
		p = self.pclass()
		feed_input(p,0,3,   "`  \n")
		feed_input(p,1,0,"    ` \n")
		feed_input(p,2,0,"     `\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_line_to_start_at_left_edge(self):
		p = self.pclass()
		feed_input(p,1,0,"`  \n")
		feed_input(p,2,0," ` \n")
		feed_input(p,3,0,"   ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,3," ",core.M_NONE))
			
	def test_allows_line_to_start_at_top_left_corner(self):
		p = self.pclass()
		feed_input(p,0,0,"`   \n")
		feed_input(p,1,0," `  \n")
		feed_input(p,2,0,"   ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,3," ",core.M_NONE))
			
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((3,   "`   \n"),
				 (0,"    `  \n"),
				 (0,"     ` \n"),
				 (0,"       "   ))
		s = core.M_OCCUPIED | core.M_LINE_START_SE | core.M_DASH_START_SE
		o = core.M_OCCUPIED
		n = core.M_NONE
		a = core.M_LINE_AFTER_SE | core.M_DASH_AFTER_SE
		meta =  ((      s,n,n,n,n,),
				 (n,n,n,n,o,n,n,n,),
				 (n,n,n,n,n,o,n,n,),
				 (n,n,n,n,n,n,a,  )) 
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,startcol+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)
				
	def do_render(self,x,y,l):
		p = self.pclass()
		for i in range(l):
			feed_input(p,y+i,x+i,"`\n")
			feed_input(p,y+i+1,0," "*(x-1+i))			
		feed_input(p,y+l,x+l," ")
		try:
			p.test(main.CurrentChar(y+l,x+l+1," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_line(self):
		r = self.do_render(4,2,2)
		self.assertEquals(1,len(r))
		self.assertTrue(isinstance(r[0],core.Line))
	
	def test_render_coordinates(self):
		l = self.do_render(4,2,2)[0]
		self.assertEquals((4,2),l.a)
		self.assertEquals((6,4),l.b)
		
	def test_render_coordinates_longer(self):
		l = self.do_render(5,1,3)[0]
		self.assertEquals((5,1),l.a)
		self.assertEquals((8,4),l.b)
	
	def test_render_z(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.C_FOREGROUND,l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.STROKE_DASHED,l.stype)	
	
	
class TestShortVertDashedLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.ShortVertDashedLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,2,  " ;  \n")
		feed_input(p,1,0,"    ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,4," ",core.M_NONE))
			
	def test_allows_occupied_left_context(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2," ",core.M_OCCUPIED))
		
	def test_rejects_alpha_as_left_context(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"b",core.M_NONE))
			
	def test_rejects_numeric_as_left_context(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"9",core.M_NONE))
		
	def test_expects_semicolon(self):
		p = self.pclass()
		feed_input(p,0,2," ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
			
	def test_expects_semicolon_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2," ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,";",core.M_OCCUPIED))

	def test_allows_occupied_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," ;")
		p.test(main.CurrentChar(0,4," ",core.M_OCCUPIED))

	def test_rejects_alpha_as_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," ;")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"d",core.M_NONE))
			
	def test_rejects_numeric_as_right_context(self):
		p = self.pclass()
		feed_input(p,0,2," ;")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"5",core.M_NONE))

	def test_allows_rest_of_first_line(self):
		p = self.pclass()
		feed_input(p,0,2," ; ")
		p.test(main.CurrentChar(0,5,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,6,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,7,"\n",core.M_OCCUPIED))

	def test_allows_start_of_second_line(self):
		p = self.pclass()
		feed_input(p,0,3," ;  \n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,2,"c",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,3,"d",core.M_OCCUPIED))

	def test_allows_no_character_at_end_due_to_eoi(self):
		p = self.pclass()
		feed_input(p,0,3," ;  \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,0,core.END_OF_INPUT,core.M_NONE))

	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,3,   " ;  \n")
		feed_input(p,1,0,"\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0," ",core.M_NONE))

	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,2,  " ;  \n")
		feed_input(p,1,0,"   ")
		p.test(main.CurrentChar(1,3,";",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,4," ",core.M_NONE))

	def test_allows_line_at_left_edge(self):
		p = self.pclass()
		feed_input(p,1,8,"\n")
		feed_input(p,2,0,";  \n")
		feed_input(p,3,0," ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,1," ",core.M_NONE))

	def test_allows_line_at_right_edge(self):
		p = self.pclass()
		feed_input(p,1,5,     " ;\n")
		feed_input(p,2,0,"       ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,7,"\n",core.M_NONE))

	def test_allows_line_at_top_left_corner(self):
		p = self.pclass()
		p.test(main.CurrentChar(-1,0,core.START_OF_INPUT,core.M_NONE))
		feed_input(p,0,0,";  \n")
		feed_input(p,1,0," ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,1," ",core.M_NONE))
			
	def test_allows_line_at_bottom_right_corner(self):
		p = self.pclass()
		feed_input(p,2,4, " ;\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((4,    " ;  \n"),
		         (0,"      "    ),)
		n = core.M_NONE
		s = core.M_OCCUPIED | core.M_LINE_START_S | core.M_DASH_START_S
		a = core.M_LINE_AFTER_S | core.M_DASH_AFTER_S
		meta = ((        n,s,n,n,n,),
		        (n,n,n,n,n,a,      ),)
		for j,(linestart,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,linestart+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)
				
	def do_render(self,x,y,smeta=core.M_NONE,emeta=core.M_NONE):
		p = self.pclass()
		feed_input(p,y,x-1," ")
		p.test(main.CurrentChar(y,x,";",smeta))
		feed_input(p,y,x+1,"; \n")
		feed_input(p,y+1,0," "*x)
		p.test(main.CurrentChar(y+1,x," ",emeta))
		try:
			p.test(main.CurrentChar(y+1,x+1," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_line(self):
		r = self.do_render(4,2)
		self.assertEquals(1,len(r))
		self.assertTrue(isinstance(r[0],core.Line))
	
	def test_render_coordinates(self):
		l = self.do_render(4,2)[0]
		self.assertEquals((4.5,2),l.a)
		self.assertEquals((4.5,3),l.b)
		
	def test_render_coordinates_start_box(self):
		l = self.do_render(4,2,smeta=core.M_BOX_AFTER_S)[0]
		self.assertEquals((4.5,1.5),l.a)
		self.assertEquals((4.5,3),l.b)

	def test_render_coordinates_end_box(self):
		l = self.do_render(4,2,emeta=core.M_BOX_START_S)[0]
		self.assertEquals((4.5,2),l.a)
		self.assertEquals((4.5,3.5),l.b)

	def test_render_coordinates_start_and_end_box(self):
		l = self.do_render(4,2,smeta=core.M_BOX_AFTER_S,emeta=core.M_BOX_START_S)[0]
		self.assertEquals((4.5,1.5),l.a)
		self.assertEquals((4.5,3.5),l.b)
		
	def test_render_z(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(core.C_FOREGROUND,l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3)[0]
		self.assertEquals(core.STROKE_DASHED,l.stype)	
	
	
class TestLongVertDashedLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.LongVertDashedLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,3,   "; \n")
		feed_input(p,1,0,"   ; \n")
		feed_input(p,2,0,"   ; \n")
		feed_input(p,3,0,"    ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,4," ",core.M_NONE))
			
	def test_expects_start_semicolon(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
			
	def test_expects_start_semicolon_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,";",core.M_OCCUPIED))
			
	def test_allows_rest_of_start_line(self):
		p = self.pclass()
		feed_input(p,0,3,";")
		p.test(main.CurrentChar(0,4,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,5,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,6,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,3,";\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,2,"c",core.M_OCCUPIED))
		
	def test_rejects_length_one_line(self):
		p = self.pclass()
		feed_input(p,0,2,  ";\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2," ",core.M_NONE))
	
	def test_rejects_length_one_line_with_early_end(self):
		p = self.pclass()
		feed_input(p,0,2,  ";\n")
		feed_input(p,1,0,"\n")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,0," ",core.M_NONE))
	
	def test_accepts_rest_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,2,  ";\n")
		feed_input(p,1,0,"  ;")
		p.test(main.CurrentChar(1,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,4,"\n",core.M_OCCUPIED))
		
	def test_allows_no_character_at_end_due_to_eoi(self):
		p = self.pclass()
		feed_input(p,0,2,  "; \n")
		feed_input(p,1,0,"  ; \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,3,   "; \n")
		feed_input(p,1,0,"   ; \n")
		feed_input(p,2,0,"\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0," ",core.M_NONE))
			
	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "; \n")
		feed_input(p,1,0,"  ; \n")
		feed_input(p,2,0,"  ")
		p.test(main.CurrentChar(2,2,";",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,3," ",core.M_NONE))
			
	def test_allows_line_to_end_at_bottom_left(self):
		p = self.pclass()
		feed_input(p,3,0,"; \n")
		feed_input(p,4,0,"; \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_line_to_end_at_bottom_right(self):
		p = self.pclass()
		feed_input(p,0,3,   ";\n")
		feed_input(p,1,0,"   ;\n")
		feed_input(p,2,0,"   ;\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
	
	def test_allows_line_to_start_at_left_edge(self):
		p = self.pclass()
		feed_input(p,2,0,";\n")
		feed_input(p,3,0,";\n")
		feed_input(p,4,0," ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(4,1," ",core.M_NONE))
	
	def test_allows_line_to_start_at_top_left_corner(self):
		p = self.pclass()
		feed_input(p,0,0,";\n")
		feed_input(p,1,0,";\n")
		feed_input(p,2,0," ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,1," ",core.M_NONE))
	
	def test_allows_line_to_start_at_bottom_left_corner(self):
		p = self.pclass()
		feed_input(p,4,0,";\n")
		feed_input(p,5,0,";\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(6,0,core.END_OF_INPUT,core.M_NONE))
		
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((3,   ";  \n"),
				 (0,"   ;  \n"),
				 (0,"   ;  \n"),
				 (0,"    "    ))
		s = core.M_OCCUPIED | core.M_LINE_START_S | core.M_DASH_START_S
		o = core.M_OCCUPIED
		n = core.M_NONE
		a = core.M_LINE_AFTER_S | core.M_DASH_AFTER_S
		meta =  ((      s,n,n,n,),
				 (n,n,n,o,n,n,n,),
				 (n,n,n,o,n,n,n,),
				 (n,n,n,a,      )) 
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,startcol+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)
				
	def do_render(self,x,y,l,smeta=core.M_NONE,emeta=core.M_NONE):
		p = self.pclass()
		for i in range(l):
			p.test(main.CurrentChar(y+i,x,";",smeta if i==0 else core.M_NONE))
			p.test(main.CurrentChar(y+i,x+1,"\n",core.M_NONE))
			feed_input(p,y+i+1,0," "*x)			
		p.test(main.CurrentChar(y+l,x," ",emeta))
		try:
			p.test(main.CurrentChar(y+l,x+1," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_line(self):
		r = self.do_render(4,2,2)
		self.assertEquals(1,len(r))
		self.assertTrue(isinstance(r[0],core.Line))
	
	def test_render_coordinates(self):
		l = self.do_render(4,2,2)[0]
		self.assertEquals((4.5,2),l.a)
		self.assertEquals((4.5,4),l.b)
		
	def test_render_coordinates_longer(self):
		l = self.do_render(5,1,3)[0]
		self.assertEquals((5.5,1),l.a)
		self.assertEquals((5.5,4),l.b)
	
	def test_render_coordinates_start_box(self):
		l = self.do_render(4,2,2,smeta=core.M_BOX_AFTER_S)[0]
		self.assertEquals((4.5,1.5),l.a)
		self.assertEquals((4.5,4),l.b)

	def test_render_coordinates_end_box(self):
		l = self.do_render(4,2,2,emeta=core.M_BOX_START_S)[0]
		self.assertEquals((4.5,2),l.a)
		self.assertEquals((4.5,4.5),l.b)

	def test_render_coordinates_start_and_end_box(self):
		l = self.do_render(4,2,2,smeta=core.M_BOX_AFTER_S,emeta=core.M_BOX_START_S)[0]
		self.assertEquals((4.5,1.5),l.a)
		self.assertEquals((4.5,4.5),l.b)

	def test_render_z(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.C_FOREGROUND,l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.STROKE_DASHED,l.stype)		
		
		
class TestLongHorizDashedLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.LongHorizDashedLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,3,   "- - -  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,10," ",core.M_NONE))
	
	def test_expects_start_hyphen(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
	
	def test_expects_start_hyphen_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"-",core.M_OCCUPIED))
			
	def test_expects_space_after_hypen(self):
		p = self.pclass()
		feed_input(p,0,3,"-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"-",core.M_NONE))
			
	def test_space_after_hyphen_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,3,"-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4," ",core.M_OCCUPIED))
	
	def test_expects_space_after_second_hyphen(self):
		p = self.pclass()
		feed_input(p,0,3,"- -")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,6,"-",core.M_NONE))
			
	def test_expects_space_after_second_hyphen_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,3,"- -")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,6," ",core.M_OCCUPIED))
		
	def test_doesnt_accept_two_char_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "- ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4," ",core.M_NONE))
	
	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,3,   "- - \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,0," ",core.M_NONE))
	
	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "- - ")
		p.test(main.CurrentChar(0,6,"-",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,7," ",core.M_NONE))
	
	def test_allows_line_to_end_at_bottom_right(self):
		p = self.pclass()
		feed_input(p,2,3,"- - \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
	
	def test_allows_line_to_start_at_left_edge(self):
		p = self.pclass()
		feed_input(p,2,0,"- -  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,5," ",core.M_NONE))
	
	def test_allows_line_to_start_at_top_left_corner(self):
		p = self.pclass()
		feed_input(p,0,0,"- -  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,5," ",core.M_NONE))
	
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((3,  "- - - -  "),)
		s = core.M_OCCUPIED | core.M_LINE_START_E | core.M_DASH_START_E
		o = core.M_OCCUPIED
		n = core.M_NONE
		a = core.M_LINE_AFTER_E | core.M_DASH_AFTER_E
		meta =  ((s,o,o,o,o,o,o,o,a,),)
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,startcol+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)
	
	def do_render(self,x,y,l,smeta=core.M_NONE,emeta=core.M_NONE):
		p = self.pclass()
		p.test(main.CurrentChar(y,x,"-",smeta))
		p.test(main.CurrentChar(y,x+1," ",core.M_NONE))
		feed_input(p,y,x+2,"- "*(l//2-1))
		p.test(main.CurrentChar(y,x+l," ",emeta))
		try:
			p.test(main.CurrentChar(y,x+l+1," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_line(self):
		r = self.do_render(4,2,4)
		self.assertEquals(1,len(r))
		self.assertTrue(isinstance(r[0],core.Line))
	
	def test_render_coordinates(self):
		l = self.do_render(4,2,6)[0]
		self.assertEquals((4,2.5),l.a)
		self.assertEquals((10,2.5),l.b)
		
	def test_render_coordinates_longer(self):
		l = self.do_render(5,1,8)[0]
		self.assertEquals((5,1.5),l.a)
		self.assertEquals((13,1.5),l.b)
	
	def test_render_coordinates_shorter(self):
		l = self.do_render(6,3,4)[0]
		self.assertEquals((6,3.5),l.a)
		self.assertEquals((10,3.5),l.b)

	def test_render_coordinates_box_start(self):
		l = self.do_render(4,2,6,smeta=core.M_BOX_AFTER_E)[0]
		self.assertEquals((3.5,2.5),l.a)
		self.assertEquals((10,2.5),l.b)
		
	def test_render_coordinates_box_end(self):
		l = self.do_render(4,2,6,emeta=core.M_BOX_START_E)[0]
		self.assertEquals((4,2.5),l.a)
		self.assertEquals((10.5,2.5),l.b)
		
	def test_render_coordinates_box_start_and_end(self):
		l = self.do_render(4,2,6,smeta=core.M_BOX_AFTER_E,emeta=core.M_BOX_START_E)[0]
		self.assertEquals((3.5,2.5),l.a)
		self.assertEquals((10.5,2.5),l.b)

	def test_render_z(self):
		l = self.do_render(3,3,4)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3,4)[0]
		self.assertEquals(core.C_FOREGROUND,l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3,4)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3,4)[0]
		self.assertEquals(core.STROKE_DASHED,l.stype)	


class TestLineSqCornerPattern(unittest.TestCase,PatternTests):

	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.LineSqCornerPattern
		
	def test_accepts_corner(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"+",core.M_LINE_AFTER_E))
		feed_input(p,0,4," \n")
		feed_input(p,1,0,"  ")
		p.test(main.CurrentChar(1,2,"|",core.M_LINE_START_S))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_expects_plus_sign(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"?",core.M_LINE_AFTER_E))
	
	def test_expects_plus_sign_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"+",core.M_OCCUPIED))
	
	def test_allows_rest_of_first_line(self):
		p = self.pclass()
		feed_input(p,0,2,"+")
		p.test(main.CurrentChar(0,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,4,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,5,"\n",core.M_OCCUPIED))
		
	def test_allows_occupied_second_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"+",core.M_LINE_AFTER_E))
		feed_input(p,0,3,"\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,2,"c",core.M_OCCUPIED|core.M_LINE_START_S))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3,"d",core.M_OCCUPIED))
			
	def test_rejects_zero_lines(self):
		p = self.pclass()
		feed_input(p,0,2,  "+ \n")
		feed_input(p,1,0,"   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_rejects_single_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+ \n")
		feed_input(p,1,0,"  ")
		p.test(main.CurrentChar(1,2,"|",core.M_LINE_START_S))
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
	
	def test_allows_northwest_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"+",core.M_LINE_AFTER_SE))
		feed_input(p,0,3,   " \n")
		feed_input(p,1,0,"  ")
		p.test(main.CurrentChar(1,2,"|",core.M_LINE_START_S))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_allows_north_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"+",core.M_LINE_AFTER_S))
		feed_input(p,0,3,   " \n")
		feed_input(p,1,0,"  ")
		p.test(main.CurrentChar(1,2,"|",core.M_LINE_START_S))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
	
	def test_allows_northeast_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"+",core.M_LINE_AFTER_SW))
		feed_input(p,0,3,   " \n")
		feed_input(p,1,0,"  ")
		p.test(main.CurrentChar(1,2,"|",core.M_LINE_START_S))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_allows_west_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"+",core.M_LINE_AFTER_E))
		feed_input(p,0,3,   " \n")
		feed_input(p,1,0,"  ")
		p.test(main.CurrentChar(1,2,"|",core.M_LINE_START_S))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_allows_east_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"+",core.M_NONE))
		p.test(main.CurrentChar(0,3,"-",core.M_LINE_START_E))
		feed_input(p,0,4,"\n")
		feed_input(p,1,0,"  ")
		p.test(main.CurrentChar(1,2,"|",core.M_LINE_START_S))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
		
	def test_allows_southwest_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+ \n")
		feed_input(p,1,0," ")
		p.test(main.CurrentChar(1,1,"/",core.M_LINE_START_SW))
		p.test(main.CurrentChar(1,2,"|",core.M_LINE_START_S))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_allows_southeast_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+ \n")
		feed_input(p,1,0,"  ")
		p.test(main.CurrentChar(1,2,"|",core.M_LINE_START_S))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3,"\\",core.M_LINE_START_SE)) 	
	
	def test_allows_more_than_two_lines(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"+",core.M_LINE_AFTER_SE|core.M_LINE_AFTER_SW))
		feed_input(p,0,1," \n")
		feed_input(p,1,0," ")
		p.test(main.CurrentChar(1,1,"/",core.M_LINE_START_SW))
		feed_input(p,1,2," ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3,"\\",core.M_LINE_START_SE))

	def test_ignores_line_characters(self):
		p = self.pclass()
		feed_input(p,0,2,"+")
		p.test(main.CurrentChar(0,3,"Z",core.M_LINE_START_E))
		feed_input(p,0,4,"\n")
		feed_input(p,1,0,"   ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3,"Q",core.M_LINE_START_SE))
	
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((2,  "+ \n"),
				 (0,"  |"  ))
		w = core.M_LINE_AFTER_E
		s = core.M_LINE_START_S
		n = core.M_NONE
		o = core.M_OCCUPIED
		inmeta = ((    w,n,n,),
				  (n,n,s,  ))
		outmeta =((    o,n,n,),
				  (n,n,n,  ))
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				im = inmeta[j][i]
				om = outmeta[j][i]
				self.assertEquals(om,p.test(main.CurrentChar(j,startcol+i,char,im)))		
			
	def do_render(self,x,y,lines):
		p = self.pclass()
		p.test(main.CurrentChar(y,x,"+",lines & (core.M_LINE_AFTER_E|core.M_LINE_AFTER_S
				|core.M_LINE_AFTER_SW|core.M_LINE_AFTER_SE|core.M_DASH_AFTER_E
				|core.M_DASH_AFTER_S|core.M_DASH_AFTER_SW|core.M_DASH_AFTER_SE)))
		p.test(main.CurrentChar(y,x+1," ",lines & (core.M_LINE_START_E|core.M_DASH_START_E)))
		p.test(main.CurrentChar(y,x+2,"\n",core.M_NONE))
		feed_input(p,y+1,0," "*(x-1))
		p.test(main.CurrentChar(y+1,x-1," ",lines & (core.M_LINE_START_SW|core.M_DASH_START_SW)))
		p.test(main.CurrentChar(y+1,x," ",lines & (core.M_LINE_START_S|core.M_DASH_START_S)))
		try:
			p.test(main.CurrentChar(y+1,x+1," ",lines & (core.M_LINE_START_SE|core.M_DASH_START_SE)))
		except StopIteration: pass
		return p.render()
				
	def test_render_returns_lines(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_S|core.M_LINE_START_E)
		for shape in r:
			self.assertTrue( isinstance(shape,core.Line) )
			
	def test_render_returns_two_lines_for_two_directions_(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_S|core.M_LINE_START_E)
		self.assertEquals(2, len(r))
		
	def test_render_returns_six_lines_for_six_directions(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_S|core.M_LINE_START_E|core.M_LINE_START_SE
				|core.M_LINE_AFTER_SE|core.M_LINE_AFTER_E|core.M_LINE_START_SW)
		self.assertEquals(6, len(r))
	
	def test_render_coordinates_northwest(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_SE)
		l = self.find_with(r,"b",(2,2))
		self.assertEquals((2.5,2.5),l.a)
		
	def test_render_coordinates_north(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_S)
		l = self.find_with(r,"b",(2.5,2))
		self.assertEquals((2.5,2.5),l.a)
		
	def test_render_coordinates_northeast(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_SW)
		l = self.find_with(r,"b",(3,2))
		self.assertEquals((2.5,2.5),l.a)
		
	def test_render_coordinates_east(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_START_E)
		l = self.find_with(r,"b",(3,2.5))
		self.assertEquals((2.5,2.5),l.a)
		
	def test_render_coordinates_southeast(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_START_SE)
		l = self.find_with(r,"b",(3,3))
		self.assertEquals((2.5,2.5),l.a)
		
	def test_render_coordinates_south(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_START_S)
		l = self.find_with(r,"b",(2.5,3))
		self.assertEquals((2.5,2.5),l.a)
		
	def test_render_coordinates_southwest(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_START_SW)
		l = self.find_with(r,"b",(2,3))
		self.assertEquals((2.5,2.5),l.a)
		
	def test_render_coordinates_west(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_S)
		l = self.find_with(r,"b",(2,2.5))
		self.assertEquals((2.5,2.5),l.a)
		
	def test_render_coordinates_position(self):
		r = self.do_render(4,6,core.M_LINE_AFTER_E|core.M_LINE_AFTER_S)
		l1 = self.find_with(r,"b",(4,6.5))
		self.assertEquals((4.5,6.5),l1.a)
		l2 = self.find_with(r,"b",(4.5,6))
		self.assertEquals((4.5,6.5),l2.a)	
	
	def test_render_z(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_S)
		for shape in r:
			self.assertEquals(0,shape.z)
	
	def test_render_stroke_colour(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_S)
		for shape in r:
			self.assertEquals(core.C_FOREGROUND,shape.stroke)
			
	def test_render_stroke_width(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_S)
		for shape in r:
			self.assertEquals(1,shape.w)
			
	def test_render_stroke_style_solid(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_S)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)
			
	def test_render_stroke_type_dashed(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_DASH_AFTER_E
				|core.M_LINE_AFTER_S|core.M_DASH_AFTER_S)
		for shape in r:
			self.assertEquals(core.STROKE_DASHED,shape.stype)
			
	def test_render_stroke_types_mixed(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_DASH_AFTER_E
				|core.M_LINE_AFTER_S)
		l1 = self.find_with(r,"b",(2,2.5))
		self.assertEquals(core.STROKE_DASHED,l1.stype)
		l2 = self.find_with(r,"b",(2.5,2))
		self.assertEquals(core.STROKE_SOLID,l2.stype)
		
	
class TestLineRdCornerPattern(unittest.TestCase,PatternTests):

	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.LineRdCornerPattern
		
	def test_accepts_corner(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,".",core.M_LINE_AFTER_E))
		feed_input(p,0,4," \n")
		feed_input(p,1,0,"  ")
		p.test(main.CurrentChar(1,2,"|",core.M_LINE_START_S))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
	
	def test_expects_period(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"?",core.M_LINE_AFTER_E))
	
	def test_expects_period_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,".",core.M_OCCUPIED))
			
	def test_allows_apostraphe(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"'",core.M_NONE))
		
	def test_rejects_apostraphe_occupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"'",core.M_OCCUPIED))
		
	def test_allows_colon(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,":",core.M_NONE))
		
	def test_rejects_colon_occupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,":",core.M_OCCUPIED))
			
	def test_allows_rest_of_first_line(self):
		p = self.pclass()
		feed_input(p,0,2,".")
		p.test(main.CurrentChar(0,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,4,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,5,"\n",core.M_OCCUPIED))
		
	def test_allows_occupied_second_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,".",core.M_LINE_AFTER_E))
		feed_input(p,0,3,"\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,2,"c",core.M_OCCUPIED|core.M_LINE_START_S))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3,"d",core.M_OCCUPIED))
			
	def test_rejects_zero_lines(self):
		p = self.pclass()
		feed_input(p,0,2,  ". \n")
		feed_input(p,1,0,"   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_rejects_single_line(self):
		p = self.pclass()
		feed_input(p,0,2,  ". \n")
		feed_input(p,1,0,"  ")
		p.test(main.CurrentChar(1,2,"|",core.M_LINE_START_S))
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
	
	def test_allows_northwest_line_with_apostraphe(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"'",core.M_LINE_AFTER_SE|core.M_LINE_AFTER_E))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
			
	def test_allows_northwest_line_with_colon(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,":",core.M_LINE_AFTER_SE|core.M_LINE_AFTER_E))
		feed_input(p,0,3," ")
		feed_input(p,1,0,"   ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_rejects_northwest_line_with_period(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,".",core.M_LINE_AFTER_SE|core.M_LINE_AFTER_E))
		feed_input(p,0,3," ")
		feed_input(p,1,0,"   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_allows_north_line_with_apostraphe(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"'",core.M_LINE_AFTER_S|core.M_LINE_AFTER_E))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
			
	def test_allows_north_line_with_colon(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,":",core.M_LINE_AFTER_S|core.M_LINE_AFTER_E))
		feed_input(p,0,3," ")
		feed_input(p,1,0,"   ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_rejects_north_line_with_period(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,".",core.M_LINE_AFTER_S|core.M_LINE_AFTER_E))
		feed_input(p,0,3," ")
		feed_input(p,1,0,"   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_allows_northeast_line_with_apostraphe(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"'",core.M_LINE_AFTER_SW|core.M_LINE_AFTER_E))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
			
	def test_allows_northeast_line_with_colon(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,":",core.M_LINE_AFTER_SW|core.M_LINE_AFTER_E))
		feed_input(p,0,3," ")
		feed_input(p,1,0,"   ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_rejects_northeast_line_with_period(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,".",core.M_LINE_AFTER_SW|core.M_LINE_AFTER_E))
		feed_input(p,0,3," ")
		feed_input(p,1,0,"   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_allows_east_line_with_apostraphe(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"'",core.M_LINE_AFTER_E))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,3,"-",core.M_LINE_START_E))
		
	def test_allows_east_line_with_colon(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,":",core.M_LINE_AFTER_E))
		p.test(main.CurrentChar(0,3,"-",core.M_LINE_START_E))
		feed_input(p,1,0,"   ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_allows_east_line_with_period(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,".",core.M_LINE_AFTER_E))
		p.test(main.CurrentChar(0,3,"-",core.M_LINE_START_E))
		feed_input(p,1,0,"   ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_rejects_southeast_line_with_apostraphe(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"'",core.M_LINE_AFTER_E))
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
			
	def test_allows_southeast_line_with_colon(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,":",core.M_LINE_AFTER_E))
		feed_input(p,0,3," ")
		feed_input(p,1,0,"   ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3,"\\",core.M_LINE_START_SE))
			
	def test_allows_southeast_line_with_period(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,".",core.M_LINE_AFTER_E))
		feed_input(p,0,3," ")
		feed_input(p,1,0,"   ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3,"\\",core.M_LINE_START_SE))
			
	def test_rejects_south_line_with_apostraphe(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"'",core.M_LINE_AFTER_E))
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
			
	def test_allows_south_line_with_colon(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,":",core.M_LINE_AFTER_E))
		feed_input(p,0,3," ")
		feed_input(p,1,0,"  ")
		p.test(main.CurrentChar(1,2,"|",core.M_LINE_START_S))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_allows_south_line_with_period(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,".",core.M_LINE_AFTER_E))
		feed_input(p,0,3," ")
		feed_input(p,1,0,"  ")
		p.test(main.CurrentChar(1,2,"|",core.M_LINE_START_S))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_rejects_southwest_line_with_apostraphe(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"'",core.M_LINE_AFTER_E))
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
			
	def test_allows_southwest_line_with_colon(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,":",core.M_LINE_AFTER_E))
		feed_input(p,0,3," ")
		feed_input(p,1,0," ")
		p.test(main.CurrentChar(1,1,"/",core.M_LINE_START_SW))
		feed_input(p,1,2," ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_allows_southwest_line_with_period(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,".",core.M_LINE_AFTER_E))
		feed_input(p,0,3," ")
		feed_input(p,1,0," ")
		p.test(main.CurrentChar(1,1,"/",core.M_LINE_START_SW))
		feed_input(p,1,2," ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_allows_more_than_two_lines(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,":",core.M_LINE_AFTER_SE|core.M_LINE_AFTER_SW))
		feed_input(p,0,1," \n")
		feed_input(p,1,0," ")
		p.test(main.CurrentChar(1,1,"/",core.M_LINE_START_SW))
		feed_input(p,1,2," ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3,"\\",core.M_LINE_START_SE))
	
	def test_ignores_line_characters(self):
		p = self.pclass()
		feed_input(p,0,2,".")
		p.test(main.CurrentChar(0,3,"Z",core.M_LINE_START_E))
		feed_input(p,0,4,"\n")
		feed_input(p,1,0,"   ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3,"Q",core.M_LINE_START_SE))
	
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((2,  ". \n"),
				 (0,"  |"  ))
		w = core.M_LINE_AFTER_E
		s = core.M_LINE_START_S
		n = core.M_NONE
		o = core.M_OCCUPIED
		inmeta = ((    w,n,n,),
				  (n,n,s,  ))
		outmeta =((    o,n,n,),
				  (n,n,n,  ))
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				im = inmeta[j][i]
				om = outmeta[j][i]
				self.assertEquals(om,p.test(main.CurrentChar(j,startcol+i,char,im)))		
	
	def do_render(self,x,y,lines):
		p = self.pclass()
		p.test(main.CurrentChar(y,x,":",lines & (core.M_LINE_AFTER_E|core.M_LINE_AFTER_S
				|core.M_LINE_AFTER_SW|core.M_LINE_AFTER_SE|core.M_DASH_AFTER_E
				|core.M_DASH_AFTER_S|core.M_DASH_AFTER_SW|core.M_DASH_AFTER_SE)))
		p.test(main.CurrentChar(y,x+1," ",lines & (core.M_LINE_START_E|core.M_DASH_START_E)))
		p.test(main.CurrentChar(y,x+2,"\n",core.M_NONE))
		feed_input(p,y+1,0," "*(x-1))
		p.test(main.CurrentChar(y+1,x-1," ",lines & (core.M_LINE_START_SW|core.M_DASH_START_SW)))
		p.test(main.CurrentChar(y+1,x," ",lines & (core.M_LINE_START_S|core.M_DASH_START_S)))
		try:
			p.test(main.CurrentChar(y+1,x+1," ",lines & (core.M_LINE_START_SE|core.M_DASH_START_SE)))
		except StopIteration: pass
		return p.render()
				
	def test_render_returns_quad_curves(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_S|core.M_LINE_START_E)
		for shape in r:
			self.assertTrue( isinstance(shape,core.QuadCurve) )
	
	def test_render_returns_one_curve_for_two_directions(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_S|core.M_LINE_START_E)
		self.assertEquals(1, len(r))
	
	def test_render_returns_fifteen_curves_for_six_directions(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_S|core.M_LINE_START_E|core.M_LINE_START_SE
				|core.M_LINE_AFTER_SE|core.M_LINE_AFTER_E|core.M_LINE_START_SW)
		self.assertEquals(15, len(r))
	
	def test_render_coordinates_northwest(self):
		l = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_SE)[0]
		self.assertEquals((2,2.5),l.a)
		self.assertEquals((2,2),l.b)
		self.assertEquals((2.5,2.5),l.c)
		
	def test_render_coordinates_north(self):
		l = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_S)[0]
		self.assertEquals((2,2.5),l.a)
		self.assertEquals((2.5,2),l.b)
		self.assertEquals((2.5,2.5),l.c)
	
	def test_render_coordinates_northeast(self):
		l = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_SW)[0]
		self.assertEquals((2,2.5),l.a)
		self.assertEquals((3,2),l.b)
		self.assertEquals((2.5,2.5),l.c)
		
	def test_render_coordinates_east(self):
		l = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_START_E)[0]
		self.assertEquals((2,2.5),l.a)
		self.assertEquals((3,2.5),l.b)
		self.assertEquals((2.5,2.5),l.c)
		
	def test_render_coordinates_southeast(self):
		l = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_START_SE)[0]
		self.assertEquals((2,2.5),l.a)
		self.assertEquals((3,3),l.b)
		self.assertEquals((2.5,2.5),l.c)
	
	def test_render_coordinates_south(self):
		l = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_START_S)[0]
		self.assertEquals((2,2.5),l.a)
		self.assertEquals((2.5,3),l.b)
		self.assertEquals((2.5,2.5),l.c)
		
	def test_render_coordinates_southwest(self):
		l = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_START_SW)[0]
		self.assertEquals((2,2.5),l.a)
		self.assertEquals((2,3),l.b)
		self.assertEquals((2.5,2.5),l.c)
	
	def test_render_coordinates_west(self):
		l = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_S)[0]
		self.assertEquals((2,2.5),l.a)
		self.assertEquals((2.5,2),l.b)
		self.assertEquals((2.5,2.5),l.c)
		
	def test_render_coordinates_position(self):
		l = self.do_render(4,6,core.M_LINE_AFTER_E|core.M_LINE_AFTER_S)[0]
		self.assertEquals((4,6.5),l.a)
		self.assertEquals((4.5,6),l.b)	
		self.assertEquals((4.5,6.5),l.c)	
	
	def test_render_z(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_S)
		for shape in r:
			self.assertEquals(0,shape.z)
	
	def test_render_stroke_colour(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_S)
		for shape in r:
			self.assertEquals(core.C_FOREGROUND,shape.stroke)
			
	def test_render_stroke_width(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_S)
		for shape in r:
			self.assertEquals(1,shape.w)
			
	def test_render_stroke_style_solid(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_S)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)
			
	def test_render_stroke_type_dashed(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_DASH_AFTER_E
				|core.M_LINE_AFTER_S|core.M_DASH_AFTER_S)
		for shape in r:
			self.assertEquals(core.STROKE_DASHED,shape.stype)
			
	def test_render_stroke_types_mixed(self):
		l = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_DASH_AFTER_E
				|core.M_LINE_AFTER_S)[0]
		self.assertEquals(core.STROKE_SOLID,l.stype)		


class TestLJumpPattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.LJumpPattern	
		
	def test_accepts_jump(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"(",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S))
		p.test(main.CurrentChar(0,3,"-",core.M_LINE_START_E))
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2,"|",core.M_LINE_START_S))
	
	def test_expects_left_paren(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"Q",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S))
		
	def test_expects_left_paren_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"(",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S
					|core.M_OCCUPIED))
					
	def test_expects_north_line_meta(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"(",core.M_LINE_AFTER_E))
			
	def test_expects_west_line_meta(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"(",core.M_LINE_AFTER_S))
			
	def test_expects_east_line_meta(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"(",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S))
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"-",core.M_OCCUPIED))
			
	def test_expects_south_line_meta(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"(",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S))
		p.test(main.CurrentChar(0,3,"-",core.M_LINE_START_E|core.M_OCCUPIED))
		feed_input(p,1,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"|",core.M_OCCUPIED))
			
	def test_ignores_line_characters(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"(",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S))
		p.test(main.CurrentChar(0,3,"Q",core.M_LINE_START_E|core.M_OCCUPIED))
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2,"Z",core.M_LINE_START_S|core.M_OCCUPIED))
			
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((2,  "(- \n"),
				 (0,"  "     ),)
		c = core.M_LINE_AFTER_E|core.M_LINE_AFTER_S
		e = core.M_LINE_START_E
		n = core.M_NONE
		o = core.M_OCCUPIED
		metain = ((    c,e,n,n,),
				  (n,n,        ),)
		metaout = ((   o,n,n,n,),
				  (n,n,        ),)
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				mi = metain[j][i]
				mo = metaout[j][i]
				self.assertEquals(mo,p.test(main.CurrentChar(j,startcol+i,char,mi)))
	
	def do_render(self,x,y,dashes):
		p = self.pclass()
		p.test(main.CurrentChar(y,x,"(",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S
				|(dashes & (core.M_DASH_AFTER_E|core.M_DASH_AFTER_S))))
		p.test(main.CurrentChar(y,x+1,"-",core.M_LINE_START_E
				| (dashes & core.M_DASH_START_E)))
		feed_input(p,y+1,0," "*x)
		try:
			p.test(main.CurrentChar(y+1,x,"|",core.M_LINE_START_S
				| (dashes & core.M_DASH_START_S)))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_correct_shapes(self):
		r = self.do_render(3,2,core.M_NONE)
		self.assertEquals(2,len(r))
		self.assertEquals(1,len(self.find_type(r,core.Line)))
		self.assertEquals(1,len(self.find_type(r,core.Arc)))
		
	def test_render_coordinates(self):
		r = self.do_render(3,2,core.M_NONE)
		l = self.find_type(r,core.Line)[0]
		self.assertEquals((3,2.5),l.a)
		self.assertEquals((4,2.5),l.b)
		a = self.find_type(r,core.Arc)[0]
		self.assertEquals((2.9,2),a.a)
		self.assertEquals((4.1,3),a.b)
		self.assertEquals(math.pi/2,a.start)
		self.assertEquals(math.pi/2*3,a.end)
	
	def test_render_coorinates_position(self):
		r = self.do_render(6,5,core.M_NONE)
		l = self.find_type(r,core.Line)[0]
		self.assertEquals((6,5.5),l.a)
		self.assertEquals((7,5.5),l.b)
		a = self.find_type(r,core.Arc)[0]
		self.assertEquals((5.9,5),a.a)
		self.assertEquals((7.1,6),a.b)
		self.assertEquals(math.pi/2,a.start)
		self.assertEquals(math.pi/2*3,a.end)
		
	def test_render_z(self):
		r = self.do_render(3,2,core.M_NONE)
		for shape in r:
			self.assertEquals(0,shape.z)
			
	def test_render_stroke_colour(self):
		r = self.do_render(3,2,core.M_NONE)
		for shape in r:
			self.assertEquals(core.C_FOREGROUND,shape.stroke)
			
	def test_render_stroke_width(self):
		r = self.do_render(3,2,core.M_NONE)
		for shape in r:
			self.assertEquals(1,shape.w)
			
	def test_render_stroke_style_solid(self):
		r = self.do_render(3,2,core.M_NONE)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)

	def test_render_stroke_style_dashed(self):
		r = self.do_render(3,2,core.M_DASH_AFTER_E|core.M_DASH_AFTER_S
				|core.M_DASH_START_E|core.M_DASH_START_S)
		for shape in r:
			self.assertEquals(core.STROKE_DASHED,shape.stype)
			
	def test_render_stroke_style_mixed(self):
		r = self.do_render(3,2,core.M_DASH_AFTER_E|core.M_DASH_AFTER_S)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)
			
	def test_render_fill_colour(self):
		a = self.find_type(self.do_render(3,2,core.M_NONE),core.Arc)[0]
		self.assertEquals(None,a.fill)

	
class TestRJumpPattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.RJumpPattern	
		
	def test_accepts_jump(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,")",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S))
		p.test(main.CurrentChar(0,3,"-",core.M_LINE_START_E))
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2,"|",core.M_LINE_START_S))
	
	def test_expects_right_paren(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"Q",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S))
		
	def test_expects_right_paren_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,")",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S
					|core.M_OCCUPIED))
					
	def test_expects_north_line_meta(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,")",core.M_LINE_AFTER_E))
			
	def test_expects_west_line_meta(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,")",core.M_LINE_AFTER_S))
			
	def test_expects_east_line_meta(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,")",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S))
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"-",core.M_OCCUPIED))
			
	def test_expects_south_line_meta(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,")",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S))
		p.test(main.CurrentChar(0,3,"-",core.M_LINE_START_E|core.M_OCCUPIED))
		feed_input(p,1,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"|",core.M_OCCUPIED))
			
	def test_ignores_line_characters(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,")",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S))
		p.test(main.CurrentChar(0,3,"Q",core.M_LINE_START_E|core.M_OCCUPIED))
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2,"Z",core.M_LINE_START_S|core.M_OCCUPIED))
			
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((2,  ")- \n"),
				 (0,"  "     ),)
		c = core.M_LINE_AFTER_E|core.M_LINE_AFTER_S
		e = core.M_LINE_START_E
		n = core.M_NONE
		o = core.M_OCCUPIED
		metain = ((    c,e,n,n,),
				  (n,n,        ),)
		metaout = ((   o,n,n,n,),
				  (n,n,        ),)
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				mi = metain[j][i]
				mo = metaout[j][i]
				self.assertEquals(mo,p.test(main.CurrentChar(j,startcol+i,char,mi)))
	
	def do_render(self,x,y,dashes):
		p = self.pclass()
		p.test(main.CurrentChar(y,x,")",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S
				|(dashes & (core.M_DASH_AFTER_E|core.M_DASH_AFTER_S))))
		p.test(main.CurrentChar(y,x+1,"-",core.M_LINE_START_E
				| (dashes & core.M_DASH_START_E)))
		feed_input(p,y+1,0," "*x)
		try:
			p.test(main.CurrentChar(y+1,x,"|",core.M_LINE_START_S
				| (dashes & core.M_DASH_START_S)))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_correct_shapes(self):
		r = self.do_render(3,2,core.M_NONE)
		self.assertEquals(2,len(r))
		self.assertEquals(1,len(self.find_type(r,core.Line)))
		self.assertEquals(1,len(self.find_type(r,core.Arc)))
		
	def test_render_coordinates(self):
		r = self.do_render(3,2,core.M_NONE)
		l = self.find_type(r,core.Line)[0]
		self.assertEquals((3,2.5),l.a)
		self.assertEquals((4,2.5),l.b)
		a = self.find_type(r,core.Arc)[0]
		self.assertEquals((2.9,2),a.a)
		self.assertEquals((4.1,3),a.b)
		self.assertEquals(-math.pi/2,a.start)
		self.assertEquals(math.pi/2,a.end)
	
	def test_render_coorinates_position(self):
		r = self.do_render(6,5,core.M_NONE)
		l = self.find_type(r,core.Line)[0]
		self.assertEquals((6,5.5),l.a)
		self.assertEquals((7,5.5),l.b)
		a = self.find_type(r,core.Arc)[0]
		self.assertEquals((5.9,5),a.a)
		self.assertEquals((7.1,6),a.b)
		self.assertEquals(-math.pi/2,a.start)
		self.assertEquals(math.pi/2,a.end)
		
	def test_render_z(self):
		r = self.do_render(3,2,core.M_NONE)
		for shape in r:
			self.assertEquals(0,shape.z)
			
	def test_render_stroke_colour(self):
		r = self.do_render(3,2,core.M_NONE)
		for shape in r:
			self.assertEquals(core.C_FOREGROUND,shape.stroke)
			
	def test_render_stroke_width(self):
		r = self.do_render(3,2,core.M_NONE)
		for shape in r:
			self.assertEquals(1,shape.w)
			
	def test_render_stroke_style_solid(self):
		r = self.do_render(3,2,core.M_NONE)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)

	def test_render_stroke_style_dashed(self):
		r = self.do_render(3,2,core.M_DASH_AFTER_E|core.M_DASH_AFTER_S
				|core.M_DASH_START_E|core.M_DASH_START_S)
		for shape in r:
			self.assertEquals(core.STROKE_DASHED,shape.stype)
			
	def test_render_stroke_style_mixed(self):
		r = self.do_render(3,2,core.M_DASH_AFTER_E|core.M_DASH_AFTER_S)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)
			
	def test_render_fill_colour(self):
		a = self.find_type(self.do_render(3,2,core.M_NONE),core.Arc)[0]
		self.assertEquals(None,a.fill)	
	
	
class TestUJumpPattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.UJumpPattern	
		
	def test_accepts_jump(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"^",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S))
		p.test(main.CurrentChar(0,3,"-",core.M_LINE_START_E))
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2,"|",core.M_LINE_START_S))
	
	def test_expects_caret(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"Q",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S))
		
	def test_expects_caret_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"^",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S
					|core.M_OCCUPIED))
					
	def test_expects_north_line_meta(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"^",core.M_LINE_AFTER_E))
			
	def test_expects_west_line_meta(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"^",core.M_LINE_AFTER_S))
			
	def test_expects_east_line_meta(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"^",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S))
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"-",core.M_OCCUPIED))
			
	def test_expects_south_line_meta(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"^",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S))
		p.test(main.CurrentChar(0,3,"-",core.M_LINE_START_E|core.M_OCCUPIED))
		feed_input(p,1,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"|",core.M_OCCUPIED))
			
	def test_ignores_line_characters(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"^",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S))
		p.test(main.CurrentChar(0,3,"Q",core.M_LINE_START_E|core.M_OCCUPIED))
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2,"Z",core.M_LINE_START_S|core.M_OCCUPIED))
			
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((2,  "^- \n"),
				 (0,"  "     ),)
		c = core.M_LINE_AFTER_E|core.M_LINE_AFTER_S
		e = core.M_LINE_START_E
		n = core.M_NONE
		o = core.M_OCCUPIED
		metain = ((    c,e,n,n,),
				  (n,n,        ),)
		metaout = ((   o,n,n,n,),
				  (n,n,        ),)
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				mi = metain[j][i]
				mo = metaout[j][i]
				self.assertEquals(mo,p.test(main.CurrentChar(j,startcol+i,char,mi)))
	
	def do_render(self,x,y,dashes):
		p = self.pclass()
		p.test(main.CurrentChar(y,x,"^",core.M_LINE_AFTER_E|core.M_LINE_AFTER_S
				|(dashes & (core.M_DASH_AFTER_E|core.M_DASH_AFTER_S))))
		p.test(main.CurrentChar(y,x+1,"-",core.M_LINE_START_E
				| (dashes & core.M_DASH_START_E)))
		feed_input(p,y+1,0," "*x)
		try:
			p.test(main.CurrentChar(y+1,x,"|",core.M_LINE_START_S
				| (dashes & core.M_DASH_START_S)))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_correct_shapes(self):
		r = self.do_render(3,2,core.M_NONE)
		self.assertEquals(2,len(r))
		self.assertEquals(1,len(self.find_type(r,core.Line)))
		self.assertEquals(1,len(self.find_type(r,core.Arc)))
		
	def test_render_coordinates(self):
		r = self.do_render(3,2,core.M_NONE)
		l = self.find_type(r,core.Line)[0]
		self.assertEquals((3.5,2),l.a)
		self.assertEquals((3.5,3),l.b)
		a = self.find_type(r,core.Arc)[0]
		self.assertEquals((3,2.1),a.a)
		self.assertEquals((4,2.9),a.b)
		self.assertEquals(math.pi/2*2,a.start)
		self.assertEquals(math.pi/2*4,a.end)
	
	def test_render_coorinates_position(self):
		r = self.do_render(6,5,core.M_NONE)
		l = self.find_type(r,core.Line)[0]
		self.assertEquals((6.5,5),l.a)
		self.assertEquals((6.5,6),l.b)
		a = self.find_type(r,core.Arc)[0]
		self.assertEquals((6,5.1),a.a)
		self.assertEquals((7,5.9),a.b)
		self.assertEquals(math.pi/2*2,a.start)
		self.assertEquals(math.pi/2*4,a.end)
		
	def test_render_z(self):
		r = self.do_render(3,2,core.M_NONE)
		for shape in r:
			self.assertEquals(0,shape.z)
			
	def test_render_stroke_colour(self):
		r = self.do_render(3,2,core.M_NONE)
		for shape in r:
			self.assertEquals(core.C_FOREGROUND,shape.stroke)
			
	def test_render_stroke_width(self):
		r = self.do_render(3,2,core.M_NONE)
		for shape in r:
			self.assertEquals(1,shape.w)
			
	def test_render_stroke_style_solid(self):
		r = self.do_render(3,2,core.M_NONE)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)

	def test_render_stroke_style_dashed(self):
		r = self.do_render(3,2,core.M_DASH_AFTER_E|core.M_DASH_AFTER_S
				|core.M_DASH_START_E|core.M_DASH_START_S)
		for shape in r:
			self.assertEquals(core.STROKE_DASHED,shape.stype)
			
	def test_render_stroke_style_mixed(self):
		r = self.do_render(3,2,core.M_DASH_AFTER_E|core.M_DASH_AFTER_S)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)
			
	def test_render_fill_colour(self):
		a = self.find_type(self.do_render(3,2,core.M_NONE),core.Arc)[0]
		self.assertEquals(None,a.fill)		


if __name__ == "__main__":
	unittest.main()
