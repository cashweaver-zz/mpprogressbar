import random, time, pbfmp, sys
import multiprocessing as mp

def do_stuff(header, pstatus, pid, pb_maxval):
    """
    Pretends to do work so we can see mpprogressbar in action.
    """
    for i in range(pb_maxval):
        time.sleep(random.random())
        pstatus[pid] += 1

def print_progressbars(pstatus, procs, pbars, header, pb_update_interval, end_msg):
    """
    Print all progress bars while any one is still running. Then print the
    end_msg
    """
    # Immediately clear the screen and print our header. Without this, if the
    # pb_update_interval is relatively long, the script will appear to 'hang',
    # even though it is running properly.
    sys.stderr.write('\033[2J\033[H') # clear screen
    print header
    # Continually update all progress bars so long as any one is still alive
    while any(p.is_alive() for p in procs):
        time.sleep(pb_update_interval)
        sys.stderr.write('\033[2J\033[H') # clear screen
        print header
        # progressbar handles the actual printing of progress bars
        for i, pbar in enumerate(pbars):
            # progressbar prints the bar each time update() is called
            pbar.update(pstatus[i])
    print end_msg


def mppb_example():
    """
    Example of mpprogressbar implementation.
    """

    # Configuration Options
    #======================
    # Update interval in seconds
    # Numbers below 1 may result in flickering
    pb_update_interval = 1
    # Message to be printed once all processes finish
    end_msg =  'all downloads complete'
    # Prefix for all process names. Be sure to include a trailing space for
    # legibility
    pname_prefix = "Process "
    # Header to be included above progress bars
    header = "Updating Database"
    # Number of processes
    nprocs = mp.cpu_count()


    # Dictionary to hold the current % of all processes,
    # indexed by pid
    pstatus = mp.Manager().dict()
    # Create list to hold all processes.
    procs = []
    # Create list to hold all progress bars.
    pbars = []

    # Create a progress bar for each process, then create and start a
    # the process itself
    for i in range(nprocs):
        # Maximum value of the progress bar. Defined within the loop because
        # this number should be equal to the operation count of the given
        # process, which may not be equal for all processes.
        pb_maxval = 40
        # Initialize status of the current process, pid=i, to 0%
        pstatus[i] = 0
        # Define progress bar in the same way you would with the regular
        # progressbar package
        pbars.append(pbfmp.ProgressBar(
            widgets=[
                (pname_prefix + str(i+1)), ' ',
                pbfmp.Percentage(), ' ',
                pbfmp.Bar('=', '[', ']'), ' ',
                pbfmp.ETA()],
                maxval=pb_maxval
            ).start())
        # Initialize the new process
        #   target: function to be run by the process
        #   args: list of arguments the function requires
        child = mp.Process(
            target=do_stuff,
            args=[header, pstatus, i, pb_maxval]
            )
        procs.append(child)
        child.start()

    # Prints progress bars while any one is still alive, then prints the end_msg
    print_progressbars(pstatus, procs, pbars, header, pb_update_interval, end_msg)

mppb_example()
