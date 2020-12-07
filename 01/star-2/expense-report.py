#!/usr/bin/python3

import sys
import re
#from pprint import pprint

expected_res = int(sys.argv[1]) if len(sys.argv) >= 2 else 0

inp = sys.stdin.read()
lines = inp.split('\n')

p = re.compile(r'^[0-9]+$')
valid_lines = [ s for s in lines if p.match(s) ]

nums = list(map(int, valid_lines))

for idx, num in enumerate(nums):
	#print("[%d] %d" % (idx, num))
	enum2 = enumerate(nums[idx + 1:])
	#enum2 = enumerate(nums)
	for idx2, num2 in enum2:
		absolute_idx2 = idx + idx2
		enum3 = enumerate(nums[absolute_idx2 + 1:])
		#enum3 = enumerate(nums)
		for idx3, num3 in enum3:
			absolute_idx3 = absolute_idx2 + idx3
			res = num + num2 + num3
			#print("%d + %d + %d = %d" % (num, num2, num3, res), end="")
			#print("\t %d:%d:%d" % (idx, absolute_idx2, absolute_idx3))
			if res == expected_res:
				print("Success!")
				print("%d + %d + %d = %d" % (num, num2, num3, res))
				print("%d * %d * %d = %d" % (num, num2, num3, num * num2 * num3))
				break
		else:
			continue
		break
		# res = num + num2
		# print("\t %d * [%d] %d = %d" % (num, idx2, num2, res))
		# if res == expected_res:
		# 	print("Success! %d + %d = %d" % (num, num2, res))
		# 	print("%d * %d = %d" % (num, num2, num * num2))
		# 	break
	else:
		continue
	break
