#!/usr/bin/python3

import sys
import re
from pprint import pprint

from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE,SIG_DFL)

inp = sys.stdin.read()
lines = inp.split('\n')

p = re.compile(r'^([0-9]+)-([0-9]+) (.): (.*)$')

for line in lines:
	if not line:
		continue
	fr, to, ch, password = p.findall(line)[0]
	fr = int(fr)
	to = int(to)
	#pprint((fr, to, ch, password))
	count = password.count(ch)
	#if count >= fr and count <= to:
	#	print("%s VALID" % line.ljust(30))
	#else:
	#	print("%s INVALID" % line.ljust(30))
	
	""" Star 2 """
	len_check = len(password) > max(fr, to) - 1
	first_check = len_check and password[fr-1] == ch
	second_check = len_check and password[to-1] == ch
	third_check = first_check ^ second_check
	#pprint((first_check, second_check, third_check))
	if third_check:
		print("%s NEW VALID" % line.ljust(30))
	else:
		print("%s NEW INVALID" % line.ljust(30))
