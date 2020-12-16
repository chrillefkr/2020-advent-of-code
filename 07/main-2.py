#!/usr/bin/python3

import sys
import argparse
import re

from signal import signal, SIGPIPE, SIG_DFL

from pprint import pprint

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


""" Flatten 2d array to 1d array. Instead of itertools.flatten etc """
def flatten(l):
    out = []
    for o in l:
        out.extend(o)
    return out


if __name__ == "__main__":
    signal(SIGPIPE, SIG_DFL)

    parser = argparse.ArgumentParser(description="Advent of Code 2020 Day 7: Handy Haversacks.\nRequires input file either as argument or STDIN")
    parser.add_argument('input', type=argparse.FileType('r'), default=(None if sys.stdin.isatty() else sys.stdin), nargs='?', help="input file or STDIN")
    parser.add_argument('-c', '--color', type=str, default="shiny gold", nargs='?', help="color of target bag")
    args = parser.parse_args()

    if not args.input:
        print("Missing input\n", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)

    inp = args.input.read()

    lines = filter(bool, inp.split('\n'))
    child_regex = re.compile(r'^(\d+) (.*)$')
    remove_bags_regex = re.compile(r' bags?\.?$')

    rules = {}

    for line in lines:
        parent, children_str = line.split(' bags contain ')
        children = []
        if children_str != "no other bags.":
            children = list(map(lambda s: child_regex.findall(s)[0], children_str.split(', ')))
        children = list(map(lambda x: (int(x[0]), remove_bags_regex.sub('', x[1])), children))
        contains = list(map(lambda x: { "color": x[1], "amount": x[0], "contains": [] }, children))
        rules[parent] = children
    
    child_colors = set([color[1] for color in rules[args.color]])
    already_checked = set()
    # already_checked = set()
    bag_counter = 0
    to_check = list(child_colors)

    depth = 1
    while True:
        if not len(to_check):
            break
        
        to_check_next = []
        print("to_check:", to_check)
        
        for test_color in to_check:
            count = sum([rule[0] for rule in rules[test_color]])
            bag_counter += count 
            print("%s: %d" % (test_color, count))
            # new_colors = set([color for color in rules if test_color in map(lambda b: b[1], rules[color])])
            new_colors = set([rule[1] for rule in rules[test_color]])
            to_check_next.extend([rule[1] for rule in rules[test_color]])
            child_colors.update(new_colors)

        to_check = to_check_next
        already_checked.update(to_check)
        depth += 1
    pprint(child_colors)
    pprint(bag_counter)
