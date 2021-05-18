
import argparse
import logging
import os

# local
import helpers
import stats
import plots_mgr

# main global chia executable name
CHIA="chia"
def main(command_line=None):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    # adds statistics subparsers
    stats_subparser = subparsers.add_parser(name="stats")
    stats_subparser.add_argument("-s", "--show", action="store_true", help="Show statistics and exit")
    stats_subparser.add_argument("-d", "--dir", default=os.path.join(helpers.getUserNamePath(), '.chia', 'mainnet', 'plotter'), help="Log path")
    stats_subparser.add_argument("-o", "--out_dir", default=None, help="out_put dir path")

    # plot operations
    plot_subparser = subparsers.add_parser(name="plots")
    plot_subparser.add_argument("--disc_space", default=1024, type=int, help="Disc Space in GB")
    plot_subparser.add_argument("--cpu_threshold", default=50.0, type=float, help="CPU Threshold in percentage")
    plot_subparser.add_argument("--size", default=32, help="")
    plot_subparser.add_argument("--num", default=1, help="")
    plot_subparser.add_argument("--buffer", default=3389, help="")
    plot_subparser.add_argument("--num_threads", default=2, help="")
    plot_subparser.add_argument("--buckets", default=128, help="")
    plot_subparser.add_argument("--alt_fingerprint", default=None, help="")
    plot_subparser.add_argument("--farmer_public_key", default=None, help="")
    plot_subparser.add_argument("--pool_public_key", default=None, help="")
    plot_subparser.add_argument("--final_dir", required=True, help="Final directory for PLots results")
    plot_subparser.add_argument("--tmp_dir", default=os.path.join(helpers.getUserNamePath(), "tmp_plot_dir"), help="")
    plot_subparser.add_argument("--tmp2_dir", default=os.path.join(helpers.getUserNamePath(), "tmp2_plot_dir"), help="")


    args = parser.parse_args(command_line)

    try:
        logging.info("Starting CHIA mgr")
        if args.command == 'stats':
            stats.run(args)
        elif args.command == 'plots':
            plots_mgr.run(args)
    except:
        logging.error("CHIA Manager ending in a failure state")


# entry point
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
