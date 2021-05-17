
import os
import subprocess

# for output
dev_null = open(os.devnull, 'w')

# local
import helpers

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

        return subprocess.Popen(cmd, stdout=dev_null)
