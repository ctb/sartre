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
    for i in range(0, len(x), 3):
        assert x[i][0] == 'bench'
        assert x[i][1] == 'starting'
        start_time = x[i][2]
        
        assert x[i+1][0].startswith('bench')
        _, size0 = x[i+1][0].split('-')
        size0 = float(size0)
        assert x[i+1][1] == 'postalloc'
        postalloc_time = x[i+1][2]

        _, size = x[i+2][0].split('-')
        size = float(size)
        assert x[i+2][1] == 'ending'
        end_time = x[i+2][2]

        start_time = time.mktime(start_time.timetuple())
        postalloc_time = time.mktime(postalloc_time.timetuple())
        end_time = time.mktime(end_time.timetuple())

        y.append((end_time - start_time, end_time - postalloc_time, size))
    return y

def main():
    filename = sys.argv[1]
    x = parse_times(filename)
    
    y = extract_diffs(x)

    for diff1, diff2, size in y:
        print size, diff1, diff2

if __name__ == '__main__':
    main()
