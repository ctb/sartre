#! /usr/bin/env python
import datetime
from collections import namedtuple
import time
import sys
import sarparse

def main():
    _, timelog = sarparse.parse_timelog('times.out')
    timelog_start = timelog[0][2]
    timelog_end = timelog[-1][2]
    ram_data = sarparse.parse_sar_ram('ram.txt.gz')
    cpu_data = sarparse.parse_sar_cpu('cpu.txt.gz')
    disk_data = sarparse.parse_sar_disk('disk.txt.gz', 'xvdb')
    
    sar_start = sarparse.get_sar_start_time(cpu_data, timelog[0].timestamp)
    secdata = sarparse.make_timediff(cpu_data)

    print >>sys.stderr, 'started sar at', sar_start
    print >>sys.stderr, 'sampling rate:', secdata, 'seconds'

    ram_data = sarparse.fixtime(ram_data, sar_start, secdata)
    cpu_data = sarparse.fixtime(cpu_data, sar_start, secdata)
    disk_data = sarparse.fixtime(disk_data, sar_start, secdata)

    fp = open('log.out', 'w')
    for x, y, z in zip(cpu_data, ram_data, disk_data):
        assert x.time == y.time
        if x.time < timelog_start:
            continue
        if x.time > timelog_end:
            break

        print >>fp, sarparse.make_time(x.time, timelog_start),\
              x.puser, y.kbmemused, \
              z.tps, z.reads, z.writes, z.await, z.putil

    for script, what, when in timelog:
        if what == 'DONE':
            print >>sys.stderr, script, sarparse.make_time(when, timelog_start)

    print 'duration:', sarparse.make_time(timelog_end) - \
          sarparse.make_time(timelog_start)

if __name__ == '__main__':
    main()
