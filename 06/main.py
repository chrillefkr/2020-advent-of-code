#!/usr/bin/python3

import sys
import argparse

from signal import signal, SIGPIPE, SIG_DFL



if __name__ == "__main__":
    signal(SIGPIPE, SIG_DFL)

    parser = argparse.ArgumentParser(description="Advent of Code 2020 Day 6: Custom Customs.\nRequires input file either as argument or STDIN")
    parser.add_argument('input', type=argparse.FileType('r'), default=(None if sys.stdin.isatty() else sys.stdin), nargs='?', help="input file or STDIN")
    args = parser.parse_args()

    if not args.input:
        print("Missing input\n", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    inp = args.input.read()

    groups = inp.split("\n\n")
    group_answers = []

    for group in groups:
        persons_votes = group.split("\n")
        answers = set()
        for person_votes in persons_votes:
            answers.update(person_votes)
        group_answers.append(answers)

    answer_amounts = map(len, group_answers)
    summary = sum(answer_amounts)
    print("Sum: %i" % (summary))

