import random, time, pbfmp, sys
import multiprocessing as mp

def basic_function(header, pstatus, pid):
    for i in range(100):
        time.sleep(random.random())
        pstatus[pid] += 1


def progbar_implement():
    pb_update_interval = 1
    end_msg =  'all downloads complete'
    pname_prefix = "Process "
    header = "Updating Database"
    nprocs = mp.cpu_count()

    pnames = []
    #pstatus = collections.OrderedDict()
    manager = mp.Manager()
    pstatus = manager.dict()
    procs = []
    pbars = []
    for i in range(nprocs):
        pnames.append(pname_prefix + str(i+1))
        pstatus[i] = 0
        pbars.append(pbfmp.ProgressBar(widgets=[('%s' % pnames[i]), ' ', pbfmp.Percentage(), ' ', pbfmp.Bar('=', '[', ']'), ' ', pbfmp.ETA()], maxval=100).start())
        child = mp.Process(target=basic_function, args=[header, pstatus, i])
        procs.append(child)
        child.start()


    sys.stderr.write('\033[2J\033[H') #clear screen
    print header
    while any(i.is_alive() for i in procs):
        time.sleep(pb_update_interval)
        sys.stderr.write('\033[2J\033[H') #clear screen
        print header
        for i, pbar in enumerate(pbars):
            pbar.update(pstatus[i])
    print end_msg


progbar_implement()
