import mpprogressbar
import multiprocessing as mp

def main():
    mppb = mpprogressbar.mpprogressbar()
    for i in range(mp.cpu_count()):
        mppb.append("Process %d" % (i+1))
    mppb.start("Updating database", "All downloads finished!", 0.1)

main()
