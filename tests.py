import unittest
import core
import patterns
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
	
	
unittest.main()
