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
import io
import xml.dom.minidom
import math
import mock


class TestMatchLookup(unittest.TestCase):

	def test_can_construct(self):
		m = main.MatchLookup()
		
	def test_can_add_match(self):
		m = main.MatchLookup()
		m.add_match(object())
		
	def test_can_add_meta_for_match(self):
		m = main.MatchLookup()
		match = object()
		m.add_match(match)
		m.add_meta(match,(1,1),core.M_OCCUPIED|core.M_BOX_START_E)
		
	def test_get_matches_returns_empty_list_for_no_matches(self):
		m = main.MatchLookup()
		self.assertEquals([], m.get_all_matches())
		
	def test_get_matches_returns_added_matches(self):
		m = main.MatchLookup()
		match1 = object()
		match2 = object()
		m.add_match(match1)
		m.add_match(match2)
		result = m.get_all_matches()
		self.assertEquals(2, len(result))
		self.assertTrue(match1 in result)
		self.assertTrue(match2 in result)
		
	def test_get_matches_returns_list_copy(self):
		m = main.MatchLookup()
		match = object()
		m.add_match(match)
		result = m.get_all_matches()
		result.pop()
		self.assertTrue(1, len(m.get_all_matches()))
		
	def test_get_meta_returns_empty_dict_for_no_meta(self):
		m = main.MatchLookup()
		match = object()
		m.add_match(match)
		self.assertEquals({}, m.get_meta_for(match))
		
	def test_get_meta_returns_meta_dict(self):
		m = main.MatchLookup()
		match = object()
		m.add_match(match)
		m.add_meta(match,(1,1),core.M_OCCUPIED|core.M_BOX_START_E)
		m.add_meta(match,(2,3),core.M_BOX_AFTER_E)
		result = m.get_meta_for(match)
		self.assertEquals(2, len(result))
		self.assertEquals(core.M_OCCUPIED|core.M_BOX_START_E, result[(1,1)])
		self.assertEquals(core.M_BOX_AFTER_E, result[(2,3)])
		
	def test_get_meta_ignores_other_matches(self):
		m = main.MatchLookup()
		match1 = object()
		match2 = object()
		m.add_match(match1)
		m.add_meta(match1,(4,5),core.M_OCCUPIED)
		m.add_match(match2)
		self.assertEquals({}, m.get_meta_for(match2))

	def test_get_meta_returns_empty_dict_if_match_doesnt_exist(self):
		m = main.MatchLookup()
		match = object()
		self.assertEquals({},m.get_meta_for(match))

	def test_get_meta_returns_dict_copy(self):
		m = main.MatchLookup()
		match = object()
		m.add_match(match)
		m.add_meta(match,(2,2),core.M_OCCUPIED)
		result = m.get_meta_for(match)
		result[(2,2)] |= core.M_BOX_START_E
		self.assertEquals(core.M_OCCUPIED, m.get_meta_for(match)[(2,2)])

	def test_get_occupants_returns_match_with_occupied_meta_at_pos(self):
		m = main.MatchLookup()
		match = object()
		m.add_match(match)
		m.add_meta(match,(2,3),core.M_OCCUPIED)
		self.assertEquals([match], m.get_occupants_at((2,3)))

	def test_get_occupants_ignores_other_positions(self):
		m = main.MatchLookup()
		match = object()
		m.add_match(match)
		m.add_meta(match,(2,3),core.M_OCCUPIED)
		self.assertEquals([], m.get_occupants_at((4,5)))
		
	def test_get_occupants_ignores_other_meta_flags(self):
		m = main.MatchLookup()
		match = object()
		m.add_match(match)
		m.add_meta(match,(2,3),core.M_BOX_START_E)
		self.assertEquals([], m.get_occupants_at((2,3)))

	def test_get_occupants_returns_multiple_matches(self):
		m = main.MatchLookup()
		match1 = object()
		m.add_match(match1)
		m.add_meta(match1,(2,3),core.M_OCCUPIED)
		match2 = object()
		m.add_match(match2)
		m.add_meta(match2,(2,3),core.M_OCCUPIED)
		result = m.get_occupants_at((2,3))
		self.assertEquals(2, len(result))
		self.assertTrue(match1 in result)
		self.assertTrue(match2 in result)

	def test_get_occupants_returns_list_copy(self):
		m = main.MatchLookup()
		match = object()
		m.add_match(match)
		m.add_meta(match,(2,2),core.M_OCCUPIED)
		result = m.get_occupants_at((2,2))
		result.pop()
		self.assertEquals(1, len(m.get_occupants_at((2,2))))

	def test_remove_match_removes_from_main_list(self):
		m = main.MatchLookup()
		match = object()
		m.add_match(match)	
		m.remove_match(match)
		self.assertEquals([], m.get_all_matches())
		
	def test_remove_match_removes_matches_meta(self):
		m = main.MatchLookup()
		match = object()
		m.add_match(match)
		m.add_meta(match,(2,2),core.M_OCCUPIED|core.M_BOX_START_E)
		m.remove_match(match)
		self.assertEquals({}, m.get_meta_for(match))
		
	def test_remove_match_removes_from_occupants(self):
		m = main.MatchLookup()
		match = object()
		m.add_match(match)
		m.add_meta(match,(2,2),core.M_OCCUPIED)
		m.remove_match(match)
		self.assertEquals([], m.get_occupants_at((2,2)))
		
	def test_remove_match_ignores_other_matches(self):
		m = main.MatchLookup()
		match1 = object()
		match2 = object()
		m.add_match(match1)
		m.add_meta(match1,(2,2),core.M_OCCUPIED)
		m.add_match(match2)
		m.add_meta(match2,(4,4),core.M_OCCUPIED)
		m.remove_match(match1)
		self.assertTrue(match2 in m.get_all_matches())
		self.assertEquals({(4,4):core.M_OCCUPIED}, m.get_meta_for(match2))
		self.assertTrue(match2 in m.get_occupants_at((4,4)))
		
	def test_remove_match_allows_non_existant_match(self):
		m = main.MatchLookup()
		match = object()
		m.remove_match(match)	
		
	def test_remove_coocupants_removes_matches_occupying(self):
		m = main.MatchLookup()
		match1 = object()
		m.add_match(match1)
		m.add_meta(match1,(2,2),core.M_OCCUPIED)
		match2 = object()
		m.add_meta(match2,(2,2),core.M_OCCUPIED)
		m.remove_cooccupants(match1)
		self.assertTrue( not match2 in m.get_all_matches() )
		
	def test_remove_cooccupants_remove_match_itself(self):
		m = main.MatchLookup()
		match = object()
		m.add_match(match)
		m.add_meta(match,(2,2),core.M_OCCUPIED)
		m.remove_cooccupants(match)
		self.assertTrue( not match in m.get_all_matches() )
		
	def test_remove_cooccupants_ignores_other_meta_flags(self):
		m = main.MatchLookup()
		match1 = object()
		m.add_match(match1)
		m.add_meta(match1,(2,2),core.M_OCCUPIED)
		match2 = object()
		m.add_match(match2)
		m.add_meta(match2,(2,2),core.M_BOX_START_E)
		m.remove_cooccupants(match1)
		self.assertTrue( match2 in m.get_all_matches() )
	
	def test_remove_cooccupants_ignores_occupants_elsewhere(self):
		m = main.MatchLookup()
		match1 = object()
		m.add_match(match1)
		m.add_meta(match1,(2,2),core.M_OCCUPIED)
		match2 = object()
		m.add_match(match2)
		m.add_meta(match2,(3,3),core.M_OCCUPIED)
		m.remove_cooccupants(match1)
		self.assertTrue( match2 in m.get_all_matches() )
		
	def test_remove_cooccupants_allows_non_existant_match(self):
		m = main.MatchLookup()
		match = object()
		m.remove_cooccupants(match)


class TestSvgOutput(unittest.TestCase):
	
	def do_output(self, content, prefs=main.OutputPrefs((0,0,0),(1,1,1),24), 
			size=(200,200)):
		s = io.BytesIO()
		main.SvgOutput.output(main.Diagram(size,content),s,prefs)
		return xml.dom.minidom.parseString(s.getvalue())
	
	def child_elements(self,node):
		return filter(lambda x: x.nodeType==xml.dom.minidom.Node.ELEMENT_NODE, node.childNodes)
	
	def test_creates_root_element(self):
		e = self.do_output([]).documentElement
		self.assertEquals("svg", e.tagName)
		self.assertEquals("1.1", e.getAttribute("version"))
		self.assertEquals("http://www.w3.org/2000/svg", e.namespaceURI)
			
	def test_creates_background(self):
		c = self.child_elements(self.do_output([],main.OutputPrefs(),
			(100,300)).documentElement)
		self.assertEquals(1, len(c))
		self.assertEquals("rect",c[0].tagName)
		self.assertEquals(0, float(c[0].getAttribute("x")))
		self.assertEquals(0, float(c[0].getAttribute("y")))
		self.assertEquals(1200, float(c[0].getAttribute("width")))
		self.assertEquals(7200, float(c[0].getAttribute("height")))
		self.assertEquals("none", c[0].getAttribute("stroke"))
		self.assertEquals("rgb(255,255,255)",c[0].getAttribute("fill"))
		self.assertEquals(1,float(c[0].getAttribute("fill-opacity")))
		
	def test_background_colour(self):
		b = self.child_elements(self.do_output([],main.OutputPrefs((0,0,0),(1,0,0.5),24),
				(10,10),).documentElement)[0]
		self.assertEquals("rgb(255,0,127)",b.getAttribute("fill"))
		
	def test_background_charheight(self):
		b = self.child_elements(self.do_output([],
			main.OutputPrefs((1,1,1),(0,0,0),30),(100,300)).documentElement)[0]
		self.assertEquals(1500, float(b.getAttribute("width")))
		self.assertEquals(9000, float(b.getAttribute("height")))
			
	def test_handles_line(self):
		e = self.do_output([core.Line(a=(0,0),b=(1,1),z=1,stroke=(1,0,0),salpha=1.0,
			w=1,stype=core.STROKE_SOLID)]).documentElement
		ch = self.child_elements(e)
		self.assertEquals(2, len(ch))
		self.assertEquals("line", ch[1].tagName)
		
	def test_line_coordinates(self):
		l = self.child_elements(self.do_output([core.Line(a=(1,2),b=(3,4),z=1,
			stroke=(1,0,0),salpha=1.0,w=1,stype=core.STROKE_SOLID)]).documentElement)[1]
		self.assertEquals(12, float(l.getAttribute("x1")))
		self.assertEquals(48, float(l.getAttribute("y1")))
		self.assertEquals(36, float(l.getAttribute("x2")))
		self.assertEquals(96, float(l.getAttribute("y2")))
		
	def test_line_coordinates_charsize(self):
		l = self.child_elements(self.do_output([core.Line(a=(1,2),b=(3,4),z=1,
				stroke=(1,0,0),salpha=1.0,w=1,stype=core.STROKE_SOLID)],
			main.OutputPrefs(charheight=36)).documentElement)[1]
		self.assertEquals(18, float(l.getAttribute("x1")))
		self.assertEquals(72, float(l.getAttribute("y1")))
		self.assertEquals(54, float(l.getAttribute("x2")))
		self.assertEquals(144, float(l.getAttribute("y2")))
		
	def test_line_stroke_colour(self):
		l = self.child_elements(self.do_output([core.Line(a=(1,2),b=(3,4),z=1,stroke=(1,0.5,0),
			salpha=1.0,w=1,stype=core.STROKE_SOLID)]).documentElement)[1]
		self.assertEquals("rgb(255,127,0)", l.getAttribute("stroke"))
		
	def test_line_special_stroke_colour(self):
		l = self.child_elements(self.do_output([core.Line(a=(1,2),b=(3,4),z=1,stroke=core.C_FOREGROUND,
				salpha=1.0,w=1,stype=core.STROKE_SOLID)],
			main.OutputPrefs((1,0.25,1),(0,0.5,0))).documentElement)[1]
		self.assertEquals("rgb(255,63,255)", l.getAttribute("stroke"))
		
	def test_line_no_stroke(self):
		l = self.child_elements(self.do_output([core.Line(a=(1,2),b=(3,4),z=1,stroke=None,
			salpha=1.0,w=1,stype=core.STROKE_SOLID)]).documentElement)[1]
		self.assertEquals("none", l.getAttribute("stroke"))
	
	def test_line_stroke_alpha(self):
		l = self.child_elements(self.do_output([core.Line(a=(1,2),b=(3,4),z=1,stroke=(1,0,0),
			salpha=0.75,w=1,stype=core.STROKE_SOLID)]).documentElement)[1]
		self.assertEquals(0.75,float(l.getAttribute("stroke-opacity")))
	
	def test_line_stroke_width(self):
		l = self.child_elements(self.do_output([core.Line(a=(1,2),b=(3,4),z=1,stroke=(1,0,0),
			salpha=1.0,w=2,stype=core.STROKE_SOLID)]).documentElement)[1]
		self.assertEquals(5, float(l.getAttribute("stroke-width")))
		
	def test_line_stroke_solid(self):
		l = self.child_elements(self.do_output([core.Line(a=(1,2),b=(3,4),z=1,stroke=(1,0,0),
			salpha=1.0,w=1,stype=core.STROKE_SOLID)]).documentElement)[1]
		self.assertEquals("", l.getAttribute("stroke-dasharray"))	
	
	def test_line_stroke_dashed(self):
		l = self.child_elements(self.do_output([core.Line(a=(1,2),b=(3,4),z=1,stroke=(1,0,0),
			salpha=1.0,w=1,stype=core.STROKE_DASHED)]).documentElement)[1]
		self.assertEquals("8,8", l.getAttribute("stroke-dasharray"))
		
	def test_line_z(self):
		ls = self.child_elements(self.do_output([
				core.Line(a=(1,2),b=(3,4),z=5,stroke=(0,1,0),salpha=1.0,w=1,stype=core.STROKE_SOLID),
				core.Line(a=(9,8),b=(7,6),z=1,stroke=(0,0,1),salpha=1.0,w=1,stype=core.STROKE_SOLID),
				core.Line(a=(6,6),b=(6,5),z=3,stroke=(1,0,0),salpha=1.0,w=1,stype=core.STROKE_SOLID), 
		]).documentElement)
		self.assertEquals("rgb(0,0,255)",ls[1].getAttribute("stroke"))
		self.assertEquals("rgb(255,0,0)",ls[2].getAttribute("stroke"))
		self.assertEquals("rgb(0,255,0)",ls[3].getAttribute("stroke"))
		
	def test_handles_rectangle(self):
		ch = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,4),z=1,
			stroke=(1,0,0),salpha=1.0,w=1,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0)]).documentElement)
		self.assertEquals(2, len(ch))
		self.assertEquals("rect", ch[1].tagName)
		
	def test_rect_coordinates(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke=(1,0,0),salpha=1.0,w=1,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0)]).documentElement)[1]
		self.assertEquals(12,float(r.getAttribute("x")))
		self.assertEquals(48,float(r.getAttribute("y")))
		self.assertEquals(24,float(r.getAttribute("width")))
		self.assertEquals(72,float(r.getAttribute("height")))
	
	def test_rect_coordinates_charheight(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
				stroke=(1,0,0),salpha=1.0,w=1,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0)],
			main.OutputPrefs(charheight=36)).documentElement)[1]
		self.assertEquals(18,float(r.getAttribute("x")))
		self.assertEquals(72,float(r.getAttribute("y")))
		self.assertEquals(36,float(r.getAttribute("width")))
		self.assertEquals(108,float(r.getAttribute("height")))
	
	def test_rect_stroke_colour(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke=(1,0,0.25),salpha=1.0,w=1,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0)]).documentElement)[1]
		self.assertEquals("rgb(255,0,63)", r.getAttribute("stroke"))
	
	def test_rect_special_stroke_colour(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke=core.C_FOREGROUND,salpha=1.0,w=1,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0)],
			main.OutputPrefs((1,1,0),(0,0,0.25))).documentElement)[1]
		self.assertEquals("rgb(255,255,0)", r.getAttribute("stroke"))
	
	def test_rect_no_stroke(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke=None,salpha=1.0,w=1,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0)]).documentElement)[1]
		self.assertEquals("none", r.getAttribute("stroke"))
		
	def test_rect_stroke_alpha(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke=(1,0,0),salpha=0.75,w=1,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0)]).documentElement)[1]
		self.assertEquals(0.75,float(r.getAttribute("stroke-opacity")))
		
	def test_rect_stroke_width(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke=(1,0,0),salpha=1.0,w=3,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0)]).documentElement)[1]
		self.assertEquals(7.5, float(r.getAttribute("stroke-width")))
		
	def test_rect_stroke_solid(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke=(1,0,0),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0)]).documentElement)[1]
		self.assertEquals("", r.getAttribute("stroke-dasharray"))
		
	def test_rect_stroke_dashed(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke=(1,0,0),salpha=1.0,w=2,stype=core.STROKE_DASHED,fill=(0,0,1),falpha=1.0)]).documentElement)[1]
		self.assertEquals("8,8", r.getAttribute("stroke-dasharray"))
		
	def test_rect_fill_colour(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke=(1,0,0),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(0,0,0.25),falpha=1.0)]).documentElement)[1]
		self.assertEquals("rgb(0,0,63)",r.getAttribute("fill"))
		
	def test_rect_special_fill_colour(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
				stroke=(1,0,0),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=core.C_BACKGROUND,falpha=1.0)],
			main.OutputPrefs((0.25,0.25,0),(0.1,0.1,0.1))).documentElement)[1]
		self.assertEquals("rgb(25,25,25)",r.getAttribute("fill"))
		
	def test_rect_no_fill(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke=(1,0,0),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=None,falpha=1.0)]).documentElement)[1]
		self.assertEquals("none",r.getAttribute("fill"))
		
	def test_rect_fill_alpha(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke=(1,0,0),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=0.75)]).documentElement)[1]
		self.assertEquals(0.75,float(r.getAttribute("fill-opacity")))
		
	def test_rect_z(self):
		rs = self.child_elements(self.do_output([
			core.Rectangle(a=(1,2),b=(3,4),z=5,stroke=(1,0,0),salpha=1.0,w=2,
				stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0),
			core.Rectangle(a=(9,9),b=(8,8),z=1,stroke=(0,1,0),salpha=1.0,w=2,
				stype=core.STROKE_SOLID,fill=(1,0,0),falpha=1.0),
			core.Rectangle(a=(3,4),b=(5,6),z=3,stroke=(0,0,1),salpha=1.0,w=2,
				stype=core.STROKE_SOLID,fill=(0,1,0),falpha=1.0), 
		]).documentElement)
		self.assertEquals("rgb(0,255,0)", rs[1].getAttribute("stroke")) 
		self.assertEquals("rgb(0,0,255)", rs[2].getAttribute("stroke"))
		self.assertEquals("rgb(255,0,0)", rs[3].getAttribute("stroke"))
		
	def test_handles_ellipse(self):
		ch = self.child_elements(self.do_output([ core.Ellipse(a=(2,3),b=(5,1),z=1,
			stroke=(1,0,0),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0) ]).documentElement)
		self.assertEquals(2, len(ch))
		self.assertEquals("ellipse", ch[1].tagName)
		
	def test_ellipse_coordinates(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke=(1,0,0),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0) ]).documentElement)[1]
		self.assertEquals(42, float(e.getAttribute("cx")))
		self.assertEquals(48, float(e.getAttribute("cy")))
		self.assertEquals(18, float(e.getAttribute("rx")))
		self.assertEquals(24, float(e.getAttribute("ry")))
		
	def test_ellipse_coordinates_charheight(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
				stroke=(1,0,0),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0) ],
			main.OutputPrefs(charheight=50)).documentElement)[1]
		self.assertEquals(87, float(e.getAttribute("cx")))
		self.assertEquals(100, float(e.getAttribute("cy")))
		self.assertEquals(37, float(e.getAttribute("rx")))
		self.assertEquals(50, float(e.getAttribute("ry")))
		
	def test_ellipse_stroke_colour(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke=(1,0.5,0),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0) ]).documentElement)[1]
		self.assertEquals("rgb(255,127,0)",e.getAttribute("stroke"))
		
	def test_ellipse_special_stroke_colour(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke=core.C_BACKGROUND,salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0) ],
			main.OutputPrefs((0,0,1),(0.5,0.25,0))).documentElement)[1]
		self.assertEquals("rgb(127,63,0)",e.getAttribute("stroke"))
		
	def test_ellipse_no_stroke(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke=None,salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0) ]).documentElement)[1]
		self.assertEquals("none",e.getAttribute("stroke"))
		
	def test_ellipse_stroke_alpha(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke=(1,0,0),salpha=0.75,w=2,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0) ]).documentElement)[1]
		self.assertEquals(0.75,float(e.getAttribute("stroke-opacity")))
		
	def test_ellipse_stroke_width(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke=(1,0,0),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0) ]).documentElement)[1]
		self.assertEquals(5, float(e.getAttribute("stroke-width")))
		
	def test_ellipse_stroke_solid(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke=(1,0,0),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0) ]).documentElement)[1]
		self.assertEquals("", e.getAttribute("stroke-dasharray"))
		
	def test_ellipse_stroke_dashed(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke=(1,0,0),salpha=1.0,w=2,stype=core.STROKE_DASHED,fill=(0,0,1),falpha=1.0) ]).documentElement)[1]
		self.assertEquals("8,8", e.getAttribute("stroke-dasharray"))
		
	def test_ellipse_fill_colour(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke=(1,0,0),salpha=10,w=2,stype=core.STROKE_SOLID,fill=(1,0,1),falpha=1.0) ]).documentElement)[1]
		self.assertEquals("rgb(255,0,255)", e.getAttribute("fill"))
		
	def test_ellipse_special_fill_colour(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
				stroke=(1,0,0),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=core.C_FOREGROUND,falpha=1.0) ],
			main.OutputPrefs((1,0.9,0.9),(0,0,0))).documentElement)[1]
		self.assertEquals("rgb(255,229,229)",e.getAttribute("fill"))
		
	def test_ellipse_no_fill(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke=(1,0,0),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=None,falpha=1.0) ]).documentElement)[1]
		self.assertEquals("none", e.getAttribute("fill"))
		
	def test_ellipse_fill_alpha(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke=(1,0,0),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=0.75) ]).documentElement)[1]
		self.assertEquals(0.75, float(e.getAttribute("fill-opacity")))
		
	def test_ellipse_z(self):
		ch = self.child_elements(self.do_output([ 
			core.Ellipse(a=(2,1),b=(5,3),z=3,stroke=(1,0,0),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0),
			core.Ellipse(a=(2,2),b=(1,1),z=10,stroke=(0,0,1),salpha=1.0,w=3,stype=core.STROKE_SOLID,fill=(0,1,0),falpha=1.0),
			core.Ellipse(a=(3,3),b=(4,5),z=1,stroke=(0,1,0),salpha=1.0,w=1,stype=core.STROKE_SOLID,fill=(1,0,0),falpha=1.0) ]).documentElement)
		self.assertEquals(4, len(ch))
		self.assertEquals("rgb(0,255,0)", ch[1].getAttribute("stroke"))
		self.assertEquals("rgb(255,0,0)", ch[2].getAttribute("stroke"))
		self.assertEquals("rgb(0,0,255)", ch[3].getAttribute("stroke"))
		
	def test_handles_arc(self):
		ch = self.child_elements(self.do_output([ core.Arc(a=(2,5),b=(3,4),z=1,
			start=-math.pi/2,end=math.pi/4,stroke=(1,0,0),salpha=1.0,w=1,stype=core.STROKE_SOLID,
			fill=(0,0,1),falpha=1.0) ]).documentElement)
		self.assertEquals(2, len(ch))
		self.assertEquals("path", ch[1].tagName)
		
	def test_arc_coordinates(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
			start=-math.pi,end=math.pi/2,stroke=(1,0,0),salpha=1.0,w=1,
			stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0) ]).documentElement)[1]
		self.assertEquals("M 24,120 A 6,24 0 1 1 30,144", a.getAttribute("d"))
		
	def test_arc_coordinates_charheight(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
				start=-math.pi,end=math.pi/2,stroke=(1,0,0),salpha=1.0,w=1,
				stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0) ],
			main.OutputPrefs(charheight=50)).documentElement)[1]
		self.assertEquals("M 50,250 A 12,50 0 1 1 62,300", a.getAttribute("d"))
		
	def test_arc_stroke_colour(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
			start=-math.pi,end=math.pi/2,stroke=(1,0,0),salpha=1.0,w=1,
			stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0) ]).documentElement)[1]
		self.assertEquals("rgb(255,0,0)", a.getAttribute("stroke"))
		
	def test_arc_special_stroke_colour(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
				start=-math.pi,end=math.pi/2,stroke=core.C_FOREGROUND,salpha=1.0,
				w=1,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0) ],
			main.OutputPrefs((0.25,0.25,0.25),(0.25,0.25,0))).documentElement)[1]
		self.assertEquals("rgb(63,63,63)",a.getAttribute("stroke"))
		
	def test_arc_no_stroke(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
			start=-math.pi,end=math.pi/2,stroke=None,salpha=1.0,w=1,
			stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0) ]).documentElement)[1]
		self.assertEquals("none", a.getAttribute("stroke"))
		
	def test_arc_stroke_alpha(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
			start=-math.pi,end=math.pi/2,stroke=(1,0,0),salpha=0.75,w=1,
			stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0) ]).documentElement)[1]
		self.assertEquals(0.75, float(a.getAttribute("stroke-opacity")))
		
	def test_arc_stroke_width(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
			start=-math.pi,end=math.pi/2,stroke=(1,0,0),salpha=1.0,w=1,
			stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0) ]).documentElement)[1]
		self.assertEquals(2.5, float(a.getAttribute("stroke-width")))
		
	def test_arc_stroke_solid(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
			start=-math.pi,end=math.pi/2,stroke=(1,0,0),salpha=1.0,w=1,
			stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0) ]).documentElement)[1]
		self.assertEquals("", a.getAttribute("stroke-dasharray"))
		
	def test_arc_stroke_dashed(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
			start=-math.pi,end=math.pi/2,stroke=(1,0,0),salpha=1.0,w=1,
			stype=core.STROKE_DASHED,fill=(0,0,1),falpha=1.0) ]).documentElement)[1]
		self.assertEquals("8,8", a.getAttribute("stroke-dasharray"))
	
	def test_arc_fill_colour(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
			start=-math.pi,end=math.pi/2,stroke=(1,0,0),salpha=1.0,w=1,
			stype=core.STROKE_SOLID,fill=(0.5,0,0.5),falpha=1.0) ]).documentElement)[1]
		self.assertEquals("rgb(127,0,127)", a.getAttribute("fill"))
		
	def test_arc_special_fill_colour(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
				start=-math.pi,end=math.pi/2,stroke=(1,0,0),salpha=1.0,w=1,
				stype=core.STROKE_SOLID,fill=core.C_FOREGROUND,falpha=1.0) ],
			main.OutputPrefs((0,1,0),(1,0,1))).documentElement)[1]
		self.assertEquals("rgb(0,255,0)", a.getAttribute("fill"))
		
	def test_arc_no_fill(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
			start=-math.pi,end=math.pi/2,stroke=(1,0,0),salpha=1.0,w=1,
			stype=core.STROKE_SOLID,fill=None,falpha=1.0) ]).documentElement)[1]
		self.assertEquals("none", a.getAttribute("fill"))
		
	def test_arc_fill_alpha(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
			start=-math.pi,end=math.pi/2,stroke=(1,0,0),salpha=1.0,w=1,
			stype=core.STROKE_SOLID,fill=(0,0,1),falpha=0.75) ]).documentElement)[1]
		self.assertEquals(0.75, float(a.getAttribute("fill-opacity")))
		
	def test_arc_z(self):
		ch = self.child_elements(self.do_output([ 
				core.Arc(a=(2,4),b=(3,6),z=5,start=-math.pi,end=math.pi/2,
					stroke=(1,0,0),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(0,0,1),falpha=1.0),
				core.Arc(a=(1,2),b=(4,5),z=20,start=-math.pi/2,end=math.pi,
					stroke=(0,0,1),salpha=1.0,w=2,stype=core.STROKE_DASHED,fill=(1,0,0),falpha=1.0),
				core.Arc(a=(3,4),b=(7,1),z=1,start=math.pi,end=math.pi*2,stroke=(0,1,0),
					salpha=1.0,w=1,stype=core.STROKE_SOLID,fill=(1,0.5,0),falpha=1.0), 
		]).documentElement)
		self.assertEquals(4, len(ch))
		self.assertEquals("rgb(0,255,0)", ch[1].getAttribute("stroke"))
		self.assertEquals("rgb(255,0,0)", ch[2].getAttribute("stroke"))
		self.assertEquals("rgb(0,0,255)", ch[3].getAttribute("stroke"))

	def test_handles_polygon(self):
		ch = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
			z=1,stroke=(1,0.5,0),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(1,0,0),
			falpha=1.0) ]).documentElement)
		self.assertEquals(2, len(ch))
		self.assertEquals("polygon", ch[1].tagName)
		
	def test_polygon_coordinates(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
			z=1,stroke=(1,0.5,0),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(1,0,0),
			falpha=1.0) ]).documentElement)[1]
		self.assertEquals("12,48 12,72 24,48", p.getAttribute("points"))
		
	def test_polygon_coordinates_charheight(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
				z=1,stroke=(1,0.5,0),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(1,0,0),
				falpha=1.0) ],
			main.OutputPrefs(charheight=50)).documentElement)[1]
		self.assertEquals("25,100 25,150 50,100", p.getAttribute("points"))
		
	def test_polygon_stroke_colour(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
			z=1,stroke=(1,0.5,0),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(1,0,0),
			falpha=1.0) ]).documentElement)[1]
		self.assertEquals("rgb(255,127,0)", p.getAttribute("stroke"))
		
	def test_polygon_special_stroke_colour(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
				z=1,stroke=core.C_FOREGROUND,salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(1,0,0),
				falpha=1.0) ],
			main.OutputPrefs((0,0,0.1),(0.2,0,0.2))).documentElement)[1]
		self.assertEquals("rgb(0,0,25)", p.getAttribute("stroke"))
		
	def test_polygon_no_stroke(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
			z=1,stroke=None,salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(1,0,0),
			falpha=1.0) ]).documentElement)[1]
		self.assertEquals("none", p.getAttribute("stroke"))
		
	def test_polygon_stroke_alpha(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
			z=1,stroke=(1,0.5,0),salpha=0.75,w=2,stype=core.STROKE_SOLID,fill=(1,0,0),
			falpha=1.0) ]).documentElement)[1]
		self.assertEquals(0.75, float(p.getAttribute("stroke-opacity")))
	
	def test_polygon_stroke_width(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
			z=1,stroke=(0.1,0,0.1),salpha=1.0,w=2,stype=core.STROKE_SOLID, fill=(1,0,0),
			falpha=1.0) ]).documentElement)[1]
		self.assertEquals(5, float(p.getAttribute("stroke-width")))
		
	def test_polygon_stroke_solid(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
			z=1,stroke=(0.1,0,0.1),salpha=1.0,w=2,stype=core.STROKE_SOLID, fill=(1,0,0),
			falpha=1.0) ]).documentElement)[1]
		self.assertEquals("", p.getAttribute("stroke-dasharray"))
		
	def test_polygon_stroke_dashed(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
			z=1,stroke=(0.1,0,0.1),salpha=1.0,w=2,stype=core.STROKE_DASHED,fill=(1,0,0),
			falpha=1.0) ]).documentElement)[1]
		self.assertEquals("8,8", p.getAttribute("stroke-dasharray"))
		
	def test_polygon_fill_colour(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
			z=1,stroke=(0.1,0,0.1),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=(1,1,0),
			falpha=1.0) ]).documentElement)[1]
		self.assertEquals("rgb(255,255,0)", p.getAttribute("fill"))
		
	def test_polygon_special_fill_colour(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
				z=1,stroke=(0.1,0,0.1),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=core.C_FOREGROUND,
				falpha=1.0) ],
			main.OutputPrefs((0,1,0),(1,0,1)) ).documentElement)[1]
		self.assertEquals("rgb(0,255,0)", p.getAttribute("fill"))
		
	def test_polygon_no_fill(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
			z=1,stroke=(1,0,1),salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=None,
			falpha=1.0) ]).documentElement)[1]
		self.assertEquals("none", p.getAttribute("fill"))
		
	def test_polygon_z(self):
		ch = self.child_elements(self.do_output([ 
			core.Polygon(points=((1,2),(1,3),(2,2)),z=1,stroke=(1,0,1),salpha=1.0,
				w=2,stype=core.STROKE_SOLID,fill=(1,0,0),falpha=1.0),
			core.Polygon(points=((1,2),(1,3),(2,2)),z=3,stroke=(0,1,0),salpha=1.0,
				w=3,stype=core.STROKE_DASHED,fill=(1,0,0),falpha=1.0),
			core.Polygon(points=((1,2),(1,3),(2,2)),z=2,stroke=(1,0.5,0),salpha=1.0,
				w=1,stype=core.STROKE_SOLID,fill=(1,0,0),falpha=1.0), 
		]).documentElement)
		self.assertEquals(4, len(ch))
		self.assertEquals("rgb(255,0,255)", ch[1].getAttribute("stroke"))
		self.assertEquals("rgb(255,127,0)", ch[2].getAttribute("stroke"))
		self.assertEquals("rgb(0,255,0)", ch[3].getAttribute("stroke"))
	
	def test_handles_quadcurve(self):
		ch = self.child_elements(self.do_output([ core.QuadCurve(a=(1,2),b=(3,5),
			c=(4,3),z=1,stroke=(1,0,1),salpha=1.0,w=2,stype=core.STROKE_SOLID) ]).documentElement)
		self.assertEquals(2, len(ch))
		self.assertEquals("path", ch[1].tagName)
		
	def test_quadcurve_coordinates(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(a=(1,2),b=(3,5),c=(4,3),
			z=1,stroke=(1,0,1),salpha=1.0,w=2,stype=core.STROKE_SOLID) ]).documentElement)[1]
		self.assertEquals("M 12,48 Q 48,72 36,120",q.getAttribute("d"))
		
	def test_quadcurve_coordinates_charheight(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(a=(1,2),b=(3,5),c=(4,3),
				z=1,stroke=(1,0,1),salpha=1.0,w=2,stype=core.STROKE_SOLID) ],
			main.OutputPrefs(charheight=50)).documentElement)[1]
		self.assertEquals("M 25,100 Q 100,150 75,250",q.getAttribute("d"))
		
	def test_quadcurve_stroke_colour(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(a=(1,2),b=(3,5),c=(4,3),
			z=1,stroke=(1,0,1),salpha=1.0,w=2,stype=core.STROKE_SOLID) ]).documentElement)[1]
		self.assertEquals("rgb(255,0,255)", q.getAttribute("stroke"))
		
	def test_quadcurve_special_stroke_colour(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(a=(1,2),b=(3,5),c=(4,3),
				z=1,stroke=core.C_FOREGROUND,salpha=1.0,w=2,stype=core.STROKE_SOLID) ],
			main.OutputPrefs((0.25,0,0),(0,0.25,0))).documentElement)[1]
		self.assertEquals("rgb(63,0,0)",q.getAttribute("stroke"))
		
	def test_quadcurve_no_stroke(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(a=(1,2),b=(3,5),c=(4,3),
			z=1,stroke=None,salpha=1.0,w=2,stype=core.STROKE_SOLID) ]).documentElement)[1]
		self.assertEquals("none", q.getAttribute("stroke"))
		
	def test_quadcurve_stroke_alpha(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(a=(1,2),b=(3,5),c=(4,3),
			z=1,stroke=(0.1,0,0.1),salpha=0.75,w=2,stype=core.STROKE_SOLID) ]).documentElement)[1]
		self.assertEquals(0.75, float(q.getAttribute("stroke-opacity")))
		
	def test_quadcurve_stroke_width(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(a=(1,2),b=(3,5),c=(4,3),
			z=1,stroke=(0.1,0,0.1),salpha=1.0,w=2,stype=core.STROKE_SOLID) ]).documentElement)[1]
		self.assertEquals(5, float(q.getAttribute("stroke-width")))
		
	def test_quadcurve_stroke_solid(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(a=(1,2),b=(3,5),c=(4,3),
			z=1,stroke=(0.1,0,0.1),salpha=1.0,w=2,stype=core.STROKE_SOLID) ]).documentElement)[1]
		self.assertEquals("", q.getAttribute("stroke-dasharray"))
		
	def test_quadcurve_stroke_dashed(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(a=(1,2),b=(3,5),c=(4,3),
			z=1,stroke=(0.1,0,0.1),salpha=1.0,w=2,stype=core.STROKE_DASHED) ]).documentElement)[1]
		self.assertEquals("8,8", q.getAttribute("stroke-dasharray"))
		
	def test_quadcurve_z(self):
		ch = self.child_elements(self.do_output([ 
			core.QuadCurve(a=(1,2),b=(3,5),c=(4,3),z=1,stroke=(0.1,0,0.1),salpha=1.0,
				w=2,stype=core.STROKE_SOLID),
			core.QuadCurve(a=(0,1),b=(2,4),c=(3,4),z=3,stroke=(0,1,0),salpha=1.0,
				w=3,stype=core.STROKE_DASHED),
			core.QuadCurve(a=(2,3),b=(4,0),c=(4,5),z=2,stroke=(1,0.5,0),salpha=1.0,
				w=1,stype=core.STROKE_SOLID), 
		]).documentElement)
		self.assertEquals(4, len(ch))
		self.assertEquals("rgb(25,0,25)", ch[1].getAttribute("stroke"))
		self.assertEquals("rgb(255,127,0)", ch[2].getAttribute("stroke"))
		self.assertEquals("rgb(0,255,0)", ch[3].getAttribute("stroke"))
		
	def test_handles_text(self):
		ch = self.child_elements(self.do_output([ core.Text(pos=(3,4),z=1,text="!",
			colour=(1,0,0),alpha=1.0,size=1) ]).documentElement)
		self.assertEquals(2, len(ch))
		self.assertEquals("text", ch[1].tagName)
		self.assertEquals("monospace", ch[1].getAttribute("font-family"))
		
	def test_text_coordinates(self):
		t = self.child_elements(self.do_output([ core.Text(pos=(3,4),z=1,text="!",
			colour=(1,0,0),alpha=1.0,size=1) ]).documentElement)[1]
		self.assertEquals(36, float(t.getAttribute("x")))
		self.assertEquals(114,float(t.getAttribute("y")))
		
	def test_text_coordinates_charheight(self):
		t = self.child_elements(self.do_output([ core.Text(pos=(3,4),z=1,text="!",
				colour=(1,0,0),alpha=1.0,size=1) ],
			main.OutputPrefs(charheight=50)).documentElement)[1]
		self.assertEquals(75, float(t.getAttribute("x")))
		self.assertEquals(237,float(t.getAttribute("y")))
		
	def test_text_content(self):
		t = self.child_elements(self.do_output([ core.Text(pos=(3,4),z=1,text="!",
			colour=(1,0,0),alpha=1.0,size=1) ]).documentElement)[1]
		self.assertEquals(1, len(t.childNodes))
		self.assertEquals("!", t.childNodes[0].nodeValue)
		
	def test_text_colour(self):
		t = self.child_elements(self.do_output([ core.Text(pos=(3,4),z=1,text="!",
			colour=(1,0,0),alpha=1.0,size=1) ]).documentElement)[1]
		self.assertEquals("rgb(255,0,0)", t.getAttribute("fill"))
		
	def test_text_special_colour(self):
		t = self.child_elements(self.do_output([ core.Text(pos=(3,4),z=1,text="!",
				colour=core.C_BACKGROUND,alpha=1.0,size=1) ],
			main.OutputPrefs((1,0.5,0),(1,1,0))).documentElement)[1]
		self.assertEquals("rgb(255,255,0)", t.getAttribute("fill"))
		
	def test_text_alpha(self):
		t = self.child_elements(self.do_output([ core.Text(pos=(3,4),z=1,text="!",
			colour=(1,0,0), alpha=0.75, size=1) ]).documentElement)[1]
		self.assertEquals(0.75, float(t.getAttribute("fill-opacity")))
		
	def test_text_size(self):
		t = self.child_elements(self.do_output([ core.Text(pos=(3,4),z=1,text="!",
			colour=(1,0,0),alpha=1.0, size=1.25) ]).documentElement)[1]
		self.assertEquals(20, float(t.getAttribute("font-size")))
	
	def test_text_size_charheight(self):
		t = self.child_elements(self.do_output([ core.Text(pos=(3,4),z=1,text="!",
				colour=(1,0,0),alpha=1.0, size=1.25) ],
			main.OutputPrefs(charheight=50)).documentElement)[1]
		self.assertEquals(41, float(t.getAttribute("font-size")))
		
	def test_text_z(self):
		ch = self.child_elements(self.do_output([ 
			core.Text(pos=(3,4),z=4,text="!",colour=(1,0,0),alpha=1.0,size=1),
			core.Text(pos=(2,2),z=12,text="?",colour=(0,0,1),alpha=1.0,size=1),
			core.Text(pos=(4,5),z=1,text="&",colour=(0,1,0),alpha=1.0,size=1), 
		]).documentElement)
		self.assertEquals(4, len(ch))
		self.assertEquals("rgb(0,255,0)",ch[1].getAttribute("fill"))
		self.assertEquals("rgb(255,0,0)",ch[2].getAttribute("fill"))
		self.assertEquals("rgb(0,0,255)",ch[3].getAttribute("fill"))


class TestProcessDiagram(unittest.TestCase):


	def test_returns_diagram(self):
		d = main.process_diagram("",[])
		self.assertTrue( isinstance(d, main.Diagram) )
	
	def test_diagram_size(self):
		r = main.process_diagram(
			"012345\n"+
			"012345\n"+
			"012345", []).size
		self.assertEquals((6,3),r)
		
	def test_diagram_size_jagged(self):
		r = main.process_diagram(
			"0123\n"+
			"012345\n"+
			"01234", []).size
		self.assertEquals((6,3),r)
	
	def test_single_character_pattern_match(self):
		r = object()
		class SingleCharPattern(object):
			def test(self,curr):
				raise StopIteration()
			def render(self):
				return [ r ]
		result = main.process_diagram("a",[SingleCharPattern]).content
		self.assertEquals(4,len(result))
		self.assertEquals(r,result[0])
	
	def test_doesnt_output_rejected_pattern(self):
		class RejectingPattern(object):
			def test(self,curr):
				raise core.PatternRejected()
			def render(self):
				return [ object() ]
		result = main.process_diagram("a",[RejectingPattern]).content
		self.assertEquals(0,len(result))
		
	def test_multiple_character_pattern_match(self):
		r = object()
		class MultiCharPattern(object):
			i = 0
			def test(self,curr):
				if self.i >= 1: raise StopIteration()
				self.i += 1
				return core.M_NONE
			def render(self):
				return [ r ]
		result = main.process_diagram("a",[MultiCharPattern]).content
		self.assertEquals(3, len(result))
		self.assertEquals(r,result[0])
		self.assertEquals(r,result[1])
		
	def test_doesnt_output_unfinished_pattern(self):
		class NeverendingPattern(object):
			def test(self,curr):
				return core.M_NONE
			def render(self):
				return [ object() ]
		result = main.process_diagram("a",[NeverendingPattern]).content
		self.assertEquals(0,len(result))

	def test_multiple_matching_patterns(self):
		r1 = object()
		r2 = object()
		class Pattern1(object):
			def test(self,curr):
				raise StopIteration()
			def render(self):
				return [ r1 ]
		class Pattern2(object):
			def test(self,curr):
				raise StopIteration()
			def render(self):
				return [ r2 ]
		result = main.process_diagram("a",[Pattern1,Pattern2]).content
		self.assertTrue( r1 in result )
		self.assertTrue( r2 in result )

	def test_feeds_pattern_current_position(self):
		class PosStoringPattern(object):
			i = 0
			insts = []
			positions = []
			def __init__(self):
				PosStoringPattern.insts.append(self)
				self.positions = []
			def test(self,curr):
				self.positions.append((curr.col,curr.row))
				if self.i >= 1: raise core.PatternRejected()
				self.i += 1	
				return core.M_NONE
			def render(self):	
				return []
		main.process_diagram("a\nb\n",[PosStoringPattern])
		self.assertEquals(6,len(PosStoringPattern.insts))
		self.assertEquals([(0,-1),(0,0)],PosStoringPattern.insts[0].positions)
		self.assertEquals([(0,0),(1,0)],PosStoringPattern.insts[1].positions)
		self.assertEquals([(1,0),(0,1)],PosStoringPattern.insts[2].positions)
		self.assertEquals([(0,1),(1,1)],PosStoringPattern.insts[3].positions)
		self.assertEquals([(1,1),(0,2)],PosStoringPattern.insts[4].positions)
		self.assertEquals([(0,2)],PosStoringPattern.insts[5].positions)
		
	def test_feeds_pattern_current_character(self):
		class CharStoringPattern(object):
			i = 0
			insts = []
			chars = []
			def __init__(self):
				CharStoringPattern.insts.append(self)
				self.chars = []
			def test(self,curr):
				self.chars.append(curr.char)
				if self.i >= 1: raise core.PatternRejected()
				self.i += 1
				return core.M_NONE
			def render(self):
				return []
		main.process_diagram("ab",[CharStoringPattern])
		self.assertEquals(5,len(CharStoringPattern.insts))
		self.assertEquals([core.START_OF_INPUT,"a"],CharStoringPattern.insts[0].chars)
		self.assertEquals(["a","b"],CharStoringPattern.insts[1].chars)
		self.assertEquals(["b","\n"],CharStoringPattern.insts[2].chars)
		self.assertEquals(["\n",core.END_OF_INPUT],CharStoringPattern.insts[3].chars)
		self.assertEquals([core.END_OF_INPUT],CharStoringPattern.insts[4].chars)
	
	def test_feeds_pattern_metadata_from_previous_patterns(self):
		class MetaPattern(object):
			i = 0
			def test(self,curr):
				if self.i >= 1: raise StopIteration()
				self.i += 1
				return core.M_BOX_START_E
			def render(self):
				return []
		class MetaStoringPattern(object):
			i = 0
			insts = []
			metas = []
			def __init__(self):
				MetaStoringPattern.insts.append(self)
				self.metas = []
			def test(self,curr):
				self.metas.append(curr.meta)
				if self.i >= 1: raise StopIteration()
				self.i += 1
				return core.M_NONE
			def render(self):
				return []
		main.process_diagram("ab",[MetaPattern,MetaStoringPattern])
		self.assertEquals(5, len(MetaStoringPattern.insts))
		self.assertEquals([core.M_BOX_START_E,core.M_BOX_START_E],MetaStoringPattern.insts[0].metas)
		self.assertEquals([core.M_BOX_START_E,core.M_BOX_START_E],MetaStoringPattern.insts[1].metas)
		self.assertEquals([core.M_BOX_START_E,core.M_BOX_START_E],MetaStoringPattern.insts[2].metas)
		self.assertEquals([core.M_BOX_START_E,core.M_NONE],MetaStoringPattern.insts[3].metas)
		self.assertEquals([core.M_NONE],MetaStoringPattern.insts[4].metas)
		
	def test_occupied_meta_disallows_overlapping_pattern_instances(self):
		class OccupyingPattern(object):
			id = 0
			i = 0
			def __init__(self):
				self.id = OccupyingPattern.id
				OccupyingPattern.id += 1
			def test(self,curr):
				if self.i >= 2: raise StopIteration()
				self.i += 1
				return core.M_OCCUPIED
			def render(self):
				return [ self.id ]
		result = main.process_diagram("abc",[OccupyingPattern]).content
		self.assertEquals([0,2], result)
	
	def test_doesnt_leave_metadata_for_failed_matches(self):
		r1 = object()
		r2 = object()
		class FailingMetaPattern(object):
			i = 0
			def test(self,curr):
				if self.i >= 1: raise core.PatternRejected()
				self.i += 1
				return core.M_BOX_START_E
			def render(self):
				return [r1]
		class MetaMatchingPattern(object):
			def test(self,curr):
				if curr.meta == core.M_BOX_START_E: 
					raise StopIteration()
				else:
					raise core.PatternRejected()
			def render(self):
				return [r2]
		result = main.process_diagram("abc",
				[FailingMetaPattern,MetaMatchingPattern]).content
		self.assertTrue( r1 not in result )
		self.assertTrue( r2 not in result )
	
	def test_metadata_not_passed_to_instances_of_same_pattern(self):
		class MetaMatchingPattern(object):
			i = 0
			def test(self,curr):
				if self.i >= 1: raise StopIteration()
				self.i += 1	
				if curr.char == "a" and curr.meta == core.M_NONE:
					return core.M_BOX_START_E
				else:
					raise core.PatternRejected()
			def render(self):
				return [ object() ]
		result = main.process_diagram("a a",[MetaMatchingPattern]).content
		self.assertEquals(2, len(result))		
		
	def test_reports_progress(self):
		class StubPattern(object):
			def test(self,curr): raise StopIteration
			def render(self): return []
		reporter = mock.Mock()
		main.process_diagram("aaaa",[StubPattern]*5,reporter)
		self.assertTrue( reporter.call_count > 2 )
	
	def test_progress_starts_with_zero(self):
		class StubPattern(object):
			def test(self,curr): raise StopIteration
			def render(self): return []
		reporter = mock.Mock()
		main.process_diagram("aaaa",[StubPattern]*5,reporter)
		self.assertEquals(((0.0,),{}),reporter.call_args_list[0])

	def test_progress_ends_with_one(self):
		class StubPattern(object):
			def test(self,curr): raise StopIteration
			def render(self): return []
		reporter = mock.Mock()
		main.process_diagram("aaaa",[StubPattern]*5,reporter)
		self.assertEquals(((1.0,),{}),reporter.call_args_list[-1])
	
	def test_progress_increases(self):
		class StubPattern(object):
			def test(self,curr): raise StopIteration
			def render(self): return []
		reporter = mock.Mock()
		main.process_diagram("aaaa",[StubPattern]*5,reporter)
		last = -1
		for args in reporter.call_args_list:
			self.assertTrue( args[0][0] > last )
			last = args[0][0]
		
if __name__ == "__main__":
	unittest.main()
