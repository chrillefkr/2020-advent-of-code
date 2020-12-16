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

    relationships = []

    for line in lines:
        parent, children_str = line.split(' bags contain ')
        children = []
        if children_str != "no other bags.":
            children = list(map(lambda s: child_regex.findall(s)[0], children_str.split(', ')))
        children = list(map(lambda x: (int(x[0]), remove_bags_regex.sub('', x[1])), children))
        contains = list(map(lambda x: { "color": x[1], "amount": x[0], "contains": [] }, children))
        root_bag = {
                "color": parent,
                "amount": None,
                "contains": contains,
        }
        relationships.append(root_bag)

    if args.ppc or args.pcc:
        sys.exit(0)
    
    extremities = relationships
    counter = 1
    amount_obj_iterated = 0
    while True:
        #pprint(extremities)
        #print(type(extremities[0]))
        extremities = flatten(map(lambda x: x['contains'], extremities))
        #pprint(extremities)
        if not len(extremities):
            break
        for extremity in extremities:
            #pprint(extremity)
            if len(extremity['contains']):
                # Circular, already populated.
                continue
            root_bag = next(bag for bag in relationships if bag["color"] == extremity["color"])
            #print("root_bag: ", end="")
            #pprint(root_bag)
            extremity['contains'] = root_bag['contains']
        print("len: %d" % (len(extremities)), file=sys.stderr)
        amount_obj_iterated += len(extremities)
        print("Iteration %d" % (counter), file=sys.stderr)
        counter += 1

    print("sum objects iterated: %d" % amount_obj_iterated)

    #pprint(relationships)
    print("done, printing json", file=sys.stderr)
    #import json
    #print(json.dumps(relationships, indent=4, sort_keys=True))
    #print(json.dumps(relationships))



    #print("Amount of bags applicable for holding '%s': %i" % (args.color, len(applicable_parent_bags)))

    # pprint(applicable_parent_bags)
