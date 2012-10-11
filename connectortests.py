#!/usr/bin/python2

import unittest
import core
import main
import patterns

from ptests import *


class TestLArrowheadPattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.LArrowheadPattern
		
	def test_accepts_arrowhead(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"<",core.M_NONE))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,3,"-",core.M_LINE_START_E))
	
	def test_expects_left_angle_bracket(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"?",core.M_NONE))
			
	def test_expects_left_angle_bracket_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"<",core.M_OCCUPIED))
			
	def test_expects_east_line_meta(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"<",core.M_NONE))
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"-",core.M_NONE))
			
	def test_allows_occupied_east_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"<",core.M_NONE))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,3,"-",core.M_OCCUPIED|core.M_LINE_START_E))
			
	def test_allows_box_right_meta(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"<",core.M_BOX_AFTER_E))
		
	def test_allows_dashed_east_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"<",core.M_NONE))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,3,"-",core.M_LINE_START_E|core.M_DASH_START_E))

	def test_doesnt_error_at_top_left_corner(self):
		p = self.pclass()
		try:
			p.test(main.CurrentChar(-1,0,core.START_OF_INPUT,core.M_NONE))
		except core.PatternRejected: pass
	
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		self.assertEquals(core.M_OCCUPIED, p.test(main.CurrentChar(0,2,"<",core.M_NONE)))
		
	def do_render(self,x,y,box,dashed):
		p = self.pclass()
		p.test(main.CurrentChar(y,x,"<",
				core.M_BOX_AFTER_E if box else core.M_NONE))
		try:
			p.test(main.CurrentChar(y,x+1,"-",core.M_LINE_START_E
					| (core.M_DASH_START_E if dashed else core.M_NONE)))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_correct_shapes(self):
		r = self.do_render(2,3,False,False)
		self.assertEquals(3,len(r))
		self.assertEquals(3,len(find_type(self,r,core.Line)))
		
	def test_render_coordinates(self):
		r = self.do_render(2,3,False,False)
		mid = find_with(self,r,"a",(3,3.5))
		self.assertEquals((2,3.5),mid.b)
		lft = find_with(self,r,"a",(2.8,3.25))
		self.assertEquals((2,3.5),lft.b)
		rgt = find_with(self,r,"a",(2.8,3.75))
		self.assertEquals((2,3.5),rgt.b)
		
	def test_render_coordinates_position(self):
		r = self.do_render(5,7,False,False)
		mid = find_with(self,r,"a",(6,7.5))
		self.assertEquals((5,7.5),mid.b)
		lft = find_with(self,r,"a",(5.8,7.25))
		self.assertEquals((5,7.5),lft.b)
		rgt = find_with(self,r,"a",(5.8,7.75))
		self.assertEquals((5,7.5),rgt.b)
	
	def test_render_coordinates_box(self):
		r = self.do_render(2,3,True,False)
		mid = find_with(self,r,"a",(3,3.5))
		self.assertEquals((1.5,3.5),mid.b)
		lft = find_with(self,r,"a",(2.3,3.25))
		self.assertEquals((1.5,3.5),lft.b)
		rgt = find_with(self,r,"a",(2.3,3.75))
		self.assertEquals((1.5,3.5),rgt.b)
		
	def test_render_z(self):
		r = self.do_render(2,3,False,False)
		for shape in r:
			self.assertEquals(0, shape.z)
			
	def test_render_stroke_colour(self):
		r = self.do_render(2,3,False,False)
		for shape in r:
			self.assertEquals(core.C_FOREGROUND,shape.stroke)
			
	def test_render_stroke_width(self):
		r = self.do_render(2,3,False,False)
		for shape in r:
			self.assertEquals(1,shape.w)
	
	def test_render_stroke_style_solid(self):
		r = self.do_render(2,3,False,False)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)
				
	def test_render_stoke_style_dashed(self):
		r = self.do_render(2,3,False,True)
		r.sort(lambda i,j: cmp(abs(i.b[0]-i.a[0]),abs(j.b[0]-j.a[0])),reverse=True)
		self.assertEquals(core.STROKE_DASHED, r[0].stype)
		self.assertEquals(core.STROKE_SOLID, r[1].stype)
		self.assertEquals(core.STROKE_SOLID, r[2].stype)


class TestRArrowheadPattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.RArrowheadPattern
		
	def test_accepts_arrowhead(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,">",core.M_LINE_AFTER_E))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
	
	def test_expects_right_angle_bracket(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"?",core.M_LINE_AFTER_E))
			
	def test_expects_right_angle_bracket_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,">",core.M_OCCUPIED|core.M_LINE_AFTER_E))
			
	def test_expects_west_line_meta(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,">",core.M_NONE))
			
	def test_allows_occupied_after(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,">",core.M_LINE_AFTER_E))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,3," ",core.M_OCCUPIED))
	
	def test_allows_box_left_meta(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,">",core.M_LINE_AFTER_E))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,3," ",core.M_BOX_START_E))
		
	def test_allows_dashed_west_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,">",core.M_LINE_AFTER_E|core.M_DASH_AFTER_E))
	
	def test_doesnt_error_at_top_left_corner(self):
		p = self.pclass()
		try:
			p.test(main.CurrentChar(-1,0,core.START_OF_INPUT,core.M_LINE_AFTER_E))
		except core.PatternRejected: pass
	
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		self.assertEquals(core.M_OCCUPIED, p.test(main.CurrentChar(0,2,">",core.M_LINE_AFTER_E)))
		
	def do_render(self,x,y,box,dashed):
		p = self.pclass()
		p.test(main.CurrentChar(y,x,">", core.M_LINE_AFTER_E
				| (core.M_DASH_AFTER_E if dashed else core.M_NONE)))
		try:
			p.test(main.CurrentChar(y,x+1," ",
					core.M_BOX_START_E if box else core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_correct_shapes(self):
		r = self.do_render(2,3,False,False)
		self.assertEquals(3,len(r))
		self.assertEquals(3,len(find_type(self,r,core.Line)))
		
	def test_render_coordinates(self):
		r = self.do_render(2,3,False,False)
		mid = find_with(self,r,"a",(2,3.5))
		self.assertEquals((3,3.5),mid.b)
		lft = find_with(self,r,"a",(2.2,3.25))
		self.assertEquals((3,3.5),lft.b)
		rgt = find_with(self,r,"a",(2.2,3.75))
		self.assertEquals((3,3.5),rgt.b)
		
	def test_render_coordinates_position(self):
		r = self.do_render(5,7,False,False)
		mid = find_with(self,r,"a",(5,7.5))
		self.assertEquals((6,7.5),mid.b)
		lft = find_with(self,r,"a",(5.2,7.25))
		self.assertEquals((6,7.5),lft.b)
		rgt = find_with(self,r,"a",(5.2,7.75))
		self.assertEquals((6,7.5),rgt.b)
	
	def test_render_coordinates_box(self):
		r = self.do_render(2,3,True,False)
		mid = find_with(self,r,"a",(2,3.5))
		self.assertEquals((3.5,3.5),mid.b)
		lft = find_with(self,r,"a",(2.7,3.25))
		self.assertEquals((3.5,3.5),lft.b)
		rgt = find_with(self,r,"a",(2.7,3.75))
		self.assertEquals((3.5,3.5),rgt.b)
	
	def test_render_z(self):
		r = self.do_render(2,3,False,False)
		for shape in r:
			self.assertEquals(0, shape.z)
			
	def test_render_stroke_colour(self):
		r = self.do_render(2,3,False,False)
		for shape in r:
			self.assertEquals(core.C_FOREGROUND,shape.stroke)
			
	def test_render_stroke_width(self):
		r = self.do_render(2,3,False,False)
		for shape in r:
			self.assertEquals(1,shape.w)
	
	def test_render_stroke_style_solid(self):
		r = self.do_render(2,3,False,False)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)
				
	def test_render_stoke_style_dashed(self):
		r = self.do_render(2,3,False,True)
		r.sort(lambda i,j: cmp(abs(i.b[0]-i.a[0]),abs(j.b[0]-j.a[0])),reverse=True)
		self.assertEquals(core.STROKE_DASHED, r[0].stype)
		self.assertEquals(core.STROKE_SOLID, r[1].stype)
		self.assertEquals(core.STROKE_SOLID, r[2].stype)


class TestUArrowheadPattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.UArrowheadPattern
		
	def test_accepts_arrowhead(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"^",core.M_NONE))
		feed_input(p,0,3,"\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2,"|",core.M_LINE_START_S))
	
	def test_expects_carent(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"?",core.M_NONE))
	
	def test_expects_caret_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"^",core.M_OCCUPIED) )
	
	def test_allows_rest_of_first_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"^",core.M_NONE))
		p.test(main.CurrentChar(0,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,4,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,5,"\n",core.M_OCCUPIED))
	
	def test_allows_start_of_second_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"^",core.M_NONE))
		feed_input(p,0,3,"\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
	
	def test_expects_south_line_meta(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"^",core.M_NONE))
		feed_input(p,0,3,"\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"|",core.M_NONE))
	
	def test_allows_box_south_meta(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"^",core.M_BOX_AFTER_S))
		
	def test_allows_dashed_south_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"^",core.M_NONE))
		feed_input(p,0,3,"\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2,"|",core.M_LINE_START_S|core.M_DASH_START_S))
	
	def test_doesnt_error_at_top_left_corner(self):
		p = self.pclass()
		try:
			p.test(main.CurrentChar(-1,0,core.START_OF_INPUT,core.M_NONE))
		except core.PatternRejected: pass
	
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((2,  "^ \n"),
				 (0,"  "    ),)
		n = core.M_NONE
		o = core.M_OCCUPIED
		inmeta = ((    n,n,n,),
				  (n,n,      ),)
		outmeta = ((   o,n,n,),
				   (n,n,     ),)  
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				im = inmeta[j][i]
				om = outmeta[j][i]
				self.assertEquals(om,p.test(main.CurrentChar(j,startcol+i,char,im)))
		
	def do_render(self,x,y,box,dashed):
		p = self.pclass()
		p.test(main.CurrentChar(y,x,"^",
				core.M_BOX_AFTER_S if box else core.M_NONE))
		feed_input(p,y,x+1,"\n")
		feed_input(p,y+1,0," "*x)
		try:
			p.test(main.CurrentChar(y+1,x,"|", core.M_LINE_START_S
					| (core.M_DASH_START_S if dashed else core.M_NONE)))
		except StopIteration: pass
		return p.render()
	
	def test_render_returns_correct_shapes(self):
		r = self.do_render(2,3,False,False)
		self.assertEquals(3,len(r))
		self.assertEquals(3,len(find_type(self,r,core.Line)))
	
	def test_render_coordinates(self):
		r = self.do_render(2,3,False,False)
		mid = find_with(self,r,"a",(2.5,4))
		self.assertEquals((2.5,3),mid.b)
		lft = find_with(self,r,"a",(2,3.4))
		self.assertEquals((2.5,3),lft.b)
		rgt = find_with(self,r,"a",(3,3.4))
		self.assertEquals((2.5,3),rgt.b)
		
	def test_render_coordinates_position(self):
		r = self.do_render(5,7,False,False)
		mid = find_with(self,r,"a",(5.5,8))
		self.assertEquals((5.5,7),mid.b)
		lft = find_with(self,r,"a",(5,7.4))
		self.assertEquals((5.5,7),lft.b)
		rgt = find_with(self,r,"a",(6,7.4))
		self.assertEquals((5.5,7),rgt.b)
	
	def test_render_coordinates_box(self):
		r = self.do_render(2,3,True,False)
		mid = find_with(self,r,"a",(2.5,4))
		self.assertEquals((2.5,2.5),mid.b)
		lft = find_with(self,r,"a",(2,2.9))
		self.assertEquals((2.5,2.5),lft.b)
		rgt = find_with(self,r,"a",(3,2.9))
		self.assertEquals((2.5,2.5),rgt.b)
	
	def test_render_z(self):
		r = self.do_render(2,3,False,False)
		for shape in r:
			self.assertEquals(0, shape.z)
			
	def test_render_stroke_colour(self):
		r = self.do_render(2,3,False,False)
		for shape in r:
			self.assertEquals(core.C_FOREGROUND,shape.stroke)
			
	def test_render_stroke_width(self):
		r = self.do_render(2,3,False,False)
		for shape in r:
			self.assertEquals(1,shape.w)
	
	def test_render_stroke_style_solid(self):
		r = self.do_render(2,3,False,False)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)
				
	def test_render_stoke_style_dashed(self):
		r = self.do_render(2,3,False,True)
		r.sort(lambda i,j: cmp(abs(i.b[1]-i.a[1]),abs(j.b[1]-j.a[1])),reverse=True)
		self.assertEquals(core.STROKE_DASHED, r[0].stype)
		self.assertEquals(core.STROKE_SOLID, r[1].stype)
		self.assertEquals(core.STROKE_SOLID, r[2].stype)
	
	
class TestDArrowheadPattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.DArrowheadPattern
		
	def test_accepts_arrowhead(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"v",core.M_LINE_AFTER_S))
		feed_input(p,0,3,"\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2," ",core.M_NONE))
	
	def test_expects_vee(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"?",core.M_LINE_AFTER_S))
	
	def test_expects_vee_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"v",core.M_OCCUPIED|core.M_LINE_AFTER_S) )
	
	def test_allows_uppercase_vee(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"V",core.M_LINE_AFTER_S) )
	
	def test_allows_rest_of_first_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"v",core.M_LINE_AFTER_S))
		p.test(main.CurrentChar(0,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,4,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,5,"\n",core.M_OCCUPIED))
	
	def test_allows_start_of_second_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"v",core.M_LINE_AFTER_S))
		feed_input(p,0,3,"\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
	
	def test_expects_north_line_meta(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"v",core.M_NONE))
	
	def test_allows_box_north_meta(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"v",core.M_LINE_AFTER_S))
		feed_input(p,0,3,"\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2," ",core.M_BOX_START_S))
	
	def test_allows_dashed_north_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"v",core.M_LINE_AFTER_S|core.M_DASH_AFTER_S))
		feed_input(p,0,3,"\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2," ",core.M_NONE))
	
	def test_doesnt_error_at_top_left_corner(self):
		p = self.pclass()
		try:
			p.test(main.CurrentChar(-1,0,core.START_OF_INPUT,core.M_NONE))
		except core.PatternRejected: pass
	
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((2,  "v \n"),
				 (0,"  "    ),)
		l = core.M_LINE_AFTER_S
		n = core.M_NONE
		o = core.M_OCCUPIED
		inmeta = ((    l,n,n,),
				  (n,n,      ),)
		outmeta = ((   o,n,n,),
				   (n,n,     ),)  
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				im = inmeta[j][i]
				om = outmeta[j][i]
				self.assertEquals(om,p.test(main.CurrentChar(j,startcol+i,char,im)))
	
	def do_render(self,x,y,box,dashed):
		p = self.pclass()
		p.test(main.CurrentChar(y,x,"v", core.M_LINE_AFTER_S
				| (core.M_DASH_AFTER_S if dashed else core.M_NONE)))
		feed_input(p,y,x+1,"\n")
		feed_input(p,y+1,0," "*x)
		try:
			p.test(main.CurrentChar(y+1,x," ",
					core.M_BOX_START_S if box else core.M_NONE))
		except StopIteration: pass
		return p.render()
	
	def test_render_returns_correct_shapes(self):
		r = self.do_render(2,3,False,False)
		self.assertEquals(3,len(r))
		self.assertEquals(3,len(find_type(self,r,core.Line)))
	
	def test_render_coordinates(self):
		r = self.do_render(2,3,False,False)
		mid = find_with(self,r,"a",(2.5,3))
		self.assertEquals((2.5,4),mid.b)
		lft = find_with(self,r,"a",(2,3.6))
		self.assertEquals((2.5,4),lft.b)
		rgt = find_with(self,r,"a",(3,3.6))
		self.assertEquals((2.5,4),rgt.b)
	
	def test_render_coordinates_position(self):
		r = self.do_render(5,7,False,False)
		mid = find_with(self,r,"a",(5.5,7))
		self.assertEquals((5.5,8),mid.b)
		lft = find_with(self,r,"a",(5,7.6))
		self.assertEquals((5.5,8),lft.b)
		rgt = find_with(self,r,"a",(6,7.6))
		self.assertEquals((5.5,8),rgt.b)
	
	def test_render_coordinates_box(self):
		r = self.do_render(2,3,True,False)
		mid = find_with(self,r,"a",(2.5,3))
		self.assertEquals((2.5,4.5),mid.b)
		lft = find_with(self,r,"a",(2,4.1))
		self.assertEquals((2.5,4.5),lft.b)
		rgt = find_with(self,r,"a",(3,4.1))
		self.assertEquals((2.5,4.5),rgt.b)
	
	def test_render_z(self):
		r = self.do_render(2,3,False,False)
		for shape in r:
			self.assertEquals(0, shape.z)
			
	def test_render_stroke_colour(self):
		r = self.do_render(2,3,False,False)
		for shape in r:
			self.assertEquals(core.C_FOREGROUND,shape.stroke)
			
	def test_render_stroke_width(self):
		r = self.do_render(2,3,False,False)
		for shape in r:
			self.assertEquals(1,shape.w)
	
	def test_render_stroke_style_solid(self):
		r = self.do_render(2,3,False,False)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)
				
	def test_render_stoke_style_dashed(self):
		r = self.do_render(2,3,False,True)
		r.sort(lambda i,j: cmp(abs(i.b[1]-i.a[1]),abs(j.b[1]-j.a[1])),reverse=True)
		self.assertEquals(core.STROKE_DASHED, r[0].stype)
		self.assertEquals(core.STROKE_SOLID, r[1].stype)
		self.assertEquals(core.STROKE_SOLID, r[2].stype)	


class TestLCrowsFeetPattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.LCrowsFeetPattern

	def test_accepts_crows_feet(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,">",core.M_BOX_AFTER_E))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,3," ",core.M_LINE_START_E))
			
	def test_expects_right_angle_bracket(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"?",core.M_BOX_AFTER_E))
			
	def test_expects_right_angle_bracket_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,">",core.M_BOX_AFTER_E|core.M_OCCUPIED))
			
	def test_expects_west_box_meta(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,">",core.M_NONE))
			
	def test_expects_east_line_meta(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,">",core.M_BOX_AFTER_E))
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
			
	def test_allows_dashed_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,">",core.M_BOX_AFTER_E))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,3," ",core.M_LINE_START_E|core.M_DASH_START_E))
		
	def test_allows_occupied_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,">",core.M_BOX_AFTER_E))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,3," ",core.M_LINE_START_E|core.M_OCCUPIED))

	def test_doesnt_error_at_top_left_corner(self):
		p = self.pclass()
		try:
			p.test(main.CurrentChar(-1,0,core.START_OF_INPUT,core.M_NONE))
		except core.PatternRejected: pass
			
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		m = p.test(main.CurrentChar(0,2,">",core.M_BOX_AFTER_E))
		self.assertEquals(core.M_OCCUPIED, m)
		
	def do_render(self,x,y,dashed):
		p = self.pclass()
		p.test(main.CurrentChar(y,x,">",core.M_BOX_AFTER_E))
		try:
			p.test(main.CurrentChar(y,x+1," ",core.M_LINE_START_E
				| (core.M_DASH_START_E if dashed else core.M_NONE)))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_correct_shapes(self):
		r = self.do_render(3,2,False)
		self.assertEquals(4,len(r))
		for shape in r:
			self.assertTrue( isinstance(shape,core.Line) )
			
	def test_render_coordinates(self):
		r = self.do_render(3,2,False)
		stem = find_with(self,r,"a",(4,2.5))
		self.assertEquals((3.5,2.5),stem.b)
		mid = find_with(self,r,"b",(2.5,2.5))
		self.assertEquals((3.5,2.5),mid.a)
		lft = find_with(self,r,"b",(2.5,2.2))
		self.assertEquals((3.5,2.5),lft.a)
		rgt = find_with(self,r,"b",(2.5,2.8))
		self.assertEquals((3.5,2.5),rgt.a)

	def test_render_coordinates_position(self):
		r = self.do_render(6,9,False)
		stem = find_with(self,r,"a",(7,9.5))
		self.assertEquals((6.5,9.5),stem.b)
		mid = find_with(self,r,"b",(5.5,9.5))
		self.assertEquals((6.5,9.5),mid.a)
		lft = find_with(self,r,"b",(5.5,9.2))
		self.assertEquals((6.5,9.5),lft.a)
		rgt = find_with(self,r,"b",(5.5,9.8))
		self.assertEquals((6.5,9.5),rgt.a)
			
	def test_render_z(self):
		r = self.do_render(2,3,False)
		for shape in r:
			self.assertEquals(0, shape.z)
			
	def test_render_stroke_colour(self):
		r = self.do_render(2,3,False)
		for shape in r:
			self.assertEquals(core.C_FOREGROUND,shape.stroke)
			
	def test_render_stroke_width(self):
		r = self.do_render(2,3,False)
		for shape in r:
			self.assertEquals(1,shape.w)
			
	def test_render_stroke_style_solid(self):
		r = self.do_render(2,3,False)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)
			
	def test_render_stroke_style_dashed(self):
		r = self.do_render(2,3,True)
		l = find_with(self,r,"a",(3,3.5))
		self.assertEquals(core.STROKE_DASHED,l.stype)
		r.remove(l)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)
			
	
class TestRCrowsFeetPattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.RCrowsFeetPattern

	def test_accepts_crows_feet(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"<",core.M_LINE_AFTER_E))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,3," ",core.M_BOX_START_E))
			
	def test_expects_left_angle_bracket(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"?",core.M_LINE_AFTER_E))
			
	def test_expects_left_angle_bracket_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"<",core.M_LINE_AFTER_E|core.M_OCCUPIED))
			
	def test_expects_east_box_meta(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"<",core.M_LINE_AFTER_E))
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2," ",core.M_NONE))
			
	def test_expects_west_line_meta(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"<",core.M_NONE))
			
	def test_allows_dashed_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"<",core.M_LINE_AFTER_E|core.M_DASH_AFTER_E))
		
	def test_allows_occupied_box(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"<",core.M_LINE_AFTER_E))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,3," ",core.M_BOX_START_E|core.M_OCCUPIED))
			
	def test_doesnt_error_at_top_left_corner(self):
		p = self.pclass()
		try:
			p.test(main.CurrentChar(-1,0,core.START_OF_INPUT,core.M_NONE))
		except core.PatternRejected: pass
			
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		m = p.test(main.CurrentChar(0,2,"<",core.M_LINE_AFTER_E))
		self.assertEquals(core.M_OCCUPIED, m)
		
	def do_render(self,x,y,dashed):
		p = self.pclass()
		p.test(main.CurrentChar(y,x,"<",core.M_LINE_AFTER_E
				| (core.M_DASH_AFTER_E if dashed else core.M_NONE)))
		try:
			p.test(main.CurrentChar(y,x+1," ",core.M_BOX_START_E))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_correct_shapes(self):
		r = self.do_render(3,2,False)
		self.assertEquals(4,len(r))
		for shape in r:
			self.assertTrue( isinstance(shape,core.Line) )
			
	def test_render_coordinates(self):
		r = self.do_render(3,2,False)
		stem = find_with(self,r,"a",(3,2.5))
		self.assertEquals((3.5,2.5),stem.b)
		mid = find_with(self,r,"b",(4.5,2.5))
		self.assertEquals((3.5,2.5),mid.a)
		lft = find_with(self,r,"b",(4.5,2.2))
		self.assertEquals((3.5,2.5),lft.a)
		rgt = find_with(self,r,"b",(4.5,2.8))
		self.assertEquals((3.5,2.5),rgt.a)

	def test_render_coordinates_position(self):
		r = self.do_render(6,9,False)
		stem = find_with(self,r,"a",(6,9.5))
		self.assertEquals((6.5,9.5),stem.b)
		mid = find_with(self,r,"b",(7.5,9.5))
		self.assertEquals((6.5,9.5),mid.a)
		lft = find_with(self,r,"b",(7.5,9.2))
		self.assertEquals((6.5,9.5),lft.a)
		rgt = find_with(self,r,"b",(7.5,9.8))
		self.assertEquals((6.5,9.5),rgt.a)
			
	def test_render_z(self):
		r = self.do_render(2,3,False)
		for shape in r:
			self.assertEquals(0, shape.z)
			
	def test_render_stroke_colour(self):
		r = self.do_render(2,3,False)
		for shape in r:
			self.assertEquals(core.C_FOREGROUND,shape.stroke)
			
	def test_render_stroke_width(self):
		r = self.do_render(2,3,False)
		for shape in r:
			self.assertEquals(1,shape.w)
			
	def test_render_stroke_style_solid(self):
		r = self.do_render(2,3,False)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)
			
	def test_render_stroke_style_dashed(self):
		r = self.do_render(2,3,True)
		l = find_with(self,r,"a",(2,3.5))
		self.assertEquals(core.STROKE_DASHED,l.stype)
		r.remove(l)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)
		
		
class TestUCrowsFeetPattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.UCrowsFeetPattern

	def test_accepts_crows_feet(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"v",core.M_BOX_AFTER_S))
		feed_input(p,0,3,"\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2," ",core.M_LINE_START_S))
			
	def test_expects_vee(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"?",core.M_BOX_AFTER_S))
			
	def test_expects_vee_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"v",core.M_BOX_AFTER_S|core.M_OCCUPIED))
			
	def test_allows_uppercase_vee(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"V",core.M_BOX_AFTER_S))
		
	def test_expects_north_box_meta(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"v",core.M_NONE))
		
	def test_allows_rest_of_first_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"v",core.M_BOX_AFTER_S))
		p.test(main.CurrentChar(0,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,4,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,5,"\n",core.M_OCCUPIED))	
			
	def test_allows_start_of_second_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"v",core.M_BOX_AFTER_S))
		feed_input(p,0,3,"\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
			
	def test_expects_south_line_meta(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"v",core.M_BOX_AFTER_S))
		feed_input(p,0,3,"\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2," ",core.M_NONE))
				
	def test_allows_dashed_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"v",core.M_BOX_AFTER_S))
		feed_input(p,0,3,"\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2," ",core.M_LINE_START_S|core.M_DASH_START_S))
		
	def test_allows_occupied_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"v",core.M_BOX_AFTER_S))
		feed_input(p,0,3,"\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2," ",core.M_LINE_START_S|core.M_OCCUPIED))
	
	def test_doesnt_error_at_top_left_corner(self):
		p = self.pclass()
		try:
			p.test(main.CurrentChar(-1,0,core.START_OF_INPUT,core.M_NONE))
		except core.PatternRejected: pass
	
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((2,  "v  \n"),
				 (0,"  "     ),)
		n = core.M_NONE
		o = core.M_OCCUPIED
		b = core.M_BOX_AFTER_S
		metain = ((    b,n,n,n,),
				  (n,n,        ),)
		metaout = ((    o,n,n,n,),
				   (n,n,        ),)
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				mi = metain[j][i]
				mo = metaout[j][i]
				self.assertEquals(mo,p.test(main.CurrentChar(j,startcol+i,char,mi)))
		
	def do_render(self,x,y,dashed):
		p = self.pclass()
		p.test(main.CurrentChar(y,x,"v",core.M_BOX_AFTER_S))
		feed_input(p,y,x+1,"\n")
		feed_input(p,y+1,0," "*x)
		try:
			p.test(main.CurrentChar(y+1,x," ",core.M_LINE_START_S
					| (core.M_DASH_START_S if dashed else core.M_NONE)))
		except StopIteration: pass
		return p.render()
	
	def test_render_returns_correct_shapes(self):
		r = self.do_render(3,2,False)
		self.assertEquals(4,len(r))
		for shape in r:
			self.assertTrue( isinstance(shape,core.Line) )
			
	def test_render_coordinates(self):
		r = self.do_render(3,2,False)
		stem = find_with(self,r,"a",(3.5,3))
		self.assertEquals((3.5,2),stem.b)
		mid = find_with(self,r,"b",(3.5,1.5))
		self.assertEquals((3.5,2),mid.a)
		lft = find_with(self,r,"b",(2.9,1.5))
		self.assertEquals((3.5,2),lft.a)
		rgt = find_with(self,r,"b",(4.1,1.5))
		self.assertEquals((3.5,2),rgt.a)

	def test_render_coordinates_position(self):
		r = self.do_render(6,9,False)
		stem = find_with(self,r,"a",(6.5,10))
		self.assertEquals((6.5,9),stem.b)
		mid = find_with(self,r,"b",(6.5,8.5))
		self.assertEquals((6.5,9),mid.a)
		lft = find_with(self,r,"b",(5.9,8.5))
		self.assertEquals((6.5,9),lft.a)
		rgt = find_with(self,r,"b",(7.1,8.5))
		self.assertEquals((6.5,9),rgt.a)
	
	def test_render_z(self):
		r = self.do_render(2,3,False)
		for shape in r:
			self.assertEquals(0, shape.z)
			
	def test_render_stroke_colour(self):
		r = self.do_render(2,3,False)
		for shape in r:
			self.assertEquals(core.C_FOREGROUND,shape.stroke)
			
	def test_render_stroke_width(self):
		r = self.do_render(2,3,False)
		for shape in r:
			self.assertEquals(1,shape.w)
			
	def test_render_stroke_style_solid(self):
		r = self.do_render(2,3,False)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)
			
	def test_render_stroke_style_dashed(self):
		r = self.do_render(2,3,True)
		l = find_with(self,r,"a",(2.5,4))
		self.assertEquals(core.STROKE_DASHED,l.stype)
		r.remove(l)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)
	
	
class TestDCrowsFeetPattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.DCrowsFeetPattern

	def test_accepts_crows_feet(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"^",core.M_LINE_AFTER_S))
		feed_input(p,0,3,"\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2," ",core.M_BOX_START_S))
			
	def test_expects_caret(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"?",core.M_LINE_AFTER_S))
			
	def test_expects_caret_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"^",core.M_LINE_AFTER_S|core.M_OCCUPIED))
			
	def test_expects_north_line_meta(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"^",core.M_NONE))
		
	def test_allows_rest_of_first_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"^",core.M_LINE_AFTER_S))
		p.test(main.CurrentChar(0,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,4,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,5,"\n",core.M_OCCUPIED))	
			
	def test_allows_start_of_second_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"^",core.M_LINE_AFTER_S))
		feed_input(p,0,3,"\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
			
	def test_expects_south_box_meta(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"^",core.M_LINE_AFTER_S))
		feed_input(p,0,3,"\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2," ",core.M_NONE))
				
	def test_allows_dashed_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"^",core.M_LINE_AFTER_S|core.M_DASH_AFTER_S))
		
	def test_allows_occupied_box(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,2,"^",core.M_LINE_AFTER_S))
		feed_input(p,0,3,"\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2," ",core.M_BOX_START_S|core.M_OCCUPIED))
	
	def test_doesnt_error_at_top_left_corner(self):
		p = self.pclass()
		try:
			p.test(main.CurrentChar(-1,0,core.START_OF_INPUT,core.M_NONE))
		except core.PatternRejected: pass
	
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((2,  "^  \n"),
				 (0,"  "     ),)
		n = core.M_NONE
		o = core.M_OCCUPIED
		l = core.M_LINE_AFTER_S
		metain = ((    l,n,n,n,),
				  (n,n,        ),)
		metaout = ((    o,n,n,n,),
				   (n,n,        ),)
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				mi = metain[j][i]
				mo = metaout[j][i]
				self.assertEquals(mo,p.test(main.CurrentChar(j,startcol+i,char,mi)))
		
	def do_render(self,x,y,dashed):
		p = self.pclass()
		p.test(main.CurrentChar(y,x,"^",core.M_LINE_AFTER_S
				|(core.M_DASH_AFTER_S if dashed else core.M_NONE)))
		feed_input(p,y,x+1,"\n")
		feed_input(p,y+1,0," "*x)
		try:
			p.test(main.CurrentChar(y+1,x," ",core.M_BOX_START_S))
		except StopIteration: pass
		return p.render()
	
	def test_render_returns_correct_shapes(self):
		r = self.do_render(3,2,False)
		self.assertEquals(4,len(r))
		for shape in r:
			self.assertTrue( isinstance(shape,core.Line) )
			
	def test_render_coordinates(self):
		r = self.do_render(3,2,False)
		stem = find_with(self,r,"a",(3.5,2))
		self.assertEquals((3.5,3),stem.b)
		mid = find_with(self,r,"b",(3.5,3.5))
		self.assertEquals((3.5,3),mid.a)
		lft = find_with(self,r,"b",(2.9,3.5))
		self.assertEquals((3.5,3),lft.a)
		rgt = find_with(self,r,"b",(4.1,3.5))
		self.assertEquals((3.5,3),rgt.a)

	def test_render_coordinates_position(self):
		r = self.do_render(6,9,False)
		stem = find_with(self,r,"a",(6.5,9))
		self.assertEquals((6.5,10),stem.b)
		mid = find_with(self,r,"b",(6.5,10.5))
		self.assertEquals((6.5,10),mid.a)
		lft = find_with(self,r,"b",(5.9,10.5))
		self.assertEquals((6.5,10),lft.a)
		rgt = find_with(self,r,"b",(7.1,10.5))
		self.assertEquals((6.5,10),rgt.a)
	
	def test_render_z(self):
		r = self.do_render(2,3,False)
		for shape in r:
			self.assertEquals(0, shape.z)
			
	def test_render_stroke_colour(self):
		r = self.do_render(2,3,False)
		for shape in r:
			self.assertEquals(core.C_FOREGROUND,shape.stroke)
			
	def test_render_stroke_width(self):
		r = self.do_render(2,3,False)
		for shape in r:
			self.assertEquals(1,shape.w)
			
	def test_render_stroke_style_solid(self):
		r = self.do_render(2,3,False)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)
			
	def test_render_stroke_style_dashed(self):
		r = self.do_render(2,3,True)
		l = find_with(self,r,"a",(2.5,3))
		self.assertEquals(core.STROKE_DASHED,l.stype)
		r.remove(l)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)	


class TestUOutlineArrowheadPattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.UOutlineArrowheadPattern
		
	def test_accepts_arrowhead(self):  
		p = self.pclass()
		feed_input(p,3,4,    "/_\  \n")
		feed_input(p,4,0,"     ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(4,5,"|",core.M_LINE_START_S))
			
	def test_expects_forwardslash(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(4,5,"?",core.M_NONE))
			
	def test_expects_fowardslash_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(4,5,"/",core.M_OCCUPIED))
			
	def test_expects_underscore(self):
		p = self.pclass()
		feed_input(p,4,5,"/")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(4,6,"\\",core.M_NONE))
			
	def test_expects_underscore_unoccupied(self):
		p = self.pclass()
		feed_input(p,4,5,"/")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(4,6,"_",core.M_OCCUPIED))
			
	def test_expects_backslash(self):
		p = self.pclass()
		feed_input(p,4,5,"/_")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(4,7,"_",core.M_NONE))
			
	def test_expects_backslash_unoccupied(self):
		p = self.pclass()
		feed_input(p,4,5,"/_")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(4,7,"\\",core.M_OCCUPIED))
			
	def test_allows_rest_of_first_line(self):
		p = self.pclass()
		feed_input(p,4,5,"/_\\")
		p.test(main.CurrentChar(4,8,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(4,9,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(4,10,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_second_line(self):
		p = self.pclass()
		feed_input(p,4,2,"/_\\  \n")
		p.test(main.CurrentChar(5,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(5,1,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(5,2,"c",core.M_OCCUPIED))
		
	def test_expects_line_meta(self):
		p = self.pclass()
		feed_input(p,4,3,   "/_\\  \n")
		feed_input(p,5,0,"    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(5,4,"|",core.M_NONE))
			
	def test_allows_dashed_line(self):
		p = self.pclass()
		feed_input(p,4,3,   "/_\\  \n")
		feed_input(p,5,0,"    ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(5,4,";",core.M_LINE_START_S|core.M_DASH_START_S))
		
	def test_allows_any_character_for_line(self):
		p = self.pclass()
		feed_input(p,4,3,   "/_\\  \n")
		feed_input(p,5,0,"    ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(5,4,"?",core.M_LINE_START_S))
		
	def test_allows_occupied_line(self):
		p = self.pclass()
		feed_input(p,4,3,   "/_\\  \n")
		feed_input(p,5,0,"    ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(5,4,"|",core.M_LINE_START_S|core.M_OCCUPIED))

	def test_allows_box_underside(self):
		p = self.pclass()
		p.test(main.CurrentChar(4,3,"/",core.M_BOX_AFTER_S))
		p.test(main.CurrentChar(4,4,"_",core.M_BOX_AFTER_S))
		p.test(main.CurrentChar(4,5,"\\",core.M_BOX_AFTER_S))
		p.test(main.CurrentChar(4,6," ",core.M_BOX_AFTER_S))
		p.test(main.CurrentChar(4,7,"\n",core.M_BOX_AFTER_S))

	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((3,   "/_\\  \n"),
				 (0,"    "       ),)
		o = core.M_OCCUPIED
		n = core.M_NONE
		meta = ((      o,o,o,n,n,n,),
			    (n,n,n,n,          ),)
		for j,(linestart,line) in enumerate(input):
			for i,char in enumerate(line):
				m = meta[j][i]
				self.assertEquals(m,p.test(main.CurrentChar(j,linestart+i,char,core.M_NONE)))
				
	def do_render(self,x,y,dash=False,tobox=False):
		p = self.pclass()
		p.test(main.CurrentChar(y,x+0,"/",core.M_BOX_AFTER_S if tobox else core.M_NONE))
		p.test(main.CurrentChar(y,x+1,"_",core.M_BOX_AFTER_S if tobox else core.M_NONE))
		p.test(main.CurrentChar(y,x+2,"\\",core.M_BOX_AFTER_S if tobox else core.M_NONE))
		p.test(main.CurrentChar(y,x+3,"\n",core.M_BOX_AFTER_S if tobox else core.M_NONE))
		feed_input(p,y+1,0," "*(x+1))
		try:
			p.test(main.CurrentChar(y+1,x+1,"|",
				core.M_LINE_START_S | (core.M_DASH_START_S if dash else core.M_NONE)))
		except StopIteration: pass		
		return p.render()
		
	def test_render_returns_correct_shapes(self):
		r = self.do_render(4,6)
		self.assertEquals(4,len(r))
		self.assertEquals(4,len(filter(lambda x: isinstance(x,core.Line),r)))
		
	def test_render_coordinates(self):
		r = self.do_render(4,6)
		ls = find_with(self,r,"b",(5,6.4))
		self.assertEquals((5.5,6),ls.a)
		rs = find_with(self,r,"b",(6,6.4))
		self.assertEquals((5.5,6),rs.a)
		bt = find_with(self,r,"a",(5,6.4))
		self.assertEquals((6,6.4),bt.b)
		st = find_with(self,r,"a",(5.5,6.4))
		self.assertEquals((5.5,7),st.b)
		
	def test_render_coordinates_position(self):
		r = self.do_render(8,2)
		ls = find_with(self,r,"b",(9,2.4))
		self.assertEquals((9.5,2),ls.a)
		rs = find_with(self,r,"b",(10,2.4))
		self.assertEquals((9.5,2),ls.a)
		bt = find_with(self,r,"a",(9,2.4))
		self.assertEquals((10,2.4),bt.b)
		st = find_with(self,r,"a",(9.5,2.4))
		self.assertEquals((9.5,3),st.b)
		
	def test_render_coordinates_to_box(self):
		r = self.do_render(4,6,tobox=True)
		ls = find_with(self,r,"b",(5,5.9))
		self.assertEquals((5.5,5.5),ls.a)
		rs = find_with(self,r,"b",(6,5.9))
		self.assertEquals((5.5,5.5),ls.a)
		bt = find_with(self,r,"a",(5,5.9))
		self.assertEquals((6,5.9),bt.b)
		st = find_with(self,r,"a",(5.5,5.9))
		self.assertEquals((5.5,7),st.b)

	def test_render_z(self):
		for shape in self.do_render(4,6):
			self.assertEquals(1,shape.z)
			
	def test_render_stroke(self):
		for shape in self.do_render(4,6):
			self.assertEquals(core.C_FOREGROUND,shape.stroke)
			
	def test_render_stroke_alpha(self):
		for shape in self.do_render(4,6):
			self.assertEquals(1.0,shape.salpha)
			
	def test_render_stroke_width(self):
		for shape in self.do_render(4,6):
			self.assertEquals(1,shape.w)

	def test_render_stroke_style_solid(self):
		for shape in self.do_render(4,6):
			self.assertEquals(core.STROKE_SOLID,shape.stype)
	
	def test_render_stroke_style_dashed(self):
		r = list(self.do_render(4,6,dash=True))
		st = find_with(self,r,"a",(5.5,6.4))
		self.assertEquals(core.STROKE_DASHED,st.stype)
		r.remove(st)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)


class TestDOutlineArrowheadPattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.DOutlineArrowheadPattern
		
	def test_accepts_arrowhead(self):  
		p = self.pclass()
		feed_input(p,3,4,    "_|_  \n")
		feed_input(p,4,0,"    \\")
		p.test(main.CurrentChar(4,5," ",core.M_LINE_AFTER_S))
		feed_input(p,4,6,      "/  \n")
		feed_input(p,5,0,"     ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(5,5," ",core.M_NONE))
			
	def test_expects_left_underscore(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(4,5,"?",core.M_NONE))
			
	def test_expects_left_underscore_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(4,5,"_",core.M_OCCUPIED))
			
	def test_allows_occupied_line(self):
		p = self.pclass()
		feed_input(p,4,5,"_")
		p.test(main.CurrentChar(4,6,"|",core.M_OCCUPIED))
			
	def test_expects_right_underscore(self):
		p = self.pclass()
		feed_input(p,4,5,"_|")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(4,7,"|",core.M_OCCUPIED))
			
	def test_expects_right_underscore_unoccupied(self):
		p = self.pclass()
		feed_input(p,4,5,"_|")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(4,7,"_",core.M_OCCUPIED))
			
	def test_allows_rest_of_first_line(self):
		p = self.pclass()
		feed_input(p,4,5,"_|_")
		p.test(main.CurrentChar(4,8,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(4,9,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(4,10,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_second_line(self):
		p = self.pclass()
		feed_input(p,4,2,"_|_  \n")
		p.test(main.CurrentChar(5,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(5,1,"b",core.M_OCCUPIED))
		
	def test_expects_backslash(self):
		p = self.pclass()
		feed_input(p,4,2,  "_|_  \n")
		feed_input(p,5,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(5,2,"?",core.M_NONE))
			
	def test_expects_backslash_unoccupied(self):
		p = self.pclass()
		feed_input(p,4,2,  "_|_  \n")
		feed_input(p,5,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(5,2,"\\",core.M_OCCUPIED))
		
	def test_expects_central_space(self):
		p = self.pclass()
		feed_input(p,4,2,  "_|_  \n")
		feed_input(p,5,0,"  \\")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(5,3,"/",core.M_LINE_AFTER_S))
			
	def test_expects_central_space_unoccupied(self):
		p = self.pclass()
		feed_input(p,4,2,  "_|_  \n")
		feed_input(p,5,0,"  \\")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(5,3," ",core.M_LINE_AFTER_S | core.M_OCCUPIED))
		
	def test_expects_central_space_line_meta(self):
		p = self.pclass()
		feed_input(p,4,2,  "_|_  \n")
		feed_input(p,5,0,"  \\")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(5,3," ",core.M_NONE))
		
	def test_allows_dashed_line(self):
		p = self.pclass()
		feed_input(p,4,3,   "_;_  \n")
		feed_input(p,5,0,"   \\")
		p.test(main.CurrentChar(5,4," ",core.M_LINE_AFTER_S|core.M_DASH_AFTER_S))
		
	def test_allows_any_character_for_line(self):
		p = self.pclass()
		feed_input(p,4,3,   "_?_  \n")
	
	def test_expects_forwardslash(self):
		p = self.pclass()
		feed_input(p,4,3,   "_|_  \n")
		feed_input(p,5,0,"   \\")
		p.test(main.CurrentChar(5,4," ",core.M_LINE_AFTER_S))
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(5,5," ",core.M_NONE))
			
	def test_expects_forwardslash_unoccupied(self):
		p = self.pclass()
		feed_input(p,4,3,   "_|_  \n")
		feed_input(p,5,0,"   \\")
		p.test(main.CurrentChar(5,4," ",core.M_LINE_AFTER_S))
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(5,5,"/",core.M_OCCUPIED))
			
	def test_allows_rest_of_second_line(self):
		p = self.pclass()
		feed_input(p,4,3,   "_|_  \n")
		feed_input(p,5,0,"   \\")
		p.test(main.CurrentChar(5,4," ",core.M_LINE_AFTER_S))
		feed_input(p,5,5,     "/")
		p.test(main.CurrentChar(5,6,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(5,7,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(5,8,"\n",core.M_OCCUPIED))
		
	def test_allows_occupied_third_line(self):
		p = self.pclass()
		feed_input(p,4,3,   "_|_  \n")
		feed_input(p,5,0,"   \\")
		p.test(main.CurrentChar(5,4," ",core.M_LINE_AFTER_S))
		feed_input(p,5,5,     "/  \n")
		p.test(main.CurrentChar(6,0," ",core.M_OCCUPIED))
		p.test(main.CurrentChar(6,1," ",core.M_OCCUPIED))
		p.test(main.CurrentChar(6,2," ",core.M_OCCUPIED))
		p.test(main.CurrentChar(6,3," ",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(6,4," ",core.M_OCCUPIED))

	def test_allows_box_top_meta(self):
		p = self.pclass()
		feed_input(p,4,3,   "_|_  \n")
		feed_input(p,5,0,"   \\")
		p.test(main.CurrentChar(5,4," ",core.M_LINE_AFTER_S))
		feed_input(p,5,5,     "/  \n")
		p.test(main.CurrentChar(6,0," ",core.M_BOX_START_S))
		p.test(main.CurrentChar(6,1," ",core.M_BOX_START_S))
		p.test(main.CurrentChar(6,2," ",core.M_BOX_START_S))
		p.test(main.CurrentChar(6,3," ",core.M_BOX_START_S))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(6,4," ",core.M_BOX_START_S))

	def test_allow_no_final_line(self):
		p = self.pclass()
		feed_input(p,4,3,   "_|_  \n")
		feed_input(p,5,0,"   \\")
		p.test(main.CurrentChar(5,4," ",core.M_LINE_AFTER_S))
		feed_input(p,5,5,      "/  \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(6,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_short_final_line(self):
		p = self.pclass()
		feed_input(p,4,3,   "_|_  \n")
		feed_input(p,5,0,"   \\")
		p.test(main.CurrentChar(5,4," ",core.M_LINE_AFTER_S))
		feed_input(p,5,5,      "/  \n")
		feed_input(p,6,0,"   \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(7,0," ",core.M_NONE))
		
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((3,   "_|_  \n" ),
				 (0,"   \\ /  \n"),
				 (0,"    "       ),)
		o = core.M_OCCUPIED
		n = core.M_NONE
		l = core.M_LINE_AFTER_S
		imeta = ((      n,o,n,n,n,n,),
				 (n,n,n,n,l,n,n,n,n,),
				 (n,n,n,n,          ),)
		ometa = ((      o,n,o,n,n,n,),
			     (n,n,n,o,o,o,n,n,n,),
			     (n,n,n,n,          ),)
		for j,(linestart,line) in enumerate(input):
			for i,char in enumerate(line):
				im = imeta[j][i]
				om = ometa[j][i]
				self.assertEquals(om,p.test(main.CurrentChar(j,linestart+i,char,im)))
				
	def do_render(self,x,y,dash=False,tobox=False):
		p = self.pclass()
		feed_input(p,y-1,x-1,"_|_\n")
		feed_input(p,y,0," "*(x-1) + "\\")
		p.test(main.CurrentChar(y,x," ",core.M_LINE_AFTER_S 
			| (core.M_DASH_AFTER_S if dash else core.M_NONE)))
		feed_input(p,y,x+1,"/ \n")
		feed_input(p,y+1,0," "*x)
		try:
			p.test(main.CurrentChar(y+1,x," ",
				core.M_BOX_START_S if tobox else core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_correct_shapes(self):
		r = self.do_render(4,6)
		self.assertEquals(4,len(r))
		self.assertEquals(4,len(filter(lambda x: isinstance(x,core.Line),r)))
		
	def test_render_coordinates(self):
		r = self.do_render(4,6)
		ls = find_with(self,r,"b",(4,6.6))
		self.assertEquals((4.5,7),ls.a)
		rs = find_with(self,r,"b",(5,6.6))
		self.assertEquals((4.5,7),ls.a)
		bt = find_with(self,r,"a",(4,6.6))
		self.assertEquals((5,6.6),bt.b)
		st = find_with(self,r,"a",(4.5,6.6))
		self.assertEquals((4.5,6),st.b)
		
	def test_render_coordinates_position(self):
		r = self.do_render(8,2)
		ls = find_with(self,r,"b",(8,2.6))
		self.assertEquals((8.5,3),ls.a)
		rs = find_with(self,r,"b",(9,2.6))
		self.assertEquals((8.5,3),ls.a)
		bt = find_with(self,r,"a",(8,2.6))
		self.assertEquals((9,2.6),bt.b)
		st = find_with(self,r,"a",(8.5,2.6))
		self.assertEquals((8.5,2),st.b)
		
	def test_render_coordinates_to_box(self):
		r = self.do_render(4,6,tobox=True)
		ls = find_with(self,r,"b",(4,7.1))
		self.assertEquals((4.5,7.5),ls.a)
		rs = find_with(self,r,"b",(5,7.1))
		self.assertEquals((4.5,7.5),ls.a)
		bt = find_with(self,r,"a",(4,7.1))
		self.assertEquals((5,7.1),bt.b)
		st = find_with(self,r,"a",(4.5,7.1))
		self.assertEquals((4.5,6),st.b)

	def test_render_z(self):
		for shape in self.do_render(4,6):
			self.assertEquals(1,shape.z)
			
	def test_render_stroke(self):
		for shape in self.do_render(4,6):
			self.assertEquals(core.C_FOREGROUND,shape.stroke)
			
	def test_render_stroke_alpha(self):
		for shape in self.do_render(4,6):
			self.assertEquals(1.0,shape.salpha)
			
	def test_render_stroke_width(self):
		for shape in self.do_render(4,6):
			self.assertEquals(1,shape.w)

	def test_render_stroke_style_solid(self):
		for shape in self.do_render(4,6):
			self.assertEquals(core.STROKE_SOLID,shape.stype)
	
	def test_render_stroke_style_dashed(self):
		r = list(self.do_render(4,6,dash=True))
		st = find_with(self,r,"a",(4.5,6.6))
		self.assertEquals(core.STROKE_DASHED,st.stype)
		r.remove(st)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)


class TestLOutlineArrowheadPattern(unittest.TestCase,PatternTests):

	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.LOutlineArrowheadPattern
		
	def test_accepts_arrowhead(self):
		p = self.pclass()
		feed_input(p,0,3,"<|")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,5,"-",core.M_LINE_START_E))
			
	def test_expects_left_angle_bracket(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,">",core.M_NONE))
			
	def test_expects_left_angle_bracket_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"<",core.M_OCCUPIED))
			
	def test_expects_pipe(self):
		p = self.pclass()
		feed_input(p,0,3,"<")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"<",core.M_NONE))
			
	def test_expects_pipe_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,3,"<")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"|",core.M_OCCUPIED))
			
	def test_expects_line_meta(self):
		p = self.pclass()
		feed_input(p,3,0,"<|")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,5,"-",core.M_NONE))
			
	def test_allows_dashed_line(self):
		p = self.pclass()
		feed_input(p,3,0,"<|")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,5,"-",core.M_LINE_START_E | core.M_DASH_START_E))
			
	def test_allows_occupied_line(self):
		p = self.pclass()
		feed_input(p,3,0,"<|")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,5,"-",core.M_OCCUPIED | core.M_LINE_START_E))
			
	def test_allows_any_line_character(self):
		p = self.pclass()
		feed_input(p,3,0,"<|")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,5,"?",core.M_LINE_START_E))
			
	def test_allows_box_meta(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,3,"<",core.M_BOX_AFTER_E))
		
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		self.assertEquals(core.M_OCCUPIED, p.test(main.CurrentChar(0,3,"<",core.M_NONE)))
		self.assertEquals(core.M_OCCUPIED, p.test(main.CurrentChar(0,4,"|",core.M_NONE)))

	def do_render(self,x,y,dash=False,tobox=False):
		p = self.pclass()
		p.test(main.CurrentChar(y,x,"<",core.M_BOX_AFTER_E if tobox else core.M_NONE ))
		p.test(main.CurrentChar(y,x+1,"|",core.M_NONE))
		try:
			p.test(main.CurrentChar(y,x+2,"-",core.M_LINE_START_E
				| (core.M_DASH_START_E if dash else core.M_NONE)))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_correct_shapes(self):
		r = self.do_render(4,6)
		self.assertEquals(4,len(r))
		self.assertEquals(4,len(filter(lambda x: isinstance(x,core.Line),r)))
		
	def test_render_coordinates(self):
		r = self.do_render(4,6)
		ls = find_with(self,r,"b",(4.8,6.75))
		self.assertEquals((4,6.5),ls.a)
		rs = find_with(self,r,"b",(4.8,6.25))
		self.assertEquals((4,6.5),ls.a)
		bt = find_with(self,r,"a",(4.8,6.75))
		self.assertEquals((4.8,6.25),bt.b)
		st = find_with(self,r,"a",(4.8,6.5))
		self.assertEquals((6,6.5),st.b)
		
	def test_render_coordinates_position(self):
		r = self.do_render(8,2)
		ls = find_with(self,r,"b",(8.8,2.75))
		self.assertEquals((8,2.5),ls.a)
		rs = find_with(self,r,"b",(8.8,2.25))
		self.assertEquals((8,2.5),ls.a)
		bt = find_with(self,r,"a",(8.8,2.75))
		self.assertEquals((8.8,2.25),bt.b)
		st = find_with(self,r,"a",(8.8,2.5))
		self.assertEquals((10,2.5),st.b)

	def test_render_coordinates_to_box(self):
		r = self.do_render(4,6,tobox=True)
		ls = find_with(self,r,"b",(4.3,6.75))
		self.assertEquals((3.5,6.5),ls.a)
		rs = find_with(self,r,"b",(4.3,6.25))
		self.assertEquals((3.5,6.5),ls.a)
		bt = find_with(self,r,"a",(4.3,6.75))
		self.assertEquals((4.3,6.25),bt.b)
		st = find_with(self,r,"a",(4.3,6.5))
		self.assertEquals((6,6.5),st.b)

	def test_render_z(self):
		for shape in self.do_render(4,6):
			self.assertEquals(1,shape.z)
			
	def test_render_stroke(self):
		for shape in self.do_render(4,6):
			self.assertEquals(core.C_FOREGROUND,shape.stroke)
			
	def test_render_stroke_alpha(self):
		for shape in self.do_render(4,6):
			self.assertEquals(1.0,shape.salpha)
			
	def test_render_stroke_width(self):
		for shape in self.do_render(4,6):
			self.assertEquals(1,shape.w)

	def test_render_stroke_style_solid(self):
		for shape in self.do_render(4,6):
			self.assertEquals(core.STROKE_SOLID,shape.stype)
	
	def test_render_stroke_style_dashed(self):
		r = list(self.do_render(4,6,dash=True))
		st = find_with(self,r,"a",(4.8,6.5))
		self.assertEquals(core.STROKE_DASHED,st.stype)
		r.remove(st)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)	


class TestROutlineArrowheadPattern(unittest.TestCase,PatternTests):

	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.ROutlineArrowheadPattern
		
	def test_accepts_arrowhead(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,3,"|",core.M_LINE_AFTER_E))
		feed_input(p,0,4,">")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,5," ",core.M_NONE))
			
	def test_expects_pipe(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,">",core.M_LINE_AFTER_E))
			
	def test_expects_pipe_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"|",core.M_OCCUPIED|core.M_LINE_AFTER_E))
			
	def test_expects_line_meta(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"|",core.M_NONE))
			
	def test_allows_dashed_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,3,"|",core.M_LINE_AFTER_E|core.M_DASH_AFTER_E))
			
	def test_expects_right_angle_bracket(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,3,"|",core.M_LINE_AFTER_E))
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"<",core.M_NONE))
			
	def test_expects_right_angle_bracket_unoccupied(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,3,"|",core.M_LINE_AFTER_E))
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,">",core.M_OCCUPIED))
					
	def test_allows_final_character(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,3,"|",core.M_LINE_AFTER_E))
		feed_input(p,0,4,">")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,5," ",core.M_OCCUPIED))
			
	def test_allows_box_meta(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,3,"|",core.M_LINE_AFTER_E))
		feed_input(p,0,4,">")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,5,"|",core.M_BOX_START_E))
		
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		self.assertEquals(core.M_OCCUPIED, p.test(main.CurrentChar(0,3,"|",core.M_LINE_AFTER_E)))
		self.assertEquals(core.M_OCCUPIED, p.test(main.CurrentChar(0,4,">",core.M_NONE)))


	def do_render(self,x,y,dash=False,tobox=False):
		p = self.pclass()
		p.test(main.CurrentChar(y,x-1,"|",core.M_LINE_AFTER_E
				| (core.M_DASH_AFTER_E if dash else core.M_NONE)))
		p.test(main.CurrentChar(y,x,">",core.M_NONE))
		try:
			p.test(main.CurrentChar(y,x+1," ",
				core.M_BOX_START_E if tobox else core.M_NONE))
		except StopIteration: pass
		return p.render()
		
	def test_render_returns_correct_shapes(self):
		r = self.do_render(4,6)
		self.assertEquals(4,len(r))
		self.assertEquals(4,len(filter(lambda x: isinstance(x,core.Line),r)))

	def test_render_coordinates(self):
		r = self.do_render(4,6)
		ls = find_with(self,r,"b",(4.2,6.25))
		self.assertEquals((5,6.5),ls.a)
		rs = find_with(self,r,"b",(4.2,6.75))
		self.assertEquals((5,6.5),ls.a)
		bt = find_with(self,r,"a",(4.2,6.25))
		self.assertEquals((4.2,6.75),bt.b)
		st = find_with(self,r,"a",(4.2,6.5))
		self.assertEquals((3,6.5),st.b)

	def test_render_coordinates_position(self):
		r = self.do_render(8,2)
		ls = find_with(self,r,"b",(8.2,2.25))
		self.assertEquals((9,2.5),ls.a)
		rs = find_with(self,r,"b",(8.2,2.75))
		self.assertEquals((9,2.5),ls.a)
		bt = find_with(self,r,"a",(8.2,2.25))
		self.assertEquals((8.2,2.75),bt.b)
		st = find_with(self,r,"a",(8.2,2.5))
		self.assertEquals((7,2.5),st.b)

	def test_render_coordinates_to_box(self):
		r = self.do_render(4,6,tobox=True)
		ls = find_with(self,r,"b",(4.7,6.25))
		self.assertEquals((5.5,6.5),ls.a)
		rs = find_with(self,r,"b",(4.7,6.75))
		self.assertEquals((5.5,6.5),ls.a)
		bt = find_with(self,r,"a",(4.7,6.25))
		self.assertEquals((4.7,6.75),bt.b)
		st = find_with(self,r,"a",(4.7,6.5))
		self.assertEquals((3,6.5),st.b)

	def test_render_z(self):
		for shape in self.do_render(4,6):
			self.assertEquals(1,shape.z)
			
	def test_render_stroke(self):
		for shape in self.do_render(4,6):
			self.assertEquals(core.C_FOREGROUND,shape.stroke)
			
	def test_render_stroke_alpha(self):
		for shape in self.do_render(4,6):
			self.assertEquals(1.0,shape.salpha)
			
	def test_render_stroke_width(self):
		for shape in self.do_render(4,6):
			self.assertEquals(1,shape.w)

	def test_render_stroke_style_solid(self):
		for shape in self.do_render(4,6):
			self.assertEquals(core.STROKE_SOLID,shape.stype)
	
	def test_render_stroke_style_dashed(self):
		r = list(self.do_render(4,6,dash=True))
		st = find_with(self,r,"a",(4.2,6.5))
		self.assertEquals(core.STROKE_DASHED,st.stype)
		r.remove(st)
		for shape in r:
			self.assertEquals(core.STROKE_SOLID,shape.stype)	


if __name__ == "__main__":
	unittest.main()
