#! /usr/bin/env python
import datetime
from collections import namedtuple
import time
import sys
import gzip

def parse_timelog(filename):
    d = {}

    typ = namedtuple('TimelogEntry', 'script stage timestamp')

    parsed = []
    for line in open(filename):
        script, stage, tstamp = line.strip().split(' ', 2)
        tstamp = datetime.datetime.strptime(tstamp, '%a %b %d %H:%M:%S %Z %Y')
        parsed.append(typ(script, stage, tstamp))

    return d, parsed

def parse_sar_cpu(filename):
    parsed = []

    #09:40:03 PM     CPU     %user     %nice   %system   %iowait    %steal     %idle
    typ = namedtuple('CPUUsage', 'time cpu puser pnice psystem piowait psteal pidle')
    for n, line in enumerate(gzip.open(filename)):
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
    typ = namedtuple('MemoryUsage', 'time kbmemfree kbmemused pmemused kbbuffers kbcached kbcommit pcommit kbactive kbinact')
    
    for n, line in enumerate(gzip.open(filename)):
        if n < 3:
            continue
        if line.startswith('Average'):
            continue

        line = line.strip().split()
        assert len(line) >= 11, len(line)
        line2 = [line[0] + ' ' + line[1]]
        line2.extend(( float(x) for x in line[2:11]))

        t = typ(*line2)
        parsed.append(t)

    return parsed

def parse_sar_disk(filename, device):
    parsed = []

    # 06:21:38 PM       DEV       tps  rd_sec/s  wr_sec/s  avgrq-sz  avgqu-sz     await     svctm     %util
    typ = namedtuple('DeviceStats', 'time dev tps reads writes avgrqsz avgqusz await svctm putil')
    
    for n, line in enumerate(gzip.open(filename)):
        if n < 3:
            continue
        if line.startswith('Average'):
            continue

        line = line.strip().split()

        if line[2] != device:
            continue
        
        assert len(line) == 11, len(line)
        line2 = [line[0] + ' ' + line[1], line[2]]
        line2.extend(( float(x) for x in line[3:]))

        t = typ(*line2)
        parsed.append(t)

    return parsed

def parse_sartime(t):
    t = t.split(' ')[0]
    hour, minute, second = t.split(':')
    return int(hour), int(minute), int(second)

def get_sar_start_time(sar_data, timelog_data):
    sar_time = sar_data[0][0]
    timelog_time = timelog_data[0].timestamp

    hour, minute, second = parse_sartime(sar_time)

    d2 = datetime.datetime(timelog_time.year,
                          timelog_time.month,
                          timelog_time.day,
                          timelog_time.hour,
                          int(minute),
                          int(second))

    return d2

def make_timediff(sar_data):
    "Calculate sampling frequency in seconds. Must be less than 1 hr."
    t1 = parse_sartime(sar_data[0][0])
    t2 = parse_sartime(sar_data[1][0])

    assert t1[0] == t2[0]
    secdiff = (t2[1] - t1[1]) * 60 + t2[2] - t1[2]

    return secdiff

def fixtime(sar_data, start, secdiff):
    "Fix the hh::mm::ss timestamps output by 'sar' to full datetimes."
    delta = datetime.timedelta(0, secdiff)

    currentime = start 

    sar_data2 = []
    for x in sar_data:
        sar_data2.append(x._replace(time=currentime))
        currentime += delta

    return sar_data2

def make_time(x, start=None):
    "Convert datetimes into seconds with time.mktime, optionally - start."
    sub = 0
    if start:
        sub = time.mktime(start.timetuple())
    return time.mktime(x.timetuple()) - sub

def main():
    _, timelog = parse_timelog('times.out')
    timelog_start = timelog[0][2]
    timelog_end = timelog[-1][2]
    ram_data = parse_sar_ram('ram.txt.gz')
    cpu_data = parse_sar_cpu('cpu.txt.gz')
    disk_data = parse_sar_disk('disk.txt.gz', 'xvdb')
    print disk_data[:5]
    
    sar_start = get_sar_start_time(cpu_data, timelog)
    secdata = make_timediff(cpu_data)

    print >>sys.stderr, 'started sar at', sar_start
    print >>sys.stderr, 'sampling rate:', secdata, 'seconds'

    ram_data = fixtime(ram_data, sar_start, secdata)
    cpu_data = fixtime(cpu_data, sar_start, secdata)
    disk_data = fixtime(disk_data, sar_start, secdata)

    print ram_data[:2], len(ram_data)
    print cpu_data[:2], len(cpu_data)
    print disk_data[:2], len(disk_data)

    fp = open('log.out', 'w')
    for x, y, z in zip(cpu_data, ram_data, disk_data):
        assert x.time == y.time
        if x.time < timelog_start:
            continue
        if x.time > timelog_end:
            break

        print >>fp, make_time(x.time, timelog_start), x.puser, y.kbmemused, \
              z.tps, z.reads, z.writes, z.await, z.putil

    for script, what, when in timelog:
        if what == 'start':
            print >>sys.stderr, script, make_time(when, timelog_start)

    print 'duration:', make_time(timelog_end) - make_time(timelog_start)

if __name__ == '__main__':
    main()
