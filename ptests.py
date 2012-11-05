import unittest
import core
import patterns
import main


class PatternTests(object):

	pclass = None

	def test_can_construct(self):
		self.pclass()
		
	def test_raises_error_on_early_render(self):
		p = self.pclass()
		with self.assertRaises(core.PatternStateError):
			p.render()

	def find_with(self,items,property,value):
		for i in items:
			if getattr(i,property) == value:
				return i
		self.fail("%s not found in '%s' properties %s" % (str(value),property,
			str([getattr(i,property) for i in items])))
	
	
	def find_type(self,items,type):
		l = filter(lambda x: isinstance(x,type), items)
		if len(l) == 0:
			self.fail("No %ss in %s" % (str(type),str(items)))
		return l


def feed_input(pattern,row,col,characters):
	for char in characters:
		pattern.test(main.CurrentChar(row,col,char,core.M_NONE))
		col += 1



