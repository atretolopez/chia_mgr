
import datetime
import logging
import os
import subprocess
import time
import psutil

# local
import helpers

# CHIA
CHIA = 'chia'

# stop request
stop_request = False

# global list with all processes running
procs = []

def cpuThreshold(cpu_percentage: float):
    cpu_use = psutil.cpu_percent(10.0)
    logging.info(f"CPU threshold set to {cpu_percentage}, usage at {cpu_use}. Build another plot: {cpu_use <= cpu_percentage}")
    return cpu_use <= cpu_percentage

def discSpaceAvailable(disc_space: int, running_plots: int):
    logging.info(f"Disc space set to {disc_space}, using {running_plots * 300}. Build another plot: {disc_space - 300 >= (running_plots * 300)}")
    return disc_space - 250 >= (running_plots * 250)

def run(args):
    try:
        os.remove(args.tmp_dir)
        os.remove(args.tmp2_dir)
    except OSError as e:
        logging.warning(f"Error: {e.strerror}")

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
            procs.append(createPlot(
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

# for output
dev_null = open(os.devnull, 'w')

def createPlot(final_dir,
               size=32,
               num=1,
               buffer=3389,
               num_threads=2,
               buckets=128,
               alt_fingerprint=None,
               farmer_public_key=None,
               pool_public_key=None,
               tmp_dir=os.path.join(helpers.getUserNamePath(), "tmp_plot_dir"),
               tmp2_dir=os.path.join(helpers.getUserNamePath(), "tmp2_plot_dir")):
        '''

        :param final_dir:
        :param size:
        :param override_k:
        :param num:
        :param buffer:
        :param num_threads:
        :param buckets:
        :param alt_fingerprint:
        :param farmer_public_key:
        :param pool_public_key:
        :param tmp_dir:
        :param tmp2_dir:
        :return:
        '''

        ## make the basic command
        cmd = ['chia', 'plots', 'create', '--final_dir', final_dir, '--tmp_dir', tmp_dir, '--tmp2_dir', tmp2_dir]

        if size != 32:
            cmd.extend(['--size', size])
        if num != 1:
            cmd.extend(['--num', num])
        if buffer != 3389:
            cmd.extend(['--buffer', buffer])
        if num_threads != 2:
            cmd.extend(['--num_threads', num_threads])
        if buckets != 128:
            cmd.extend(['--buckets', buckets])
        if alt_fingerprint != None:
            cmd.extend(['--alt_fingerprint', alt_fingerprint])
        if farmer_public_key != None:
            cmd.extend(['--farmer_public_key', farmer_public_key])
        if pool_public_key != None:
            cmd.extend(['--pool_public_key', pool_public_key])

        return subprocess.Popen(cmd)
