#! /usr/bin/env python
import datetime
import sys
import time

def parse_times(filename):
    x = []
    for line in open(filename):
        name, stage, tstamp = line.strip().split(' ', 2)
        tstamp = datetime.datetime.strptime(tstamp, '%a %b %d %H:%M:%S %Z %Y')

        x.append((name, stage, tstamp))

    return x

def extract_diffs(x):
    y = []
    for i in range(0, len(x), 2):
        assert x[i][1] == 'start'
        start_time = x[i][2]

        assert x[i+1][1] == 'stop'
        end_time = x[i+1][2]

        start_time = time.mktime(start_time.timetuple())
        end_time = time.mktime(end_time.timetuple())

        y.append((end_time - start_time, x[i][0]))
    return y

def main():
    filename = sys.argv[1]
    x = parse_times(filename)
    y = extract_diffs(x)

    for diff, size in y:
        print size, diff

if __name__ == '__main__':
    main()
