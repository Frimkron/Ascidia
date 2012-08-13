import unittest
import core
import patterns
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
	
	def do_output(self,items):
		s = io.BytesIO()
		main.SvgOutput()._output(items,s)
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
		e = self.do_output([core.Line((0,0),(1,1),1,"red",1,core.STROKE_SOLID)]).documentElement
		ch = self.child_elements(e)
		self.assertEquals(1, len(ch))
		self.assertEquals("line", ch[0].tagName)
		
	def test_line_coordinates(self):
		l = self.child_elements(self.do_output([core.Line(
				(1,2),(3,4),1,"red",1,core.STROKE_SOLID)]).documentElement)[0]
		self.assertEquals(12, float(l.getAttribute("x1")))
		self.assertEquals(48, float(l.getAttribute("y1")))
		self.assertEquals(36, float(l.getAttribute("x2")))
		self.assertEquals(96, float(l.getAttribute("y2")))
		
	def test_line_stroke_colour(self):
		l = self.child_elements(self.do_output([core.Line(
				(1,2),(3,4),1,"red",1,core.STROKE_SOLID)]).documentElement)[0]
		self.assertEquals("red", l.getAttribute("stroke"))
		
	def test_line_no_stroke(self):
		l = self.child_elements(self.do_output([core.Line(
				(1,2),(3,4),1,None,1,core.STROKE_SOLID)]).documentElement)[0]
		self.assertEquals("none", l.getAttribute("stroke"))
	
	def test_line_stroke_width(self):
		l = self.child_elements(self.do_output([core.Line(
				(1,2),(3,4),1,"red",2,core.STROKE_SOLID)]).documentElement)[0]
		self.assertEquals(5, float(l.getAttribute("stroke-width")))
		
	def test_line_stroke_solid(self):
		l = self.child_elements(self.do_output([core.Line(
				(1,2),(3,4),1,"red",1,core.STROKE_SOLID)]).documentElement)[0]
		self.assertEquals("", l.getAttribute("stroke-dasharray"))	
	
	def test_line_stroke_dashed(self):
		l = self.child_elements(self.do_output([core.Line(
				(1,2),(3,4),1,"red",1,core.STROKE_DASHED)]).documentElement)[0]
		self.assertEquals("8,8", l.getAttribute("stroke-dasharray"))
		
	def test_line_z(self):
		ls = self.child_elements(self.do_output([
				core.Line((1,2),(3,4),5,"green",1,core.STROKE_SOLID),
				core.Line((9,8),(7,6),1,"blue",1,core.STROKE_SOLID),
				core.Line((6,6),(6,5),3,"red",1,core.STROKE_SOLID), ]).documentElement)
		self.assertEquals("blue",ls[0].getAttribute("stroke"))
		self.assertEquals("red",ls[1].getAttribute("stroke"))
		self.assertEquals("green",ls[2].getAttribute("stroke"))
		
	def test_handles_rectangle(self):
		ch = self.child_elements(self.do_output([core.Rectangle(
				(1,2),(3,4),1,"red",1,core.STROKE_SOLID,"blue")]).documentElement)
		self.assertEquals(1, len(ch))
		self.assertEquals("rect", ch[0].tagName)
		
	def test_rect_coordinates(self):
		r = self.child_elements(self.do_output([core.Rectangle(
				(1,2),(3,5),1,"red",1,core.STROKE_SOLID,"blue")]).documentElement)[0]
		self.assertEquals(12,float(r.getAttribute("x")))
		self.assertEquals(48,float(r.getAttribute("y")))
		self.assertEquals(24,float(r.getAttribute("width")))
		self.assertEquals(72,float(r.getAttribute("height")))
	
	def test_rect_stroke_colour(self):
		r = self.child_elements(self.do_output([core.Rectangle(
				(1,2),(3,5),1,"red",1,core.STROKE_SOLID,"blue")]).documentElement)[0]
		self.assertEquals("red", r.getAttribute("stroke"))
	
	def test_rect_no_stroke(self):
		r = self.child_elements(self.do_output([core.Rectangle(
				(1,2),(3,5),1,None,1,core.STROKE_SOLID,"blue")]).documentElement)[0]
		self.assertEquals("none", r.getAttribute("stroke"))
		
	def test_rect_stroke_width(self):
		r = self.child_elements(self.do_output([core.Rectangle(
				(1,2),(3,5),1,"red",3,core.STROKE_SOLID,"blue")]).documentElement)[0]
		self.assertEquals(7.5, float(r.getAttribute("stroke-width")))
		
	def test_rect_stroke_solid(self):
		r = self.child_elements(self.do_output([core.Rectangle(
				(1,2),(3,5),1,"red",2,core.STROKE_SOLID,"blue")]).documentElement)[0]
		self.assertEquals("", r.getAttribute("stroke-dasharray"))
		
	def test_rect_stroke_dashed(self):
		r = self.child_elements(self.do_output([core.Rectangle(
				(1,2),(3,5),1,"red",2,core.STROKE_DASHED,"blue")]).documentElement)[0]
		self.assertEquals("8,8", r.getAttribute("stroke-dasharray"))
		
	def test_rect_fill_colour(self):
		r = self.child_elements(self.do_output([core.Rectangle(
				(1,2),(3,5),1,"red",2,core.STROKE_SOLID,"blue")]).documentElement)[0]
		self.assertEquals("blue",r.getAttribute("fill"))
		
	def test_rect_no_fill(self):
		r = self.child_elements(self.do_output([core.Rectangle(
				(1,2),(3,5),1,"red",2,core.STROKE_SOLID,None)]).documentElement)[0]
		self.assertEquals("none",r.getAttribute("fill"))
		
	def test_rect_z(self):
		rs = self.child_elements(self.do_output([
			core.Rectangle((1,2),(3,4),5,"red",2,core.STROKE_SOLID,"blue"),
			core.Rectangle((9,9),(8,8),1,"green",2,core.STROKE_SOLID,"red"),
			core.Rectangle((3,4),(5,6),3,"blue",2,core.STROKE_SOLID,"green"), ]).documentElement)
		self.assertEquals("green", rs[0].getAttribute("stroke"))
		self.assertEquals("blue", rs[1].getAttribute("stroke"))
		self.assertEquals("red", rs[2].getAttribute("stroke"))
		
	def test_handles_ellipse(self):
		ch = self.child_elements(self.do_output([ core.Ellipse(
				(2,3),(5,1),1,"red",2,core.STROKE_SOLID,"blue") ]).documentElement)
		self.assertEquals(1, len(ch))
		self.assertEquals("ellipse", ch[0].tagName)
		
	def test_ellipse_coordinates(self):
		e = self.child_elements(self.do_output([ core.Ellipse(
				(2,1),(5,3),1,"red",2,core.STROKE_SOLID,"blue") ]).documentElement)[0]
		self.assertEquals(42, float(e.getAttribute("cx")))
		self.assertEquals(48, float(e.getAttribute("cy")))
		self.assertEquals(18, float(e.getAttribute("rx")))
		self.assertEquals(24, float(e.getAttribute("ry")))
		
	def test_ellipse_stroke_colour(self):
		e = self.child_elements(self.do_output([ core.Ellipse(
				(2,1),(5,3),1,"red",2,core.STROKE_SOLID,"blue") ]).documentElement)[0]
		self.assertEquals("red",e.getAttribute("stroke"))
		
	def test_ellipse_no_stroke(self):
		e = self.child_elements(self.do_output([ core.Ellipse(
				(2,1),(5,3),1,None,2,core.STROKE_SOLID,"blue") ]).documentElement)[0]
		self.assertEquals("none",e.getAttribute("stroke"))
		
	def test_ellipse_stroke_width(self):
		e = self.child_elements(self.do_output([ core.Ellipse(
				(2,1),(5,3),1,"red",2,core.STROKE_SOLID,"blue") ]).documentElement)[0]
		self.assertEquals(5, float(e.getAttribute("stroke-width")))
		
	def test_ellipse_stroke_solid(self):
		e = self.child_elements(self.do_output([ core.Ellipse(
				(2,1),(5,3),1,"red",2,core.STROKE_SOLID,"blue") ]).documentElement)[0]
		self.assertEquals("", e.getAttribute("stroke-dasharray"))
		
	def test_ellipse_stroke_dashed(self):
		e = self.child_elements(self.do_output([ core.Ellipse(
				(2,1),(5,3),1,"red",2,core.STROKE_DASHED,"blue") ]).documentElement)[0]
		self.assertEquals("8,8", e.getAttribute("stroke-dasharray"))
		
	def test_ellipse_fill_colour(self):
		e = self.child_elements(self.do_output([ core.Ellipse(
				(2,1),(5,3),1,"red",2,core.STROKE_SOLID,"blue") ]).documentElement)[0]
		self.assertEquals("blue", e.getAttribute("fill"))
		
	def test_ellipse_no_fill(self):
		e = self.child_elements(self.do_output([ core.Ellipse(
				(2,1),(5,3),1,"red",2,core.STROKE_SOLID,None) ]).documentElement)[0]
		self.assertEquals("none", e.getAttribute("fill"))
		
	def test_ellipse_z(self):
		ch = self.child_elements(self.do_output([ 
			core.Ellipse((2,1),(5,3),3,"red",2,core.STROKE_SOLID,"blue"),
			core.Ellipse((2,2),(1,1),10,"blue",3,core.STROKE_SOLID,"green"),
			core.Ellipse((3,3),(4,5),1,"green",1,core.STROKE_SOLID,"red") ]).documentElement)
		self.assertEquals(3, len(ch))
		self.assertEquals("green", ch[0].getAttribute("stroke"))
		self.assertEquals("red", ch[1].getAttribute("stroke"))
		self.assertEquals("blue", ch[2].getAttribute("stroke"))
		
	def test_handles_arc(self):
		ch = self.child_elements(self.do_output([ core.Arc(
				(2,5),(3,4),1,-math.pi/2,math.pi/4,"red",1,core.STROKE_SOLID,"blue") ]).documentElement)
		self.assertEquals(1, len(ch))
		self.assertEquals("path", ch[0].tagName)
		
	def test_arc_coordinates(self):
		a = self.child_elements(self.do_output([ core.Arc(
				(2,4),(3,6),1,-math.pi,math.pi/2,"red",1,core.STROKE_SOLID,"blue") ]).documentElement)[0]
		self.assertEquals("M 24,120 A 6,24 0 1 1 30,144", a.getAttribute("d"))
		
	def test_arc_stroke_colour(self):
		a = self.child_elements(self.do_output([ core.Arc(
				(2,4),(3,6),1,-math.pi,math.pi/2,"red",1,core.STROKE_SOLID,"blue") ]).documentElement)[0]
		self.assertEquals("red", a.getAttribute("stroke"))
		
	def test_arc_no_stroke(self):
		a = self.child_elements(self.do_output([ core.Arc(
				(2,4),(3,6),1,-math.pi,math.pi/2,None,1,core.STROKE_SOLID,"blue") ]).documentElement)[0]
		self.assertEquals("none", a.getAttribute("stroke"))
		
	def test_arc_stroke_width(self):
		a = self.child_elements(self.do_output([ core.Arc(
				(2,4),(3,6),1,-math.pi,math.pi/2,"red",1,core.STROKE_SOLID,"blue") ]).documentElement)[0]
		self.assertEquals(2.5, float(a.getAttribute("stroke-width")))
		
	def test_arc_stroke_solid(self):
		a = self.child_elements(self.do_output([ core.Arc(
				(2,4),(3,6),1,-math.pi,math.pi/2,"red",1,core.STROKE_SOLID,"blue") ]).documentElement)[0]
		self.assertEquals("", a.getAttribute("stroke-dasharray"))
		
	def test_arc_stroke_dashed(self):
		a = self.child_elements(self.do_output([ core.Arc(
				(2,4),(3,6),1,-math.pi,math.pi/2,"red",1,core.STROKE_DASHED,"blue") ]).documentElement)[0]
		self.assertEquals("8,8", a.getAttribute("stroke-dasharray"))
	
	def test_arc_fill_colour(self):
		a = self.child_elements(self.do_output([ core.Arc(
				(2,4),(3,6),1,-math.pi,math.pi/2,"red",1,core.STROKE_SOLID,"blue") ]).documentElement)[0]
		self.assertEquals("blue", a.getAttribute("fill"))
		
	def test_arc_no_fill(self):
		a = self.child_elements(self.do_output([ core.Arc(
				(2,4),(3,6),1,-math.pi,math.pi/2,"red",1,core.STROKE_SOLID,None) ]).documentElement)[0]
		self.assertEquals("none", a.getAttribute("fill"))
		
	def test_arc_z(self):
		ch = self.child_elements(self.do_output([ 
				core.Arc((2,4),(3,6),5,-math.pi,math.pi/2,"red",2,core.STROKE_SOLID,"blue"),
				core.Arc((1,2),(4,5),20,-math.pi/2,math.pi,"blue",2,core.STROKE_DASHED,"red"),
				core.Arc((3,4),(7,1),1,math.pi,math.pi*2,"green",1,core.STROKE_SOLID,"orange"), ]).documentElement)
		self.assertEquals(3, len(ch))
		self.assertEquals("green", ch[0].getAttribute("stroke"))
		self.assertEquals("red", ch[1].getAttribute("stroke"))
		self.assertEquals("blue", ch[2].getAttribute("stroke"))
		
	def test_handles_quadcurve(self):
		ch = self.child_elements(self.do_output([ core.QuadCurve(
				(1,2),(3,5),(4,3),1,"purple",2,core.STROKE_SOLID) ]).documentElement)
		self.assertEquals(1, len(ch))
		self.assertEquals("path", ch[0].tagName)
		
	def test_quadcurve_coordinates(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(
				(1,2),(3,5),(4,3),1,"purple",2,core.STROKE_SOLID) ]).documentElement)[0]
		self.assertEquals("M 12,48 Q 48,72 36,120",q.getAttribute("d"))
		
	def test_quadcurve_stroke_colour(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(
				(1,2),(3,5),(4,3),1,"purple",2,core.STROKE_SOLID) ]).documentElement)[0]
		self.assertEquals("purple", q.getAttribute("stroke"))
		
	def test_quadcurve_no_stroke(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(
				(1,2),(3,5),(4,3),1,None,2,core.STROKE_SOLID) ]).documentElement)[0]
		self.assertEquals("none", q.getAttribute("stroke"))
		
	def test_quadcurve_stroke_width(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(
				(1,2),(3,5),(4,3),1,"purple",2,core.STROKE_SOLID) ]).documentElement)[0]
		self.assertEquals(5, float(q.getAttribute("stroke-width")))
		
	def test_quadcurve_stroke_solid(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(
				(1,2),(3,5),(4,3),1,"purple",2,core.STROKE_SOLID) ]).documentElement)[0]
		self.assertEquals("", q.getAttribute("stroke-dasharray"))
		
	def test_quadcurve_stroke_dashed(self):
		q = self.child_elements(self.do_output([ core.QuadCurve(
				(1,2),(3,5),(4,3),1,"purple",2,core.STROKE_DASHED) ]).documentElement)[0]
		self.assertEquals("8,8", q.getAttribute("stroke-dasharray"))
		
	def test_quadcurve_z(self):
		ch = self.child_elements(self.do_output([ 
			core.QuadCurve((1,2),(3,5),(4,3),1,"purple",2,core.STROKE_SOLID),
			core.QuadCurve((0,1),(2,4),(3,4),3,"green",3,core.STROKE_DASHED),
			core.QuadCurve((2,3),(4,0),(4,5),2,"wheat",1,core.STROKE_SOLID), ]).documentElement)
		self.assertEquals(3, len(ch))
		self.assertEquals("purple", ch[0].getAttribute("stroke"))
		self.assertEquals("wheat", ch[1].getAttribute("stroke"))
		self.assertEquals("green", ch[2].getAttribute("stroke"))
		
	def test_handles_text(self):
		ch = self.child_elements(self.do_output([ core.Text(
				(3,4),1,"!","red",1) ]).documentElement)
		self.assertEquals(1, len(ch))
		self.assertEquals("text", ch[0].tagName)
		self.assertEquals("monospace", ch[0].getAttribute("font-family"))
		
	def test_text_coordinates(self):
		t = self.child_elements(self.do_output([ core.Text(
				(3,4),1,"!","red",1) ]).documentElement)[0]
		self.assertEquals(36, float(t.getAttribute("x")))
		self.assertEquals(114,float(t.getAttribute("y")))
		
	def test_text_content(self):
		t = self.child_elements(self.do_output([ core.Text(
				(3,4),1,"!","red",1) ]).documentElement)[0]
		self.assertEquals(1, len(t.childNodes))
		self.assertEquals("!", t.childNodes[0].nodeValue)
		
	def test_text_colour(self):
		t = self.child_elements(self.do_output([ core.Text(
				(3,4),1,"!","red",1) ]).documentElement)[0]
		self.assertEquals("red", t.getAttribute("fill"))
		
	def test_text_size(self):
		t = self.child_elements(self.do_output([ core.Text(
				(3,4),1,"!","red",1.25) ]).documentElement)[0]
		self.assertEquals(20, float(t.getAttribute("font-size")))
		
	def test_text_z(self):
		ch = self.child_elements(self.do_output([ 
			core.Text((3,4),4,"!","red",1),
			core.Text((2,2),12,"?","blue",1),
			core.Text((4,5),1,"&","green",1), ]).documentElement)
		self.assertEquals(3, len(ch))
		self.assertEquals("green",ch[0].getAttribute("fill"))
		self.assertEquals("red",ch[1].getAttribute("fill"))
		self.assertEquals("blue",ch[2].getAttribute("fill"))


class TestProcessDiagram(unittest.TestCase):

	def test_returns_empty_list_for_no_matches(self):
		result = main.process_diagram("",[])
		self.assertTrue(isinstance(result,list))
		
	def test_single_character_pattern_match(self):
		r = object()
		class SingleCharPattern(object):
			def test(self,curr):
				raise StopIteration()
			def render(self):
				return [ r ]
		result = main.process_diagram("a",[SingleCharPattern])
		self.assertEquals(3,len(result))
		self.assertEquals(r,result[0])
	
	def test_doesnt_output_rejected_pattern(self):
		class RejectingPattern(object):
			def test(self,curr):
				raise core.PatternRejected()
			def render(self):
				return [ object() ]
		result = main.process_diagram("a",[RejectingPattern])
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
		result = main.process_diagram("a",[MultiCharPattern])
		self.assertEquals(2, len(result))
		self.assertEquals(r,result[0])
		self.assertEquals(r,result[1])
		
	def test_doesnt_output_unfinished_pattern(self):
		class NeverendingPattern(object):
			def test(self,curr):
				return core.M_NONE
			def render(self):
				return [ object() ]
		result = main.process_diagram("a",[NeverendingPattern])
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
		result = main.process_diagram("a",[Pattern1,Pattern2])
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
		self.assertEquals(5,len(PosStoringPattern.insts))
		self.assertEquals([(0,0),(1,0)],PosStoringPattern.insts[0].positions)
		self.assertEquals([(1,0),(0,1)],PosStoringPattern.insts[1].positions)
		self.assertEquals([(0,1),(1,1)],PosStoringPattern.insts[2].positions)
		self.assertEquals([(1,1),(0,2)],PosStoringPattern.insts[3].positions)
		self.assertEquals([(0,2)],PosStoringPattern.insts[4].positions)
		
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
		self.assertEquals(4,len(CharStoringPattern.insts))
		self.assertEquals(["a","b"],CharStoringPattern.insts[0].chars)
		self.assertEquals(["b","\n"],CharStoringPattern.insts[1].chars)
		self.assertEquals(["\n",core.END_OF_INPUT],CharStoringPattern.insts[2].chars)
		self.assertEquals([core.END_OF_INPUT],CharStoringPattern.insts[3].chars)
	
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
		self.assertEquals(4, len(MetaStoringPattern.insts))
		self.assertEquals([core.M_BOX_START_E,core.M_BOX_START_E],MetaStoringPattern.insts[0].metas)
		self.assertEquals([core.M_BOX_START_E,core.M_BOX_START_E],MetaStoringPattern.insts[1].metas)
		self.assertEquals([core.M_BOX_START_E,core.M_NONE],MetaStoringPattern.insts[2].metas)
		self.assertEquals([core.M_NONE],MetaStoringPattern.insts[3].metas)
		
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
		result = main.process_diagram("abc",[OccupyingPattern])
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
				return []
		class MetaMatchingPattern(object):
			def test(self,curr):
				if curr.meta == core.M_BOX_START_E: 
					raise StopIteration()
				else:
					raise core.PatternRejected()
			def render(self):
				return []
		result = main.process_diagram("abc",[FailingMetaPattern,MetaMatchingPattern])
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
		result = main.process_diagram("a a",[MetaMatchingPattern])
		self.assertEquals(2, len(result))		


class PatternTests(object):

	pclass = None

	def test_can_construct(self):
		self.pclass()
		
	def test_raises_error_on_early_render(self):
		p = self.pclass()
		with self.assertRaises(core.PatternStateError):
			p.render()


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
		self.assertEquals("black", text.colour)
		
	def test_render_size(self):
		text = self.do_render(2,1,"a")[0]
		self.assertEquals(1, text.size)

def feed_input(pattern,row,col,characters):
	for char in characters:
		pattern.test(main.CurrentChar(row,col,char,core.M_NONE))
		col += 1

def find_with(test,items,property,value):
	for i in items:
		if getattr(i,property) == value:
			return i
	test.fail("%s not found in '%s' properties %s" % (str(value),property,
		str([getattr(i,property) for i in items])))

def find_type(test,items,type):
	l = filter(lambda x: isinstance(x,type), items)
	if len(l) == 0:
		test.fail("No %ss in %s" % (str(type),str(items)))
	return l


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
		linea = find_with(self,lines,"a",(2.5,3))
		self.assertEquals((2.5,5),linea.b)
		lineb = find_with(self,lines,"a",(6.5,3))
		self.assertEquals((6.5,5),lineb.b)
		
	def test_render_line_coordinates_wider(self):
		lines = filter(lambda x: isinstance(x,core.Line), self.do_render(5,1,5,1))
		linea = find_with(self,lines,"a",(5.5,2))
		self.assertEquals((5.5,4),linea.b)
		lineb = find_with(self,lines,"a",(11.5,2))
		self.assertEquals((11.5,4),lineb.b)
		
	def test_render_line_coordinates_taller(self):
		lines = filter(lambda x: isinstance(x,core.Line), self.do_render(3,2,3,3))
		linea = find_with(self,lines,"a",(3.5,3))
		self.assertEquals((3.5,7), linea.b)
		lineb = find_with(self,lines,"a",(7.5,3))
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
			self.assertEquals("black",r.stroke)
			
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


class TestUpDiagLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.UpDiagLinePattern
		
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
			p.test(main.CurrentChar(0,0," ",core.M_NONE))
			
	def test_expects_start_forwardslash_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,0,"/",core.M_OCCUPIED))
			
	def test_allows_rest_of_start_line(self):
		p = self.pclass()
		feed_input(p,0,0,"/")
		p.test(main.CurrentChar(0,1,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,2,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,3,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,2,"/\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		
	def test_accepts_single_char_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "/\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2," ",core.M_NONE))
	
	def test_accepts_rest_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "/\n")
		feed_input(p,1,0," /")
		p.test(main.CurrentChar(1,2,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,3,"\n",core.M_OCCUPIED))
		
	def test_allows_no_character_at_end_due_to_eoi(self):
		p = self.pclass()
		feed_input(p,0,2,  "/  \n")
		feed_input(p,1,0," / \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,3,   "/  \n")
		feed_input(p,1,0,"  /   \n")
		feed_input(p,2,0,"\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0," ",core.M_NONE))
			
	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "/\n")
		feed_input(p,1,0," ")
		p.test(main.CurrentChar(1,1,"/",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2," ",core.M_NONE))
			
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
	
	def test_render_coordinates_shorter(self):
		l = self.do_render(6,3,1)[0]
		self.assertEquals((7,3),l.a)
		self.assertEquals((6,4),l.b)

	def test_render_z(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals("black",l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.STROKE_SOLID,l.stype)
	
	
class TestDownDiagLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.DownDiagLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,1, "\\   \n")
		feed_input(p,1,0,"  \\  \n")
		feed_input(p,2,0,"   \\ \n")
		feed_input(p,3,0,"     ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,4," ",core.M_NONE))
			
	def test_expects_start_backslash(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,0," ",core.M_NONE))
			
	def test_expects_start_backslash_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,0,"\\",core.M_OCCUPIED))
			
	def test_allows_rest_of_start_line(self):
		p = self.pclass()
		feed_input(p,0,0,"\\")
		p.test(main.CurrentChar(0,1,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,2,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,3,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,1,"\\\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		
	def test_accepts_single_char_line(self):
		p = self.pclass()
		feed_input(p,0,1, "\\\n")
		feed_input(p,1,0,"   ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2," ",core.M_NONE))
	
	def test_accepts_rest_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,1, "\\\n")
		feed_input(p,1,0,"  \\")
		p.test(main.CurrentChar(1,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,4,"\n",core.M_OCCUPIED))
		
	def test_allows_no_character_at_end_due_to_eoi(self):
		p = self.pclass()
		feed_input(p,0,1, "\\  \n")
		feed_input(p,1,0,"  \\ \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,1, "\\  \n")
		feed_input(p,1,0,"  \\ \n")
		feed_input(p,2,0," \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0," ",core.M_NONE))
			
	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,1, "\\ \n")
		feed_input(p,1,0,"  ")
		p.test(main.CurrentChar(1,2,"\\",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_allows_line_to_end_at_right_edge(self):
		p = self.pclass()
		feed_input(p,0,1, "\\  \n")
		feed_input(p,1,0,"  \\ \n")
		feed_input(p,2,0,"   \\\n")
		feed_input(p,3,0,"    \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(4,0," ",core.M_NONE))
			
	def test_allows_line_to_end_at_bottom_right_corner(self):
		p = self.pclass()
		feed_input(p,0,1, "\\  \n")
		feed_input(p,1,0,"  \\ \n")
		feed_input(p,2,0,"   \\\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((2,  "\\   \n"),
				 (0,"   \\  \n"),
				 (0,"    \\ \n"),
				 (0,"      "   ))
		s = core.M_OCCUPIED|core.M_LINE_START_SE
		o = core.M_OCCUPIED
		n = core.M_NONE
		a = core.M_LINE_AFTER_SE
		meta =  ((    s,n,n,n,n,),
				 (n,n,n,o,n,n,n,),
				 (n,n,n,n,o,n,n,),
				 (n,n,n,n,n,a,  )) 
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
	
	def test_render_coordinates_shorter(self):
		l = self.do_render(6,3,1)[0]
		self.assertEquals((6,3),l.a)
		self.assertEquals((7,4),l.b)

	def test_render_z(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals("black",l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.STROKE_SOLID,l.stype)	
	
	
class TestVertLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.VertLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "| \n")
		feed_input(p,1,0,"  | \n")
		feed_input(p,2,0,"  | \n")
		feed_input(p,3,0,"   ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,3," ",core.M_NONE))
			
	def test_expects_start_pipe(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,0," ",core.M_NONE))
			
	def test_expects_start_pipe_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,0,"|",core.M_OCCUPIED))
			
	def test_allows_rest_of_start_line(self):
		p = self.pclass()
		feed_input(p,0,0,"|")
		p.test(main.CurrentChar(0,1,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,2,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,3,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,2,"|\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		
	def test_accepts_single_char_line(self):
		p = self.pclass()
		feed_input(p,0,1, "|\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2," ",core.M_NONE))
	
	def test_accepts_rest_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,1, "|\n")
		feed_input(p,1,0," |")
		p.test(main.CurrentChar(1,2,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,3,"\n",core.M_OCCUPIED))
		
	def test_allows_no_character_at_end_due_to_eoi(self):
		p = self.pclass()
		feed_input(p,0,1, "| \n")
		feed_input(p,1,0," | \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "| \n")
		feed_input(p,1,0,"  | \n")
		feed_input(p,2,0,"\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0," ",core.M_NONE))
			
	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,1, "| \n")
		feed_input(p,1,0," | \n")
		feed_input(p,2,0," ")
		p.test(main.CurrentChar(2,1,"|",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,2," ",core.M_NONE))
			
	def test_allows_line_to_end_at_bottom_left(self):
		p = self.pclass()
		feed_input(p,0,0,"| \n")
		feed_input(p,1,0,"| \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_line_to_end_at_bottom_right(self):
		p = self.pclass()
		feed_input(p,0,2,  "|\n")
		feed_input(p,1,0,"  |\n")
		feed_input(p,2,0,"  |\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((2,  "|  \n"),
				 (0,"  |  \n"),
				 (0,"  |  \n"),
				 (0,"   "    ))
		s = core.M_OCCUPIED|core.M_LINE_START_S
		o = core.M_OCCUPIED
		n = core.M_NONE
		a = core.M_LINE_AFTER_S
		meta =  ((    s,n,n,n,),
				 (n,n,o,n,n,n,),
				 (n,n,o,n,n,n,),
				 (n,n,a,      )) 
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,startcol+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)
				
	def do_render(self,x,y,l):
		p = self.pclass()
		for i in range(l):
			feed_input(p,y+i,x,"|\n")
			feed_input(p,y+i+1,0," "*x)			
		feed_input(p,y+l,x," ")
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
	
	def test_render_coordinates_shorter(self):
		l = self.do_render(6,3,1)[0]
		self.assertEquals((6.5,3),l.a)
		self.assertEquals((6.5,4),l.b)

	def test_render_z(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals("black",l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.STROKE_SOLID,l.stype)	
				
				
class TestHorizLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.HorizLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "--- ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,4," ",core.M_NONE))
			
	def test_expects_start_hyphen(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,0," ",core.M_NONE))
			
	def test_expects_start_hyphen_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,0,"-",core.M_OCCUPIED))
			
	def test_accepts_single_char_line(self):
		p = self.pclass()
		feed_input(p,0,1, "- ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
			
	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "---\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,0," ",core.M_NONE))
			
	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,1, "---")
		p.test(main.CurrentChar(0,4,"-",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,5," ",core.M_NONE))
			
	def test_allows_line_to_end_at_bottom_right(self):
		p = self.pclass()
		feed_input(p,2,2,"---\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
					
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((2,  "--- "),)
		s = core.M_OCCUPIED|core.M_LINE_START_E
		o = core.M_OCCUPIED
		n = core.M_NONE
		a = core.M_LINE_AFTER_E
		meta =  ((s,o,o,a,),)
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,startcol+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)
				
	def do_render(self,x,y,l):
		p = self.pclass()
		feed_input(p,y,x,"-"*l + " ")
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
	
	def test_render_coordinates_shorter(self):
		l = self.do_render(6,3,1)[0]
		self.assertEquals((6,3.5),l.a)
		self.assertEquals((7,3.5),l.b)

	def test_render_z(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals("black",l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.STROKE_SOLID,l.stype)	


class TestUpDiagDashedLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.UpDiagDashedLinePattern
		
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
			p.test(main.CurrentChar(0,0," ",core.M_NONE))
				
	def test_expects_start_comma_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,0,",",core.M_OCCUPIED))
			
	def test_allows_rest_of_start_line(self):
		p = self.pclass()
		feed_input(p,0,0,",")
		p.test(main.CurrentChar(0,1,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,2,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,3,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,2,",\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
	
	def test_accepts_single_char_line(self):
		p = self.pclass()
		feed_input(p,0,2,  ",\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2," ",core.M_NONE))
	
	def test_accepts_rest_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,2,  ",\n")
		feed_input(p,1,0," ,")
		p.test(main.CurrentChar(1,2,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,3,"\n",core.M_OCCUPIED))
	
	def test_allows_no_character_at_end_due_to_eoi(self):
		p = self.pclass()
		feed_input(p,0,2,  ",  \n")
		feed_input(p,1,0," , \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0,core.END_OF_INPUT,core.M_NONE))
	
	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,3,   ",  \n")
		feed_input(p,1,0,"  ,   \n")
		feed_input(p,2,0,"\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0," ",core.M_NONE))
		
	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,2,  ",\n")
		feed_input(p,1,0," ")
		p.test(main.CurrentChar(1,1,",",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2," ",core.M_NONE))
	
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
	
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((3,   ",  \n"),
				 (0,"  ,   \n"),
				 (0," ,    \n"),
				 (0," "       ))
		s = core.M_OCCUPIED|core.M_LINE_START_SW|core.M_DASH_START_SW
		o = core.M_OCCUPIED
		n = core.M_NONE
		a = core.M_LINE_AFTER_SW|core.M_DASH_AFTER_SW
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
	
	def test_render_coordinates_shorter(self):
		l = self.do_render(6,3,1)[0]
		self.assertEquals((7,3),l.a)
		self.assertEquals((6,4),l.b)

	def test_render_z(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals("black",l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.STROKE_DASHED,l.stype)


class TestDownDiagLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.DownDiagDashedLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,1, "`   \n")
		feed_input(p,1,0,"  `  \n")
		feed_input(p,2,0,"   ` \n")
		feed_input(p,3,0,"     ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,4," ",core.M_NONE))
			
	def test_expects_start_backtick(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,0," ",core.M_NONE))
			
	def test_expects_start_backtick_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,0,"`",core.M_OCCUPIED))
			
	def test_allows_rest_of_start_line(self):
		p = self.pclass()
		feed_input(p,0,0,"`")
		p.test(main.CurrentChar(0,1,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,2,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,3,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,1,"`\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		
	def test_accepts_single_char_line(self):
		p = self.pclass()
		feed_input(p,0,1, "`\n")
		feed_input(p,1,0,"   ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2," ",core.M_NONE))
	
	def test_accepts_rest_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,1, "`\n")
		feed_input(p,1,0,"  `")
		p.test(main.CurrentChar(1,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,4,"\n",core.M_OCCUPIED))
		
	def test_allows_no_character_at_end_due_to_eoi(self):
		p = self.pclass()
		feed_input(p,0,1, "`  \n")
		feed_input(p,1,0,"  ` \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,1, "`  \n")
		feed_input(p,1,0,"  ` \n")
		feed_input(p,2,0," \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0," ",core.M_NONE))
			
	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,1, "` \n")
		feed_input(p,1,0,"  ")
		p.test(main.CurrentChar(1,2,"\\",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,3," ",core.M_NONE))
			
	def test_allows_line_to_end_at_right_edge(self):
		p = self.pclass()
		feed_input(p,0,1, "`  \n")
		feed_input(p,1,0,"  ` \n")
		feed_input(p,2,0,"   `\n")
		feed_input(p,3,0,"    \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(4,0," ",core.M_NONE))
			
	def test_allows_line_to_end_at_bottom_right_corner(self):
		p = self.pclass()
		feed_input(p,0,1, "`  \n")
		feed_input(p,1,0,"  ` \n")
		feed_input(p,2,0,"   `\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((2,  "`   \n"),
				 (0,"   `  \n"),
				 (0,"    ` \n"),
				 (0,"      "   ))
		s = core.M_OCCUPIED|core.M_LINE_START_SE|core.M_DASH_START_SE
		o = core.M_OCCUPIED
		n = core.M_NONE
		a = core.M_LINE_AFTER_SE|core.M_DASH_AFTER_SE
		meta =  ((    s,n,n,n,n,),
				 (n,n,n,o,n,n,n,),
				 (n,n,n,n,o,n,n,),
				 (n,n,n,n,n,a,  )) 
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
	
	def test_render_coordinates_shorter(self):
		l = self.do_render(6,3,1)[0]
		self.assertEquals((6,3),l.a)
		self.assertEquals((7,4),l.b)

	def test_render_z(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals("black",l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.STROKE_DASHED,l.stype)	
	

class TestVertDashedLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.VertDashedLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "; \n")
		feed_input(p,1,0,"  ; \n")
		feed_input(p,2,0,"  ; \n")
		feed_input(p,3,0,"   ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,3," ",core.M_NONE))
			
	def test_expects_start_semicolon(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,0," ",core.M_NONE))
			
	def test_expects_start_semicolon_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,0,";",core.M_OCCUPIED))
			
	def test_allows_rest_of_start_line(self):
		p = self.pclass()
		feed_input(p,0,0,";")
		p.test(main.CurrentChar(0,1,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,2,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,3,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,2,";\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		
	def test_accepts_single_char_line(self):
		p = self.pclass()
		feed_input(p,0,1, ";\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,2," ",core.M_NONE))
	
	def test_accepts_rest_of_next_line(self):
		p = self.pclass()
		feed_input(p,0,1, ";\n")
		feed_input(p,1,0," ;")
		p.test(main.CurrentChar(1,2,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,3,"\n",core.M_OCCUPIED))
		
	def test_allows_no_character_at_end_due_to_eoi(self):
		p = self.pclass()
		feed_input(p,0,1, "; \n")
		feed_input(p,1,0," ; \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "; \n")
		feed_input(p,1,0,"  ; \n")
		feed_input(p,2,0,"\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0," ",core.M_NONE))
			
	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,1, "; \n")
		feed_input(p,1,0," ; \n")
		feed_input(p,2,0," ")
		p.test(main.CurrentChar(2,1,";",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,2," ",core.M_NONE))
			
	def test_allows_line_to_end_at_bottom_left(self):
		p = self.pclass()
		feed_input(p,0,0,"; \n")
		feed_input(p,1,0,"; \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(2,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_line_to_end_at_bottom_right(self):
		p = self.pclass()
		feed_input(p,0,2,  ";\n")
		feed_input(p,1,0,"  ;\n")
		feed_input(p,2,0,"  ;\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((2,  ";  \n"),
				 (0,"  ;  \n"),
				 (0,"  ;  \n"),
				 (0,"   "    ))
		s = core.M_OCCUPIED|core.M_LINE_START_S|core.M_DASH_START_S
		o = core.M_OCCUPIED
		n = core.M_NONE
		a = core.M_LINE_AFTER_S|core.M_DASH_AFTER_S
		meta =  ((    s,n,n,n,),
				 (n,n,o,n,n,n,),
				 (n,n,o,n,n,n,),
				 (n,n,a,      )) 
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,startcol+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)
				
	def do_render(self,x,y,l):
		p = self.pclass()
		for i in range(l):
			feed_input(p,y+i,x,";\n")
			feed_input(p,y+i+1,0," "*x)			
		feed_input(p,y+l,x," ")
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
	
	def test_render_coordinates_shorter(self):
		l = self.do_render(6,3,1)[0]
		self.assertEquals((6.5,3),l.a)
		self.assertEquals((6.5,4),l.b)

	def test_render_z(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals("black",l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3,3)[0]
		self.assertEquals(core.STROKE_DASHED,l.stype)	


class TestHorizDashedLinePattern(unittest.TestCase,PatternTests):
	
	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.HorizDashedLinePattern
		
	def test_accepts_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "- - -  ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,9," ",core.M_NONE))
	
	def test_expects_start_hyphen(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,0," ",core.M_NONE))
	
	def test_expects_start_hyphen_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,0,"-",core.M_OCCUPIED))
			
	def test_expects_space_after_hypen(self):
		p = self.pclass()
		feed_input(p,0,2,"-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"-",core.M_NONE))
			
	def test_space_after_hyphen_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,"-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_OCCUPIED))
	
	def test_expects_space_after_second_hyphen(self):
		p = self.pclass()
		feed_input(p,0,2,"- -")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"-",core.M_NONE))
			
	def test_expects_space_after_second_hyphen_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,"- -")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_OCCUPIED))
		
	def test_doesnt_accept_two_char_line(self):
		p = self.pclass()
		feed_input(p,0,1, "- ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3," ",core.M_NONE))
	
	def test_allows_no_character_at_end_due_to_short_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "- - \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(1,0," ",core.M_NONE))
	
	def test_allows_line_to_end_at_occupied_line(self):
		p = self.pclass()
		feed_input(p,0,1, "- - ")
		p.test(main.CurrentChar(0,5,"-",core.M_OCCUPIED))
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(0,6," ",core.M_NONE))
	
	def test_allows_line_to_end_at_bottom_right(self):
		p = self.pclass()
		feed_input(p,2,2,"- - \n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
	
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((2,  "- - - -  "),)
		s = core.M_OCCUPIED|core.M_LINE_START_E|core.M_DASH_START_E
		o = core.M_OCCUPIED
		n = core.M_NONE
		a = core.M_LINE_AFTER_E|core.M_DASH_AFTER_E
		meta =  ((s,o,o,o,o,o,o,o,a,),)
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,startcol+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)
	
	def do_render(self,x,y,l):
		p = self.pclass()
		feed_input(p,y,x,"- "*(l//2) + " ")
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

	def test_render_z(self):
		l = self.do_render(3,3,4)[0]
		self.assertEquals(0,l.z)
		
	def test_render_stroke_colour(self):
		l = self.do_render(3,3,4)[0]
		self.assertEquals("black",l.stroke)
	
	def test_render_stroke_width(self):
		l = self.do_render(3,3,4)[0]
		self.assertEquals(1,l.w)
	
	def test_render_stroke_style(self):
		l = self.do_render(3,3,4)[0]
		self.assertEquals(core.STROKE_DASHED,l.stype)	


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
		arms = find_with(self,filter(lambda x: isinstance(x,core.Line), r),"a",(2,3.25))
		self.assertEquals((2,3.25),arms.a)
		self.assertEquals((5,3.25),arms.b)
		lleg = find_with(self,filter(lambda x: isinstance(x,core.Line), r),"b",(2.5,4.8))
		self.assertEquals((3.5,3.8),lleg.a)
		self.assertEquals((2.5,4.8),lleg.b)
		rleg = find_with(self,filter(lambda x: isinstance(x,core.Line), r),"b",(4.5,4.8))
		self.assertEquals((3.5,3.8),rleg.a)
		self.assertEquals((4.5,4.8),rleg.b)

	def test_render_z(self):
		r = self.do_render(3,2)
		for shape in r:
			self.assertEquals(0,shape.z)
			
	def test_render_stroke_colour(self):
		r = self.do_render(3,2)
		for shape in r:
			self.assertEquals("black",shape.stroke)
			
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
		l = find_with(self,r,"b",(2,2))
		self.assertEquals((2.5,2.5),l.a)
		
	def test_render_coordinates_north(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_S)
		l = find_with(self,r,"b",(2.5,2))
		self.assertEquals((2.5,2.5),l.a)
		
	def test_render_coordinates_northeast(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_SW)
		l = find_with(self,r,"b",(3,2))
		self.assertEquals((2.5,2.5),l.a)
		
	def test_render_coordinates_east(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_START_E)
		l = find_with(self,r,"b",(3,2.5))
		self.assertEquals((2.5,2.5),l.a)
		
	def test_render_coordinates_southeast(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_START_SE)
		l = find_with(self,r,"b",(3,3))
		self.assertEquals((2.5,2.5),l.a)
		
	def test_render_coordinates_south(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_START_S)
		l = find_with(self,r,"b",(2.5,3))
		self.assertEquals((2.5,2.5),l.a)
		
	def test_render_coordinates_southwest(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_START_SW)
		l = find_with(self,r,"b",(2,3))
		self.assertEquals((2.5,2.5),l.a)
		
	def test_render_coordinates_west(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_S)
		l = find_with(self,r,"b",(2,2.5))
		self.assertEquals((2.5,2.5),l.a)
		
	def test_render_coordinates_position(self):
		r = self.do_render(4,6,core.M_LINE_AFTER_E|core.M_LINE_AFTER_S)
		l1 = find_with(self,r,"b",(4,6.5))
		self.assertEquals((4.5,6.5),l1.a)
		l2 = find_with(self,r,"b",(4.5,6))
		self.assertEquals((4.5,6.5),l2.a)	
	
	def test_render_z(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_S)
		for shape in r:
			self.assertEquals(0,shape.z)
	
	def test_render_stroke_colour(self):
		r = self.do_render(2,2,core.M_LINE_AFTER_E|core.M_LINE_AFTER_S)
		for shape in r:
			self.assertEquals("black",shape.stroke)
			
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
		l1 = find_with(self,r,"b",(2,2.5))
		self.assertEquals(core.STROKE_DASHED,l1.stype)
		l2 = find_with(self,r,"b",(2.5,2))
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
			self.assertEquals("black",shape.stroke)
			
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
		self.assertEquals(1,len(find_type(self,r,core.Line)))
		self.assertEquals(1,len(find_type(self,r,core.Arc)))
		
	def test_render_coordinates(self):
		r = self.do_render(3,2,core.M_NONE)
		l = find_type(self,r,core.Line)[0]
		self.assertEquals((3,2.5),l.a)
		self.assertEquals((4,2.5),l.b)
		a = find_type(self,r,core.Arc)[0]
		self.assertEquals((2.9,2),a.a)
		self.assertEquals((4.1,3),a.b)
		self.assertEquals(math.pi/2,a.start)
		self.assertEquals(math.pi/2*3,a.end)
	
	def test_render_coorinates_position(self):
		r = self.do_render(6,5,core.M_NONE)
		l = find_type(self,r,core.Line)[0]
		self.assertEquals((6,5.5),l.a)
		self.assertEquals((7,5.5),l.b)
		a = find_type(self,r,core.Arc)[0]
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
			self.assertEquals("black",shape.stroke)
			
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
		a = find_type(self,self.do_render(3,2,core.M_NONE),core.Arc)[0]
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
		self.assertEquals(1,len(find_type(self,r,core.Line)))
		self.assertEquals(1,len(find_type(self,r,core.Arc)))
		
	def test_render_coordinates(self):
		r = self.do_render(3,2,core.M_NONE)
		l = find_type(self,r,core.Line)[0]
		self.assertEquals((3,2.5),l.a)
		self.assertEquals((4,2.5),l.b)
		a = find_type(self,r,core.Arc)[0]
		self.assertEquals((2.9,2),a.a)
		self.assertEquals((4.1,3),a.b)
		self.assertEquals(-math.pi/2,a.start)
		self.assertEquals(math.pi/2,a.end)
	
	def test_render_coorinates_position(self):
		r = self.do_render(6,5,core.M_NONE)
		l = find_type(self,r,core.Line)[0]
		self.assertEquals((6,5.5),l.a)
		self.assertEquals((7,5.5),l.b)
		a = find_type(self,r,core.Arc)[0]
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
			self.assertEquals("black",shape.stroke)
			
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
		a = find_type(self,self.do_render(3,2,core.M_NONE),core.Arc)[0]
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
		self.assertEquals(1,len(find_type(self,r,core.Line)))
		self.assertEquals(1,len(find_type(self,r,core.Arc)))
		
	def test_render_coordinates(self):
		r = self.do_render(3,2,core.M_NONE)
		l = find_type(self,r,core.Line)[0]
		self.assertEquals((3.5,2),l.a)
		self.assertEquals((3.5,3),l.b)
		a = find_type(self,r,core.Arc)[0]
		self.assertEquals((3,2.1),a.a)
		self.assertEquals((4,2.9),a.b)
		self.assertEquals(math.pi/2*2,a.start)
		self.assertEquals(math.pi/2*4,a.end)
	
	def test_render_coorinates_position(self):
		r = self.do_render(6,5,core.M_NONE)
		l = find_type(self,r,core.Line)[0]
		self.assertEquals((6.5,5),l.a)
		self.assertEquals((6.5,6),l.b)
		a = find_type(self,r,core.Arc)[0]
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
			self.assertEquals("black",shape.stroke)
			
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
		a = find_type(self,self.do_render(3,2,core.M_NONE),core.Arc)[0]
		self.assertEquals(None,a.fill)		
	
	
unittest.main()
