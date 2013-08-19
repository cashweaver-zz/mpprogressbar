import mpprogressbar, random, time
import multiprocessing as mp

def download(status, pname, *fargs):
    count = random.randint(5, fargs[0][1])
    for i in range(count):
        status.put([pname, (i+1.0)/count])
        time.sleep(0.1)

def main():
    mppb = mpprogressbar.MPProgressbar()
    for i in range(mp.cpu_count()):
        mppb.append("Process %d" % (i+1))
    mppb.start(
        "Updating database",
        "All downloads finished!",
        0.1,
        download,
        10,
        100,
        1000
        )

main()
