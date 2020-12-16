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


if __name__ == "__main__":
    signal(SIGPIPE, SIG_DFL)

    parser = argparse.ArgumentParser(description="Advent of Code 2020 Day 7: Handy Haversacks.\nRequires input file either as argument or STDIN")
    parser.add_argument('input', type=argparse.FileType('r'), default=(None if sys.stdin.isatty() else sys.stdin), nargs='?', help="input file or STDIN")
    parser.add_argument('-c', '--color', type=str, default="shiny gold", nargs='?', help="color of bag")
    # parser.add_argument('-k', '--child-colors', dest='pcc', type=str2bool, default=False, const=True, nargs='?', help="print available child colors and exit")
    # parser.add_argument('-l', '--parent-colors', dest='ppc', type=str2bool, default=False, const=True, nargs='?', help="print available parent colors and exit")
    parser.add_argument('--child-colors', '-k', dest='pcc', action='store_true')
    parser.add_argument('--parent-colors', '-l', dest='ppc', action='store_true')
    args = parser.parse_args()

    if not args.input:
        print("Missing input\n", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)

    inp = args.input.read()

    lines = filter(bool, inp.split('\n'))
    child_regex = re.compile(r'^(\d+) (.*)$')
    remove_bags_regex = re.compile(r' bags?\.?$')

    all_parents = set()
    all_children = set()
    relationships = {}
    relationships_list = []

    for line in lines:
        parent, children_str = line.split(' bags contain ')
        children = []
        if children_str != "no other bags.":
            children = list(map(lambda s: child_regex.findall(s)[0], children_str.split(', ')))
        children = list(map(lambda x: (int(x[0]), remove_bags_regex.sub('', x[1])), children))
        relationships[parent] = children
        relationships_list.append((parent, children))
        
        all_parents.add(parent)
        all_children.update(map(lambda x: x[1], children))

    if args.ppc:
        [print(x) for x in all_parents]
    if args.pcc:
        [print(x) for x in all_children]

    if args.ppc or args.pcc:
        sys.exit(0)
    # pprint(relationships)

    applicable_parent_bags = list(filter(lambda x: args.color in map(lambda y: y[1], x[1]), relationships_list))
    applicable_tree = applicable_parent_bags[:]
    while true:
        for applicable_parent_bag in applicable_parent_bags:
            parent_parent = None

    print("Amount of bags applicable for holding '%s': %i" % (args.color, len(applicable_parent_bags)))

    # pprint(applicable_parent_bags)
