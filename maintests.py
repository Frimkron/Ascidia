#!/usr/bin/python2

import unittest
import core
import main
import io
import xml.dom.minidom
import math


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
	
	def do_output(self,items,prefs=main.OutputPrefs("black","white")):
		s = io.BytesIO()
		main.SvgOutput()._output(items,s,prefs)
		return xml.dom.minidom.parseString(s.getvalue())
	
	def child_elements(self,node):
		return filter(lambda x: x.nodeType==xml.dom.minidom.Node.ELEMENT_NODE, node.childNodes)
	
	def test_can_construct(self):	
		main.SvgOutput()
		
	def test_creates_root_element(self):
		e = self.do_output([]).documentElement
		self.assertEquals("svg", e.tagName)
		self.assertEquals("1.1", e.getAttribute("version"))
		self.assertEquals("http://www.w3.org/2000/svg", e.namespaceURI)
			
	def test_handles_line(self):
		e = self.do_output([core.Line(a=(0,0),b=(1,1),z=1,stroke="red",salpha=1.0,
			w=1,stype=core.STROKE_SOLID)]).documentElement
		ch = self.child_elements(e)
		self.assertEquals(1, len(ch))
		self.assertEquals("line", ch[0].tagName)
		
	def test_line_coordinates(self):
		l = self.child_elements(self.do_output([core.Line(a=(1,2),b=(3,4),z=1,
			stroke="red",salpha=1.0,w=1,stype=core.STROKE_SOLID)]).documentElement)[0]
		self.assertEquals(12, float(l.getAttribute("x1")))
		self.assertEquals(48, float(l.getAttribute("y1")))
		self.assertEquals(36, float(l.getAttribute("x2")))
		self.assertEquals(96, float(l.getAttribute("y2")))
		
	def test_line_stroke_colour(self):
		l = self.child_elements(self.do_output([core.Line(a=(1,2),b=(3,4),z=1,stroke="red",
			salpha=1.0,w=1,stype=core.STROKE_SOLID)]).documentElement)[0]
		self.assertEquals("red", l.getAttribute("stroke"))
		
	def test_line_special_stroke_colour(self):
		l = self.child_elements(self.do_output([core.Line(a=(1,2),b=(3,4),z=1,stroke=core.C_FOREGROUND,
				salpha=1.0,w=1,stype=core.STROKE_SOLID)],
			main.OutputPrefs("purple","green")).documentElement)[0]
		self.assertEquals("purple", l.getAttribute("stroke"))
		
	def test_line_no_stroke(self):
		l = self.child_elements(self.do_output([core.Line(a=(1,2),b=(3,4),z=1,stroke=None,
			salpha=1.0,w=1,stype=core.STROKE_SOLID)]).documentElement)[0]
		self.assertEquals("none", l.getAttribute("stroke"))
	
	def test_line_stroke_alpha(self):
		l = self.child_elements(self.do_output([core.Line(a=(1,2),b=(3,4),z=1,stroke="red",
			salpha=0.75,w=1,stype=core.STROKE_SOLID)]).documentElement)[0]
		self.assertEquals(0.75,float(l.getAttribute("stroke-opacity")))
	
	def test_line_stroke_width(self):
		l = self.child_elements(self.do_output([core.Line(a=(1,2),b=(3,4),z=1,stroke="red",
			salpha=1.0,w=2,stype=core.STROKE_SOLID)]).documentElement)[0]
		self.assertEquals(5, float(l.getAttribute("stroke-width")))
		
	def test_line_stroke_solid(self):
		l = self.child_elements(self.do_output([core.Line(a=(1,2),b=(3,4),z=1,stroke="red",
			salpha=1.0,w=1,stype=core.STROKE_SOLID)]).documentElement)[0]
		self.assertEquals("", l.getAttribute("stroke-dasharray"))	
	
	def test_line_stroke_dashed(self):
		l = self.child_elements(self.do_output([core.Line(a=(1,2),b=(3,4),z=1,stroke="red",
			salpha=1.0,w=1,stype=core.STROKE_DASHED)]).documentElement)[0]
		self.assertEquals("8,8", l.getAttribute("stroke-dasharray"))
		
	def test_line_z(self):
		ls = self.child_elements(self.do_output([
				core.Line(a=(1,2),b=(3,4),z=5,stroke="green",salpha=1.0,w=1,stype=core.STROKE_SOLID),
				core.Line(a=(9,8),b=(7,6),z=1,stroke="blue",salpha=1.0,w=1,stype=core.STROKE_SOLID),
				core.Line(a=(6,6),b=(6,5),z=3,stroke="red",salpha=1.0,w=1,stype=core.STROKE_SOLID), 
		]).documentElement)
		self.assertEquals("blue",ls[0].getAttribute("stroke"))
		self.assertEquals("red",ls[1].getAttribute("stroke"))
		self.assertEquals("green",ls[2].getAttribute("stroke"))
		
	def test_handles_rectangle(self):
		ch = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,4),z=1,
			stroke="red",salpha=1.0,w=1,stype=core.STROKE_SOLID,fill="blue",falpha=1.0)]).documentElement)
		self.assertEquals(1, len(ch))
		self.assertEquals("rect", ch[0].tagName)
		
	def test_rect_coordinates(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke="red",salpha=1.0,w=1,stype=core.STROKE_SOLID,fill="blue",falpha=1.0)]).documentElement)[0]
		self.assertEquals(12,float(r.getAttribute("x")))
		self.assertEquals(48,float(r.getAttribute("y")))
		self.assertEquals(24,float(r.getAttribute("width")))
		self.assertEquals(72,float(r.getAttribute("height")))
	
	def test_rect_stroke_colour(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke="red",salpha=1.0,w=1,stype=core.STROKE_SOLID,fill="blue",falpha=1.0)]).documentElement)[0]
		self.assertEquals("red", r.getAttribute("stroke"))
	
	def test_rect_special_stroke_colour(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke=core.C_FOREGROUND,salpha=1.0,w=1,stype=core.STROKE_SOLID,fill="blue",falpha=1.0)],
			main.OutputPrefs("yellow","indigo")).documentElement)[0]
		self.assertEquals("yellow", r.getAttribute("stroke"))
	
	def test_rect_no_stroke(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke=None,salpha=1.0,w=1,stype=core.STROKE_SOLID,fill="blue",falpha=1.0)]).documentElement)[0]
		self.assertEquals("none", r.getAttribute("stroke"))
		
	def test_rect_stroke_alpha(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke="red",salpha=0.75,w=1,stype=core.STROKE_SOLID,fill="blue",falpha=1.0)]).documentElement)[0]
		self.assertEquals(0.75,float(r.getAttribute("stroke-opacity")))
		
	def test_rect_stroke_width(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke="red",salpha=1.0,w=3,stype=core.STROKE_SOLID,fill="blue",falpha=1.0)]).documentElement)[0]
		self.assertEquals(7.5, float(r.getAttribute("stroke-width")))
		
	def test_rect_stroke_solid(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke="red",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill="blue",falpha=1.0)]).documentElement)[0]
		self.assertEquals("", r.getAttribute("stroke-dasharray"))
		
	def test_rect_stroke_dashed(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke="red",salpha=1.0,w=2,stype=core.STROKE_DASHED,fill="blue",falpha=1.0)]).documentElement)[0]
		self.assertEquals("8,8", r.getAttribute("stroke-dasharray"))
		
	def test_rect_fill_colour(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke="red",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill="blue",falpha=1.0)]).documentElement)[0]
		self.assertEquals("blue",r.getAttribute("fill"))
		
	def test_rect_special_fill_colour(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
				stroke="red",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=core.C_BACKGROUND,falpha=1.0)],
			main.OutputPrefs("brown","gray")).documentElement)[0]
		self.assertEquals("gray",r.getAttribute("fill"))
		
	def test_rect_no_fill(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke="red",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=None,falpha=1.0)]).documentElement)[0]
		self.assertEquals("none",r.getAttribute("fill"))
		
	def test_rect_fill_alpha(self):
		r = self.child_elements(self.do_output([core.Rectangle(a=(1,2),b=(3,5),z=1,
			stroke="red",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill="blue",falpha=0.75)]).documentElement)[0]
		self.assertEquals(0.75,float(r.getAttribute("fill-opacity")))
		
	def test_rect_z(self):
		rs = self.child_elements(self.do_output([
			core.Rectangle(a=(1,2),b=(3,4),z=5,stroke="red",salpha=1.0,w=2,
				stype=core.STROKE_SOLID,fill="blue",falpha=1.0),
			core.Rectangle(a=(9,9),b=(8,8),z=1,stroke="green",salpha=1.0,w=2,
				stype=core.STROKE_SOLID,fill="red",falpha=1.0),
			core.Rectangle(a=(3,4),b=(5,6),z=3,stroke="blue",salpha=1.0,w=2,
				stype=core.STROKE_SOLID,fill="green",falpha=1.0), 
		]).documentElement)
		self.assertEquals("green", rs[0].getAttribute("stroke"))
		self.assertEquals("blue", rs[1].getAttribute("stroke"))
		self.assertEquals("red", rs[2].getAttribute("stroke"))
		
	def test_handles_ellipse(self):
		ch = self.child_elements(self.do_output([ core.Ellipse(a=(2,3),b=(5,1),z=1,
			stroke="red",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill="blue",falpha=1.0) ]).documentElement)
		self.assertEquals(1, len(ch))
		self.assertEquals("ellipse", ch[0].tagName)
		
	def test_ellipse_coordinates(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke="red",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill="blue",falpha=1.0) ]).documentElement)[0]
		self.assertEquals(42, float(e.getAttribute("cx")))
		self.assertEquals(48, float(e.getAttribute("cy")))
		self.assertEquals(18, float(e.getAttribute("rx")))
		self.assertEquals(24, float(e.getAttribute("ry")))
		
	def test_ellipse_stroke_colour(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke="red",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill="blue",falpha=1.0) ]).documentElement)[0]
		self.assertEquals("red",e.getAttribute("stroke"))
		
	def test_ellipse_special_stroke_colour(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke=core.C_BACKGROUND,salpha=1.0,w=2,stype=core.STROKE_SOLID,fill="blue",falpha=1.0) ],
			main.OutputPrefs("green","orange")).documentElement)[0]
		self.assertEquals("orange",e.getAttribute("stroke"))
		
	def test_ellipse_no_stroke(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke=None,salpha=1.0,w=2,stype=core.STROKE_SOLID,fill="blue",falpha=1.0) ]).documentElement)[0]
		self.assertEquals("none",e.getAttribute("stroke"))
		
	def test_ellipse_stroke_alpha(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke="red",salpha=0.75,w=2,stype=core.STROKE_SOLID,fill="blue",falpha=1.0) ]).documentElement)[0]
		self.assertEquals(0.75,float(e.getAttribute("stroke-opacity")))
		
	def test_ellipse_stroke_width(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke="red",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill="blue",falpha=1.0) ]).documentElement)[0]
		self.assertEquals(5, float(e.getAttribute("stroke-width")))
		
	def test_ellipse_stroke_solid(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke="red",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill="blue",falpha=1.0) ]).documentElement)[0]
		self.assertEquals("", e.getAttribute("stroke-dasharray"))
		
	def test_ellipse_stroke_dashed(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke="red",salpha=1.0,w=2,stype=core.STROKE_DASHED,fill="blue",falpha=1.0) ]).documentElement)[0]
		self.assertEquals("8,8", e.getAttribute("stroke-dasharray"))
		
	def test_ellipse_fill_colour(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke="red",salpha=10,w=2,stype=core.STROKE_SOLID,fill="blue",falpha=1.0) ]).documentElement)[0]
		self.assertEquals("blue", e.getAttribute("fill"))
		
	def test_ellipse_special_fill_colour(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
				stroke="red",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=core.C_FOREGROUND,falpha=1.0) ],
			main.OutputPrefs("pink","black")).documentElement)[0]
		self.assertEquals("pink",e.getAttribute("fill"))
		
	def test_ellipse_no_fill(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke="red",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=None,falpha=1.0) ]).documentElement)[0]
		self.assertEquals("none", e.getAttribute("fill"))
		
	def test_ellipse_fill_alpha(self):
		e = self.child_elements(self.do_output([ core.Ellipse(a=(2,1),b=(5,3),z=1,
			stroke="red",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill="blue",falpha=0.75) ]).documentElement)[0]
		self.assertEquals(0.75, float(e.getAttribute("fill-opacity")))
		
	def test_ellipse_z(self):
		ch = self.child_elements(self.do_output([ 
			core.Ellipse(a=(2,1),b=(5,3),z=3,stroke="red",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill="blue",falpha=1.0),
			core.Ellipse(a=(2,2),b=(1,1),z=10,stroke="blue",salpha=1.0,w=3,stype=core.STROKE_SOLID,fill="green",falpha=1.0),
			core.Ellipse(a=(3,3),b=(4,5),z=1,stroke="green",salpha=1.0,w=1,stype=core.STROKE_SOLID,fill="red",falpha=1.0) ]).documentElement)
		self.assertEquals(3, len(ch))
		self.assertEquals("green", ch[0].getAttribute("stroke"))
		self.assertEquals("red", ch[1].getAttribute("stroke"))
		self.assertEquals("blue", ch[2].getAttribute("stroke"))
		
	def test_handles_arc(self):
		ch = self.child_elements(self.do_output([ core.Arc(a=(2,5),b=(3,4),z=1,
			start=-math.pi/2,end=math.pi/4,stroke="red",salpha=1.0,w=1,stype=core.STROKE_SOLID,
			fill="blue",falpha=1.0) ]).documentElement)
		self.assertEquals(1, len(ch))
		self.assertEquals("path", ch[0].tagName)
		
	def test_arc_coordinates(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
			start=-math.pi,end=math.pi/2,stroke="red",salpha=1.0,w=1,
			stype=core.STROKE_SOLID,fill="blue",falpha=1.0) ]).documentElement)[0]
		self.assertEquals("M 24,120 A 6,24 0 1 1 30,144", a.getAttribute("d"))
		
	def test_arc_stroke_colour(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
			start=-math.pi,end=math.pi/2,stroke="red",salpha=1.0,w=1,
			stype=core.STROKE_SOLID,fill="blue",falpha=1.0) ]).documentElement)[0]
		self.assertEquals("red", a.getAttribute("stroke"))
		
	def test_arc_special_stroke_colour(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
				start=-math.pi,end=math.pi/2,stroke=core.C_FOREGROUND,salpha=1.0,
				w=1,stype=core.STROKE_SOLID,fill="blue",falpha=1.0) ],
			main.OutputPrefs("silver","gold")).documentElement)[0]
		self.assertEquals("silver",a.getAttribute("stroke"))
		
	def test_arc_no_stroke(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
			start=-math.pi,end=math.pi/2,stroke=None,salpha=1.0,w=1,
			stype=core.STROKE_SOLID,fill="blue",falpha=1.0) ]).documentElement)[0]
		self.assertEquals("none", a.getAttribute("stroke"))
		
	def test_arc_stroke_alpha(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
			start=-math.pi,end=math.pi/2,stroke="red",salpha=0.75,w=1,
			stype=core.STROKE_SOLID,fill="blue",falpha=1.0) ]).documentElement)[0]
		self.assertEquals(0.75, float(a.getAttribute("stroke-opacity")))
		
	def test_arc_stroke_width(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
			start=-math.pi,end=math.pi/2,stroke="red",salpha=1.0,w=1,
			stype=core.STROKE_SOLID,fill="blue",falpha=1.0) ]).documentElement)[0]
		self.assertEquals(2.5, float(a.getAttribute("stroke-width")))
		
	def test_arc_stroke_solid(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
			start=-math.pi,end=math.pi/2,stroke="red",salpha=1.0,w=1,
			stype=core.STROKE_SOLID,fill="blue",falpha=1.0) ]).documentElement)[0]
		self.assertEquals("", a.getAttribute("stroke-dasharray"))
		
	def test_arc_stroke_dashed(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
			start=-math.pi,end=math.pi/2,stroke="red",salpha=1.0,w=1,
			stype=core.STROKE_DASHED,fill="blue",falpha=1.0) ]).documentElement)[0]
		self.assertEquals("8,8", a.getAttribute("stroke-dasharray"))
	
	def test_arc_fill_colour(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
			start=-math.pi,end=math.pi/2,stroke="red",salpha=1.0,w=1,
			stype=core.STROKE_SOLID,fill="blue",falpha=1.0) ]).documentElement)[0]
		self.assertEquals("blue", a.getAttribute("fill"))
		
	def test_arc_special_fill_colour(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
				start=-math.pi,end=math.pi/2,stroke="red",salpha=1.0,w=1,
				stype=core.STROKE_SOLID,fill=core.C_FOREGROUND,falpha=1.0) ],
			main.OutputPrefs("lime","magenta")).documentElement)[0]
		self.assertEquals("lime", a.getAttribute("fill"))
		
	def test_arc_no_fill(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
			start=-math.pi,end=math.pi/2,stroke="red",salpha=1.0,w=1,
			stype=core.STROKE_SOLID,fill=None,falpha=1.0) ]).documentElement)[0]
		self.assertEquals("none", a.getAttribute("fill"))
		
	def test_arc_fill_alpha(self):
		a = self.child_elements(self.do_output([ core.Arc(a=(2,4),b=(3,6),z=1,
			start=-math.pi,end=math.pi/2,stroke="red",salpha=1.0,w=1,
			stype=core.STROKE_SOLID,fill="blue",falpha=0.75) ]).documentElement)[0]
		self.assertEquals(0.75, float(a.getAttribute("fill-opacity")))
		
	def test_arc_z(self):
		ch = self.child_elements(self.do_output([ 
				core.Arc(a=(2,4),b=(3,6),z=5,start=-math.pi,end=math.pi/2,
					stroke="red",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill="blue",falpha=1.0),
				core.Arc(a=(1,2),b=(4,5),z=20,start=-math.pi/2,end=math.pi,
					stroke="blue",salpha=1.0,w=2,stype=core.STROKE_DASHED,fill="red",falpha=1.0),
				core.Arc(a=(3,4),b=(7,1),z=1,start=math.pi,end=math.pi*2,stroke="green",
					salpha=1.0,w=1,stype=core.STROKE_SOLID,fill="orange",falpha=1.0), 
		]).documentElement)
		self.assertEquals(3, len(ch))
		self.assertEquals("green", ch[0].getAttribute("stroke"))
		self.assertEquals("red", ch[1].getAttribute("stroke"))
		self.assertEquals("blue", ch[2].getAttribute("stroke"))

	def test_handles_polygon(self):
		ch = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
			z=1,stroke="orange",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill="red",
			falpha=1.0) ]).documentElement)
		self.assertEquals(1, len(ch))
		self.assertEquals("polygon", ch[0].tagName)
		
	def test_polygon_coordinates(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
			z=1,stroke="orange",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill="red",
			falpha=1.0) ]).documentElement)[0]
		self.assertEquals("12,48 12,72 24,48", p.getAttribute("points"))
		
	def test_polygon_stroke_colour(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
			z=1,stroke="orange",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill="red",
			falpha=1.0) ]).documentElement)[0]
		self.assertEquals("orange", p.getAttribute("stroke"))
		
	def test_polygon_special_stroke_colour(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
				z=1,stroke=core.C_FOREGROUND,salpha=1.0,w=2,stype=core.STROKE_SOLID,fill="red",
				falpha=1.0) ],
			main.OutputPrefs("darkblue","purple")).documentElement)[0]
		self.assertEquals("darkblue", p.getAttribute("stroke"))
		
	def test_polygon_no_stroke(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
			z=1,stroke=None,salpha=1.0,w=2,stype=core.STROKE_SOLID,fill="red",
			falpha=1.0) ]).documentElement)[0]
		self.assertEquals("none", p.getAttribute("stroke"))
		
	def test_polygon_stroke_alpha(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
			z=1,stroke="orange",salpha=0.75,w=2,stype=core.STROKE_SOLID,fill="red",
			falpha=1.0) ]).documentElement)[0]
		self.assertEquals(0.75, float(p.getAttribute("stroke-opacity")))
	
	def test_polygon_stroke_width(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
			z=1,stroke="purple",salpha=1.0,w=2,stype=core.STROKE_SOLID, fill="red",
			falpha=1.0) ]).documentElement)[0]
		self.assertEquals(5, float(p.getAttribute("stroke-width")))
		
	def test_polygon_stroke_solid(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
			z=1,stroke="purple",salpha=1.0,w=2,stype=core.STROKE_SOLID, fill="red",
			falpha=1.0) ]).documentElement)[0]
		self.assertEquals("", p.getAttribute("stroke-dasharray"))
		
	def test_polygon_stroke_dashed(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
			z=1,stroke="purple",salpha=1.0,w=2,stype=core.STROKE_DASHED,fill="red",
			falpha=1.0) ]).documentElement)[0]
		self.assertEquals("8,8", p.getAttribute("stroke-dasharray"))
		
	def test_polygon_fill_colour(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
			z=1,stroke="purple",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill="yellow",
			falpha=1.0) ]).documentElement)[0]
		self.assertEquals("yellow", p.getAttribute("fill"))
		
	def test_polygon_special_fill_colour(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
				z=1,stroke="purple",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=core.C_FOREGROUND,
				falpha=1.0) ],
			main.OutputPrefs("lime","magenta") ).documentElement)[0]
		self.assertEquals("lime", p.getAttribute("fill"))
		
	def test_polygon_no_fill(self):
		p = self.child_elements(self.do_output([ core.Polygon(points=((1,2),(1,3),(2,2)),
			z=1,stroke="purple",salpha=1.0,w=2,stype=core.STROKE_SOLID,fill=None,
			falpha=1.0) ]).documentElement)[0]
		self.assertEquals("none", p.getAttribute("fill"))
		
	def test_polygon_z(self):
		ch = self.child_elements(self.do_output([ 
			core.Polygon(points=((1,2),(1,3),(2,2)),z=1,stroke="purple",salpha=1.0,
				w=2,stype=core.STROKE_SOLID,fill="red",falpha=1.0),
			core.Polygon(points=((1,2),(1,3),(2,2)),z=3,stroke="green",salpha=1.0,
				w=3,stype=core.STROKE_DASHED,fill="red",falpha=1.0),
			core.Polygon(points=((1,2),(1,3),(2,2)),z=2,stroke="wheat",salpha=1.0,
				w=1,stype=core.STROKE_SOLID,fill="red",falpha=1.0), 
		]).documentElement)
		self.assertEquals(3, len(ch))
		self.assertEquals("purple", ch[0].getAttribute("stroke"))
		self.assertEquals("wheat", ch[1].getAttribute("stroke"))
		self.assertEquals("green", ch[2].getAttribute("stroke"))
	
	def test_handles_quadcurve(self):
		ch = self.child_elements(self.do_output([ core.QuadCurve(a=(1,2),b=(3,5),
			c=(4,3),z=1,stroke="purple",salpha=1.0,w=2,stype=core.STROKE_SOLID) ]).documentElement)
		self.assertEquals(1, len(ch))
		self.assertEquals("path", ch[0].tagName)
		
	def test_quadcurve_coordinates(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(a=(1,2),b=(3,5),c=(4,3),
			z=1,stroke="purple",salpha=1.0,w=2,stype=core.STROKE_SOLID) ]).documentElement)[0]
		self.assertEquals("M 12,48 Q 48,72 36,120",q.getAttribute("d"))
		
	def test_quadcurve_stroke_colour(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(a=(1,2),b=(3,5),c=(4,3),
			z=1,stroke="purple",salpha=1.0,w=2,stype=core.STROKE_SOLID) ]).documentElement)[0]
		self.assertEquals("purple", q.getAttribute("stroke"))
		
	def test_quadcurve_special_stroke_colour(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(a=(1,2),b=(3,5),c=(4,3),
				z=1,stroke=core.C_FOREGROUND,salpha=1.0,w=2,stype=core.STROKE_SOLID) ],
			main.OutputPrefs("darkred","green")).documentElement)[0]
		self.assertEquals("darkred",q.getAttribute("stroke"))
		
	def test_quadcurve_no_stroke(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(a=(1,2),b=(3,5),c=(4,3),
			z=1,stroke=None,salpha=1.0,w=2,stype=core.STROKE_SOLID) ]).documentElement)[0]
		self.assertEquals("none", q.getAttribute("stroke"))
		
	def test_quadcurve_stroke_alpha(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(a=(1,2),b=(3,5),c=(4,3),
			z=1,stroke="purple",salpha=0.75,w=2,stype=core.STROKE_SOLID) ]).documentElement)[0]
		self.assertEquals(0.75, float(q.getAttribute("stroke-opacity")))
		
	def test_quadcurve_stroke_width(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(a=(1,2),b=(3,5),c=(4,3),
			z=1,stroke="purple",salpha=1.0,w=2,stype=core.STROKE_SOLID) ]).documentElement)[0]
		self.assertEquals(5, float(q.getAttribute("stroke-width")))
		
	def test_quadcurve_stroke_solid(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(a=(1,2),b=(3,5),c=(4,3),
			z=1,stroke="purple",salpha=1.0,w=2,stype=core.STROKE_SOLID) ]).documentElement)[0]
		self.assertEquals("", q.getAttribute("stroke-dasharray"))
		
	def test_quadcurve_stroke_dashed(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(a=(1,2),b=(3,5),c=(4,3),
			z=1,stroke="purple",salpha=1.0,w=2,stype=core.STROKE_DASHED) ]).documentElement)[0]
		self.assertEquals("8,8", q.getAttribute("stroke-dasharray"))
		
	def test_quadcurve_z(self):
		ch = self.child_elements(self.do_output([ 
			core.QuadCurve(a=(1,2),b=(3,5),c=(4,3),z=1,stroke="purple",salpha=1.0,
				w=2,stype=core.STROKE_SOLID),
			core.QuadCurve(a=(0,1),b=(2,4),c=(3,4),z=3,stroke="green",salpha=1.0,
				w=3,stype=core.STROKE_DASHED),
			core.QuadCurve(a=(2,3),b=(4,0),c=(4,5),z=2,stroke="wheat",salpha=1.0,
				w=1,stype=core.STROKE_SOLID), 
		]).documentElement)
		self.assertEquals(3, len(ch))
		self.assertEquals("purple", ch[0].getAttribute("stroke"))
		self.assertEquals("wheat", ch[1].getAttribute("stroke"))
		self.assertEquals("green", ch[2].getAttribute("stroke"))
		
	def test_handles_text(self):
		ch = self.child_elements(self.do_output([ core.Text(pos=(3,4),z=1,text="!",
			colour="red",alpha=1.0,size=1) ]).documentElement)
		self.assertEquals(1, len(ch))
		self.assertEquals("text", ch[0].tagName)
		self.assertEquals("monospace", ch[0].getAttribute("font-family"))
		
	def test_text_coordinates(self):
		t = self.child_elements(self.do_output([ core.Text(pos=(3,4),z=1,text="!",
			colour="red",alpha=1.0,size=1) ]).documentElement)[0]
		self.assertEquals(36, float(t.getAttribute("x")))
		self.assertEquals(114,float(t.getAttribute("y")))
		
	def test_text_content(self):
		t = self.child_elements(self.do_output([ core.Text(pos=(3,4),z=1,text="!",
			colour="red",alpha=1.0,size=1) ]).documentElement)[0]
		self.assertEquals(1, len(t.childNodes))
		self.assertEquals("!", t.childNodes[0].nodeValue)
		
	def test_text_colour(self):
		t = self.child_elements(self.do_output([ core.Text(pos=(3,4),z=1,text="!",
			colour="red",alpha=1.0,size=1) ]).documentElement)[0]
		self.assertEquals("red", t.getAttribute("fill"))
		
	def test_text_special_colour(self):
		t = self.child_elements(self.do_output([ core.Text(pos=(3,4),z=1,text="!",
				colour=core.C_BACKGROUND,alpha=1.0,size=1) ],
			main.OutputPrefs("orange","yellow")).documentElement)[0]
		self.assertEquals("yellow", t.getAttribute("fill"))
		
	def test_text_alpha(self):
		t = self.child_elements(self.do_output([ core.Text(pos=(3,4),z=1,text="!",
			colour="red", alpha=0.75, size=1) ]).documentElement)[0]
		self.assertEquals(0.75, float(t.getAttribute("fill-opacity")))
		
	def test_text_size(self):
		t = self.child_elements(self.do_output([ core.Text(pos=(3,4),z=1,text="!",
			colour="red",alpha=1.0, size=1.25) ]).documentElement)[0]
		self.assertEquals(20, float(t.getAttribute("font-size")))
		
	def test_text_z(self):
		ch = self.child_elements(self.do_output([ 
			core.Text(pos=(3,4),z=4,text="!",colour="red",alpha=1.0,size=1),
			core.Text(pos=(2,2),z=12,text="?",colour="blue",alpha=1.0,size=1),
			core.Text(pos=(4,5),z=1,text="&",colour="green",alpha=1.0,size=1), 
		]).documentElement)
		self.assertEquals(3, len(ch))
		self.assertEquals("green",ch[0].getAttribute("fill"))
		self.assertEquals("red",ch[1].getAttribute("fill"))
		self.assertEquals("blue",ch[2].getAttribute("fill"))


class TestProcessDiagram(unittest.TestCase):

	def test_returns_background_rect(self):
		result = main.process_diagram("",[])
		self.assertEquals(1, len(result))
		self.assertTrue( isinstance(result[0],core.Rectangle) )
	
	def test_background_rect_size(self):
		r = main.process_diagram(
			"012345\n"+
			"012345\n"+
			"012345", [])[0]
		self.assertEquals((0,0),r.a)
		self.assertEquals((6,3),r.b)
		
	def test_background_rect_size_jagged(self):
		r = main.process_diagram(
			"0123\n"+
			"012345\n"+
			"01234", [])[0]
		self.assertEquals((0,0),r.a)
		self.assertEquals((6,3),r.b)
	
	def test_background_rect_colours(self):
		r = main.process_diagram("",[])[0]
		self.assertEquals(core.C_BACKGROUND,r.fill)
		self.assertEquals(None,r.stroke)
		
	def test_background_z(self):
		r = main.process_diagram("",[])[0]
		self.assertEquals(-1, r.z)
	
	def remove_background(self,result):
		return filter(lambda x: not isinstance(x,core.Rectangle),result)
	
	def test_single_character_pattern_match(self):
		r = object()
		class SingleCharPattern(object):
			def test(self,curr):
				raise StopIteration()
			def render(self):
				return [ r ]
		result = self.remove_background(main.process_diagram("a",[SingleCharPattern]))
		self.assertEquals(4,len(result))
		self.assertEquals(r,result[0])
	
	def test_doesnt_output_rejected_pattern(self):
		class RejectingPattern(object):
			def test(self,curr):
				raise core.PatternRejected()
			def render(self):
				return [ object() ]
		result = self.remove_background(main.process_diagram("a",[RejectingPattern]))
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
		result = self.remove_background(main.process_diagram("a",[MultiCharPattern]))
		self.assertEquals(3, len(result))
		self.assertEquals(r,result[0])
		self.assertEquals(r,result[1])
		
	def test_doesnt_output_unfinished_pattern(self):
		class NeverendingPattern(object):
			def test(self,curr):
				return core.M_NONE
			def render(self):
				return [ object() ]
		result = self.remove_background(main.process_diagram("a",[NeverendingPattern]))
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
		result = self.remove_background(main.process_diagram("a",[Pattern1,Pattern2]))
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
		result = self.remove_background(main.process_diagram("abc",[OccupyingPattern]))
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
		result = self.remove_background(main.process_diagram("abc",
				[FailingMetaPattern,MetaMatchingPattern]))
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
		result = self.remove_background(main.process_diagram("a a",[MetaMatchingPattern]))
		self.assertEquals(2, len(result))		


if __name__ == "__main__":
	unittest.main()
