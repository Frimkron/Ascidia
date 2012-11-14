#!/usr/bin/python2

import json
import sys
import os
import subprocess

data = json.load(sys.stdin)
imgnum = 0
for i,item in enumerate(list(data[1])):
	try:
		cb = item["CodeBlock"]
	except KeyError: continue
	if map(unicode.lower,cb[0][1]) != ["ascidia"]: continue
	imgname = "diagram%s.png" % str(imgnum).rjust(4,"0")
	proc = subprocess.Popen(["ascidia","-o","%s" % imgname,"-q","-"],stdin=subprocess.PIPE)
	proc.communicate(cb[1])
	data[1][i] = { u"Para": [ { u"Image": [[],[unicode(imgname),u""]] } ] }
	imgnum += 1

json.dump(data,sys.stdout)
