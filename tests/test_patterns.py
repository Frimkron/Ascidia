import unittest

from ascidia import core
from ascidia import patterns
from ascidia import main


class PatternTests:

    pclass = None

    def test_can_construct(self):
        self.pclass()
        
    def test_raises_error_on_early_render(self):
        p = self.pclass()
        with self.assertRaises(core.PatternStateError):
            p.render()

    def find_with(self,items,properties,value=None):
        if not isinstance(properties,dict):
            properties = {properties: value}
        for i in items:
            for k,v in properties.items():
                try:
                    if getattr(i,k) != v: break
                except AttributeError: break
            else:
                return i
        expstr = "[" + ", ".join(["%s=%s" % tuple(map(str,p)) for p in properties.items()]) + "]"
        actstr = ", ".join([( "[" +
            ", ".join(["%s=%s" % (k,str(getattr(i,k,"<Not Found>"))) for k in properties.keys()]) 
                + "]" ) for i in items ])
        self.fail("%s not found in items %s" % (expstr,actstr))    
    
    def find_type(self,items,type):
        l = list(filter(lambda x: isinstance(x,type), items))
        if len(l) == 0:
            self.fail("No %ss in %s" % (str(type),str(items)))
        return l


def feed_input(pattern,row,col,characters):
    for char in characters:
        pattern.test(main.CurrentChar(row,col,char,core.M_NONE))
        col += 1



