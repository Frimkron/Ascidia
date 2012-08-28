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
