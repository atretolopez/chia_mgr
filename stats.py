import logging

import helpers
import os
import pandas
import datetime

def run(args):
    # check the directory exists
    if not os.path.isdir(args.dir):
        logging.error(f"Unable to find plot logs at {args.dir}")
        raise FileNotFoundError

    # get stats from
    stats = getStatistics(args.dir)

    # print them
    printStats(stats, args.out_dir)

def getStatistics(directory):
    '''

    :param directory:
    :return:
    '''
    stats_map = {"KSize": [],
                 "RAM": [],
                 "Threads": [],
                 "Start_time": [],
                 "Phase_1": [],
                 "Phase_2": [],
                 "Phase_3": [],
                 "Phase_4": [],
                 "Total_Plot_Time": [],
                 "Copy_Time": [],
                 }
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        _, file_extension = os.path.splitext(file)
        if (file_extension != ".log"):
            continue
        if os.path.isfile(file):
            log = open(file, "r")
            stat_map = {}
            for line in log:
                if "Starting phase 1/4" in line:
                    stat_map["Start_time"] = " ".join(line.split()[-4:])
                elif "Time for phase" in line:
                    phase = "Phase_" + line.split()[3]
                    time = line.split()[5]
                    stat_map[phase] = time
                elif "Total time" in line:
                    stat_map["Total_Plot_Time"] = line.split()[3]
                elif "Plot size" in line:
                    stat_map["KSize"] = line.split()[3]
                elif "Buffer size" in line:
                    stat_map["RAM"] = line.split()[3]
                elif "threads of stripe" in line:
                    stat_map["Threads"] = line.split()[1]
                elif "Copy time" in line:
                    stat_map["Copy_Time"] = line.split()[3]
            if len(stats_map) == len(stat_map):
                for key in stats_map:
                    stats_map[key].append(stat_map[key])
            else:
                logging.error(f"Incomplete log found: {filename}")



    return stats_map

def printStats(stats_map, out_path=None):
    df = pandas.DataFrame(data=stats_map)
    df.Phase_1 = pandas.to_datetime(df.Phase_1, unit='s').dt.strftime('%H:%M')
    df.Phase_2 = pandas.to_datetime(df.Phase_2, unit='s').dt.strftime('%H:%M')
    df.Phase_3 = pandas.to_datetime(df.Phase_3, unit='s').dt.strftime('%H:%M')
    df.Phase_4 = pandas.to_datetime(df.Phase_4, unit='s').dt.strftime('%H:%M')
    df.Total_Plot_Time = pandas.to_datetime(df.Total_Plot_Time, unit='s').dt.strftime('%H:%M')
    df.Copy_Time = pandas.to_datetime(df.Copy_Time, unit='s').dt.strftime('%H:%M')

    if (out_path != None):
        df.to_excel(out_path)

    print(df)