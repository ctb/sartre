#! /usr/bin/env python
import datetime
from collections import namedtuple
import time

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

def parse_sartime(t):
    t = t.split(' ')[0]
    hour, minute, second = t.split(':')
    return int(hour), int(minute), int(second)

def get_sar_start_time(sar_data, timelog_data):
    sar_time = sar_data[0][0]
    timelog_time = timelog_data[0][2]

    hour, minute, second = parse_sartime(sar_time)

    d2 = datetime.datetime(timelog_time.year,
                          timelog_time.month,
                          timelog_time.day,
                          timelog_time.hour,
                          int(minute),
                          int(second))

    return d2

def make_timediff(sar_data):
    t1 = parse_sartime(sar_data[0][0])
    t2 = parse_sartime(sar_data[1][0])

    assert t1[0] == t2[0]
    secdiff = (t2[1] - t1[1]) * 60 + t2[2] - t1[2]

    return secdiff

def fixtime(sar_data, start, secdiff):
    delta = datetime.timedelta(0, secdiff)

    currentime = start 

    sar_data2 = []
    for x in sar_data:
        sar_data2.append(x._replace(time=currentime))
        currentime += delta

    return sar_data2

def make_time(x, start=None):
    sub = 0
    if start:
        sub = time.mktime(start.timetuple())
    return time.mktime(x.timetuple()) - sub

def main():
    _, timelog = parse_timelog('times.out')
    timelog_start = timelog[0][2]
    timelog_end = timelog[-1][2]
    #print parse_sar_ram('r.txt')
    cpu_data = parse_sar_cpu('u.txt')
    sar_start = get_sar_start_time(cpu_data, timelog)
    secdata = make_timediff(cpu_data)

    cpu_data = fixtime(cpu_data, sar_start, secdata)

    for x in cpu_data:
        if x.time < timelog_start:
            continue
        if x.time > timelog_end:
            break
    
        print make_time(x.time, timelog_start), x.puser

    for script, what, when in timelog:
        if what == 'DONE':
            print script, make_time(when, timelog_start)

if __name__ == '__main__':
    main()
