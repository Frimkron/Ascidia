P_IGNORED = "IGNORED"
P_ACCEPTED = "ACCEPTED"
P_FINISHED = "FINISHED"
P_ABORTED = "ABORTED"

from collections import defaultdict


def pattern_box():
	j,i,c = yield
	startx = i
	if c != "+": yield P_ABORTED
	while True:
		j,i,c = yield P_ACCEPTED
		if c == "+": break
		elif c != "-": yield P_ABORTED
	j,i,c = yield P_ACCEPTED
	while i!=startx:
		j,i,c = yield P_IGNORED
	if c != "|": yield P_ABORTED
	yield P_ACCEPTED
	yield P_FINISHED
	
def pattern_line():
	j,i,c = yield
	if c != "-": yield P_ABORTED
	while True:
		j,i,c = yield P_ACCEPTED
		if c != "-": break
	yield P_FINISHED
		
		
PATTERNS = [pattern_box,pattern_line]


class MatchLookup(object):

	_matches = None
	matches = property(lambda s: list(s._matches))	
	_match_by_pos = None
	match_by_pos = property(lambda s: dict(s._match_by_pos))
	_pos_by_match = None
	pos_by_match = property(lambda s: dict(s._pos_by_match))
	
	def __init__(self):
		self._matches = []
		self._match_by_pos = defaultdict(list)
		self._pos_by_match = defaultdict(list)
		
	def add_match(self,match):
		self._matches.append(match)
		
	def add_position(self,match,pos):
		self._match_by_pos[pos].append(match)
		self._pos_by_match[match].append(pos)
		
	def remove_match(self,match):
		try: 
			self._matches.remove(match)
		except ValueError: pass
		for p in self._pos_by_match[match]:
			try:
				self._match_by_pos[p].remove(match)
			except ValueError: pass
		try:
			del(self._pos_by_match[match])
		except KeyError: pass


if __name__ == "__main__":

	INPUT = """\
+---+  +-<>  ---+ +-------+  
|   |  |  +------+| +---+ |  
+---+--+  | ***  || |   | |  
    |  |  +------+| +---+ |  
    +--+          +-------+  """
		
	ongoing = MatchLookup()	
	for pgen in PATTERNS:
		for j,line in enumerate(INPUT.splitlines()):
			for i,c in enumerate(line):
				newp = pgen()
				newp.next()
				ongoing.add_match(newp)
				for p in ongoing.matches:
					if p in ongoing.matches:
						r = p.send((j,i,c))
						if r == P_ABORTED: 
							ongoing.remove_match(p)
						elif r == P_FINISHED:
							print "matched %s at line %d char %d: %s" % (
								pgen.__name__,(j+1),(i+1),str(ongoing.pos_by_match[p]))
							for pos in ongoing.pos_by_match[p]:
								for match in ongoing.match_by_pos[pos]:
									ongoing.remove_match(match)
							ongoing.remove_match(p)
						elif r == P_ACCEPTED:
							ongoing.add_position(p,(j,i))
				
	
	
	
