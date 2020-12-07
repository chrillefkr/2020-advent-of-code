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

    groups = filter(bool, inp.split("\n\n"))
    group_answers = []
    group_intersect_answers = []

    for group in groups:
        persons_votes = filter(bool, group.split("\n"))
        answers = set()
        group_intersect_answer = set()
        group_intersect_answer_empty = False
        for person_votes in persons_votes:
            person_answer = set(person_votes)
            if group_intersect_answer:
                group_intersect_answer.intersection_update(person_answer)
            elif not group_intersect_answer_empty:
                group_intersect_answer.update(person_answer)
            
            if not group_intersect_answer: # intersection has emptied set.
                group_intersect_answer_empty = True
            answers.update(person_votes)
        group_answers.append(answers)
        group_intersect_answers.append(group_intersect_answer)

    answer_amounts = map(len, group_answers)
    answer_summary = sum(answer_amounts)
    
    intersect_amounts = map(len, group_intersect_answers)
    intersect_summary = sum(intersect_amounts)


    print("Sum: %i" % (answer_summary))
    print("Intersect sum: %i" % (intersect_summary))

