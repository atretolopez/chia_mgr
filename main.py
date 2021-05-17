
import argparse
import datetime
import logging
import os
import sys
import time
import psutil

# local
import helpers
import plots_mgr
import stats

# stop request
stop_request = False

# global list with all processes running
procs = []

def cpuThreshold(cpu_percentage: float):
    cpu_use = psutil.cpu_percent(10.0)
    logging.info(f"CPU threshold set to {cpu_percentage}, usage at {cpu_use}. Run another plot: {cpu_use <= cpu_percentage}")
    return cpu_use <= cpu_percentage

def discSpaceAvailable(disc_space: int, running_plots: int):
    logging.info(f"Disc space set to {disc_space}, using {running_plots * 300}. Run another plot: {disc_space - 300 >= (running_plots * 300)}")
    return disc_space - 300 >= (running_plots * 300)

def Run(args):
    while (not stop_request):
        # check how many plots are running
        plots_running = 0
        for proc in procs:
            if proc.poll() is None:
                plots_running += 1

        # Determine if a new Plot should be created
        cpu = cpuThreshold(args.cpu_threshold)
        space = discSpaceAvailable(args.disc_space, plots_running)

        if (cpu and space):
            procs.append(plots_mgr.createPlot(
                        args.final_dir,
                        args.size,
                        args.num,
                        args.buffer,
                        args.num_threads,
                        args.buckets,
                        args.alt_fingerprint,
                        args.farmer_public_key,
                        args.pool_public_key,
                        args.tmp_dir,
                        args.tmp2_dir))
            logging.info("--------------------------------------------------------------")
            logging.info(f"Creating a new Plot: {datetime.datetime.now()}")
            logging.info("--------------------------------------------------------------")

        # sleep 30 sec
        time.sleep(30)


# main global chia executable name
CHIA="chia"
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--stats", action="store_true", help="Show statistics and exit")
    parser.add_argument("-p", "--plot", action="store_true", help="Plot options")
    parser.add_argument("--disc_space", default=1024, type=int, help="Disc Space in GB")
    parser.add_argument("--cpu_threshold", default=50.0, type=float, help="CPU Threshold in percentage")
    parser.add_argument("--size", default=32, help="")
    parser.add_argument("--num", default=1, help="")
    parser.add_argument("--buffer", default=3389, help="")
    parser.add_argument("--num_threads", default=2, help="")
    parser.add_argument("--buckets", default=128, help="")
    parser.add_argument("--alt_fingerprint", default=None, help="")
    parser.add_argument("--farmer_public_key", default=None, help="")
    parser.add_argument("--pool_public_key", default=None, help="")
    parser.add_argument("--final_dir", required=True, help="Final directory for PLots results")
    parser.add_argument("--tmp_dir", default=os.path.join(helpers.getUserNamePath(), "tmp_plot_dir"), help="")
    parser.add_argument("--tmp2_dir", default=os.path.join(helpers.getUserNamePath(), "tmp2_plot_dir"), help="")

    args = parser.parse_args()
    if args.stats:
        stats.runStatsFromUser()
        sys.exit()

    if args.plot:
        if not helpers.is_tool(CHIA):
            logging.error("Unable to find CHIA executable entry point.")
            sys.exit(-1)

        try:
            os.remove(args.tmp_dir)
            os.remove(args.tmp2_dir)
        except OSError as e:
            logging.error(f"Error: {e.strerror}")

        # Run
        logging.info(f"Starting CHIA mgr")
        Run(args)


# entry point
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
