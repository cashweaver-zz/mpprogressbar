import random, time, pbfmp, sys
import multiprocessing as mp

def do_stuff(sub_nums, header, pstatus, pid, pb_maxval):
    """
    Pretends to do work so we can see mpprogressbar in action.
    """
    for i in range(pb_maxval):
        ##########
        # Do stuff

        for n in sub_nums:
            # Numbercrunching simulated by time.sleep()
            time.sleep(random.uniform(0.1, 0.01))

        # Done doing things
        ###################
        # update progress bar for this process
        pstatus[pid] += 1
        # update the global progress bar
        pstatus[0] += 1

def print_progressbars(pstatus, procs, pbars, header, pb_update_interval, end_msg):
    """
    Print all progress bars while any one is still running. Then print the
    end_msg
    """
    # Immediately clear the screen and print our header.
    # Without this, if the pb_update_interval is relatively long, the script
    # will appear to 'hang', even though it is running properly.
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
    This example will use mpprogressbars to show the progress of nproc
    processes as they iterate over their sub-section of nums, a list of dummy
    data
    """

    # Configuration Options
    #======================
    # Update interval in seconds
    # Numbers below 1 may result in flickering
    pb_update_interval = 1
    # Message to be printed once all processes finish
    end_msg =  'All processes complete!\n'
    # Prefix for all process names. Be sure to include a trailing space for
    # legibility
    pname_prefix = "Process "
    # Header to be included above progress bars
    header = "Running processes"
    # Number of processes
    nprocs = mp.cpu_count()



    # Create dummy list and data
    #===========================
    nums = []
    nums.extend(range(1,49))
    # Split nums, as equally as can be done, into a list of lists: sub_nums
    sub_nums = [nums[i*len(nums)//nprocs:(i+1)*len(nums)//nprocs] for i in range(nprocs)]



    # Create overseer lists and dicts
    #================================
    # Dictionary to hold the current % of all processes,
    # indexed by pid
    pstatus = mp.Manager().dict()
    # Create list to hold all processes.
    procs = []
    # Create list to hold all progress bars.
    pbars = []



    # Create the global progress bar
    #===============================
    # Define progress bar in the same way you would with the regular
    # progressbar package.
    #   NOTE: maxval must equal the sum of maxvals for all processes
    pbars.append(pbfmp.ProgressBar(
        widgets=[
            'All Procs', ' ',
            pbfmp.Percentage(), ' ',
            pbfmp.Bar('#', '[', ']'), ' ',
            pbfmp.ETA()],
            maxval=len(nums)
        ).start())

    # Initialize status of the global process to 0%
    pstatus[0] = 0



    # Create a progress bar for each process
    #=======================================
    for i in range(nprocs):
        # Maximum value of the progress bar. Defined within the loop because
        # this number should be equal to the operation count of the given
        # process, which may not be equal for all processes.
        pb_maxval = len(sub_nums[i])

        # Initialize status of the current process to 0%
        # pid = i+1 because 0 is reserved for the global progress bar
        pstatus[i+1] = 0

        # Define progress bar in the same way you would with the regular
        # progressbar package
        pbars.append(pbfmp.ProgressBar(
            widgets=[
                (pname_prefix + str(i+1)), ' ',
                pbfmp.Percentage(), ' ',
                pbfmp.Bar('-', '[', ']'), ' ',
                pbfmp.ETA()],
                maxval=pb_maxval
            ).start())

        # Initialize the new process
        #   target: function to be run by the process
        #   args: list of arguments the function requires
        child = mp.Process(
            target=do_stuff,
            args=[sub_nums[i], header, pstatus, (i+1), pb_maxval]
            )

        # Add child to procs so we can keep track of it
        procs.append(child)

        # Start the process
        child.start()

    # Prints progress bars while any one is still alive, then prints the end_msg
    print_progressbars(pstatus, procs, pbars, header, pb_update_interval, end_msg)

mppb_example()
