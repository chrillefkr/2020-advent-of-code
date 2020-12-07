#!/usr/bin/python3

import sys
import re
#from pprint import pprint

from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE,SIG_DFL)

expected_res = int(sys.argv[1]) if len(sys.argv) >= 2 else 0

inp = sys.stdin.read()
lines = inp.split('\n')

p = re.compile(r'^[0-9]+$')
valid_lines = [ s for s in lines if p.match(s) ]

nums = list(map(int, valid_lines))

for idx, num in enumerate(nums):
	# print("[%d] %d" % (idx, num))
	for idx2, num2 in enumerate(nums[idx + 1:]):
		res = num + num2
		# print("\t %d * [%d] %d = %d" % (num, idx2, num2, res))
		if res == expected_res:
			print("Success! %d + %d = %d" % (num, num2, res))
			print("%d * %d = %d" % (num, num2, num * num2))
			break
	else:
		continue
	break
