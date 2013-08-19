#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, random, sys, collections
import multiprocessing as mp

class mpprogressbar(object):
    def __init__(self):
        self.pbar_names = []

    def append(self, pbar_name):
        self.pbar_names.append(pbar_name)

    def start(self, header, end_msg, interval):
        def download(status, filename):
            count = random.randint(5, 100)
            for i in range(count):
                status.put([filename, (i+1.0)/count])
                time.sleep(0.1)

        def print_progress(header, progress, elapsed):
            sys.stdout.write('\033[2J\033[H') #clear screen
            combined_perc = 0
            sys.stdout.write(header+"\n")
            for pname, percent in progress.items():
                bar = ('=' * int(percent * 20)).ljust(20)
                percent = int(percent * 100)
                combined_perc += percent
                sys.stdout.write("%s [%s] %3s%%\n" % (pname, bar, percent))
            sys.stdout.flush()

        status = mp.Queue()
        progress = collections.OrderedDict()
        workers = []
        for pname in self.pbar_names:
            child = mp.Process(target=download, args=(status, pname))
            child.start()
            workers.append(child)
            progress[pname] = 0.0

        stime = int(time.time())
        while any(i.is_alive() for i in workers):
            time.sleep(interval)
            while not status.empty():
                pname, percent = status.get()
                progress[pname] = percent
                now = int(time.time())
                print_progress(header, progress, (now - stime))
        print end_msg


