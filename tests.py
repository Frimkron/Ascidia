import unittest
import core
import patterns
import main

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


# TODO
class TestSvgOutput(unittest.TestCase):
	pass
		
	
unittest.main()
