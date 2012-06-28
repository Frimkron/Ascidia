P_IGNORED = "IGNORED"
P_ACCEPTED = "ACCEPTED"
P_FINISHED = "FINISHED"
P_ABORTED = "ABORTED"


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

# TODO: data structure for looking up instances by their characters 
# or vice versa

if __name__ == "__main__":

	INPUT = """\
+---+  +-<>  ---+ +-------+  
|   |  |  +------+| +---+ |  
+---+--+  | ***  || |   | |  
    |  |  +------+| +---+ |  
    +--+          +-------+  """
	
	
	
	ongoing = []
	for pgen in PATTERNS:
		for j,line in enumerate(INPUT.splitlines()):
			for i,c in enumerate(line):
				newp = pgen()
				newp.next()
				ongoing.append(newp)
				toremove = []
				for p in ongoing:
					r = p.send((j,i,c))
					if r == P_ABORTED: 
						toremove.append(p)
					elif r == P_FINISHED:
						print "matched %s at line %d char %d" % (pgen.__name__,(j+1),(i+1))
						toremove.append(p)
				else:
					for p in toremove:
						ongoing.remove(p)
				
	
	
	
