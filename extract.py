#! /usr/bin/env python
import datetime
from collections import namedtuple

def parse_timelog(filename):
    d = {}

    parsed = []
    for line in open(filename):
        script, stage, tstamp = line.strip().split(' ', 2)
        tstamp = datetime.datetime.strptime(tstamp, '%a %b %d %H:%M:%S %Z %Y')
        parsed.append((script, stage, tstamp))

    return d, parsed

def parse_sar_cpu(filename):
    parsed = []

    #09:40:03 PM     CPU     %user     %nice   %system   %iowait    %steal     %idle
    typ = namedtuple('CPUUsage', 'time cpu puser pnice psystem piowait psteal pidle')
    for n, line in enumerate(open(filename)):
        if n < 3:
            continue
        if line.startswith('Average'):
            continue

        line = line.strip().split()
        assert len(line) == 9, len(line)
        line2 = [line[0] + ' ' + line[1], line[2]]
        line2.extend(( float(x) for x in line[3:]))

        print line2

        t = typ(*line2)
        parsed.append(t)

    return parsed
    

def parse_sar_ram(filename):
    parsed = []

    # 09:40:03 PM kbmemfree kbmemused  %memused kbbuffers  kbcached  kbcommit   %commit kbactive   kbinact   kbdirty
    typ = namedtuple('MemoryUsage', 'time kbmemfree kbmemused pmemused kbbuffers kbcached kbcommit pcommit kbactive kbinact kbdirty')
    
    for n, line in enumerate(open(filename)):
        if n < 3:
            continue
        if line.startswith('Average'):
            continue

        line = line.strip().split()
        assert len(line) == 12, len(line)
        line2 = [line[0] + ' ' + line[1]]
        line2.extend(( float(x) for x in line[2:]))

        t = typ(*line2)
        parsed.append(t)

    return parsed


def main():
    #print parse_timelog('times.out')
    #print parse_sar_ram('r.txt')
    print parse_sar_cpu('u.txt')

if __name__ == '__main__':
    main()
