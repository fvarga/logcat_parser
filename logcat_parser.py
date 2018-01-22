import argparse
from datetime import datetime, timedelta


def open_file(file):
    with open(file) as f:
        f = f.read().splitlines()
    return f


def print_difference(file):
    f = open_file(file)
    start = 0
    stop = 0
    for line in f:
        if 'TEST STARTED' in line:
            print(line)
            start = line.split()[1]
        elif 'TEST FINISHED' in line:
            print(line)
            stop = line.split()[1]
        else:
            continue
    time = '%H:%M:%S.%f'
    delta = datetime.strptime(stop, time) - datetime.strptime(start, time)
    if delta.days < 0:
        delta = timedelta(days=0, seconds=delta.seconds, microseconds=delta.microseconds)
    print('Delta is: {}'.format(delta))


def lines_include(file, words):
    f = open_file(file)
    for line in f:
        if all(word in line for word in words):
            print(line)


def lines_exclude(file, words):
    f = open_file(file)
    for line in f:
        if not any(word in line for word in words):
            print(line)


parser = argparse.ArgumentParser(description='LogCat Search Tool')
parser.add_argument('file', help='path to the log file')
parser.add_argument('-s', dest='action', action='store_const', const=print_difference,
                    help='prints out the time difference between lines containing “TEST STARTED” and “TEST FINISHED"')
parser.add_argument('-i', dest='action', action='store_const', const=lines_include,
                    help='​prints out lines containing all arguments')
parser.add_argument('-e', dest='action', action='store_const', const=lines_exclude,
                    help='prints out all lines which don\'t contain any of provided arguments')
parser.add_argument('words', default=None, nargs='*', help='specify words to look for in the log file')
args = parser.parse_args()

if args.words:
    args.words = args.words[0].split(",")
    args.action(args.file, args.words)
else:
    try:
        args.action(args.file)
    except TypeError:
        print('Please provide arguments! See "{} -h"'.format(parser.prog))
