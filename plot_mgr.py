
class PlotInfo:
    def __init__(self, path):
        self.path = path

    def getPlotPath(self):
        return self.path

def getConfigPlots(chia_net_path):
    '''

    :param chia_root:
    :return: list of all the current config plots in
    '''