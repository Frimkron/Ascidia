import unittest
import core
import patterns
import main
import io
import xml.dom.minidom

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
	
unittest.main()
