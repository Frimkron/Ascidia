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



