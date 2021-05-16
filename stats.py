
import helpers
import os
import pandas
import datetime

def runStatsFromUser():
    '''

    :return:
    '''
    # get user path
    user_path = helpers.getUserNamePath()

    # get plotter path
    plotter_path = os.path.join(user_path, '.chia', 'mainnet', 'plotter')

    # check the directory exists
    if not os.path.isdir(plotter_path):
        raise FileNotFoundError

    # get stats from
    stats = getStatistics(plotter_path)

    # print them
    printStats(stats)

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
        if os.path.isfile(file):

            stats_map["Start_time"].append(datetime.datetime.fromtimestamp(os.path.getctime(file)).strftime('%H:%M:%S'))
            log = open(file, "r")
            for line in log:
                if "Time for phase" in line:
                    phase = "Phase_" + line.split()[3]
                    time = line.split()[5]
                    stats_map[phase].append(time)
                elif "Total time" in line:
                    stats_map["Total_Plot_Time"].append(line.split()[3])
                elif "Plot size" in line:
                    stats_map["KSize"].append(line.split()[3])
                elif "Buffer size" in line:
                    stats_map["RAM"].append(line.split()[3])
                elif "threads of stripe" in line:
                    stats_map["Threads"].append(line.split()[1])
                elif "Copy time" in line:
                    stats_map["Copy_Time"].append(line.split()[3])


    return stats_map

def printStats(stats_map):
    df = pandas.DataFrame(data=stats_map)
    df.Phase_1 = pandas.to_datetime(df.Phase_1, unit='s').dt.strftime('%H:%M')
    df.Phase_2 = pandas.to_datetime(df.Phase_2, unit='s').dt.strftime('%H:%M')
    df.Phase_3 = pandas.to_datetime(df.Phase_3, unit='s').dt.strftime('%H:%M')
    df.Phase_4 = pandas.to_datetime(df.Phase_4, unit='s').dt.strftime('%H:%M')
    print(df)