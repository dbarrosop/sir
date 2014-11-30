from bgp_controller.prefix_table import PrefixTable

from datetime import datetime
import os.path
import argparse
import yaml
import json

from pydoc import locate


def configure_parser():
    parser = argparse.ArgumentParser(
        description="",
    )
    global_parser = argparse.ArgumentParser(add_help=False)
    global_parser.add_argument(
        '-c',
        default='etc/config.yaml',
        dest='config',
        help='Configuration file. Default is config.yaml'
    )

    subparsers = parser.add_subparsers()

    parser_simulate = subparsers.add_parser(
        'simulate',
        help='Connects to pmacct folder and runs a simulation',
        parents=[global_parser]
    )
    parser_simulate.set_defaults(action='simulate')

    parser_run = subparsers.add_parser(
        'run',
        help='Runs the controller',
        parents=[global_parser]
    )
    parser_run.set_defaults(action='run')

    args = parser.parse_args()
    return args


def load_bgp_file():
    files = os.listdir(conf['pmacct_bgp_folder'])
    files = [os.path.join(conf['pmacct_bgp_folder'], f) for f in files] # add path to each file

    bgp_table = dict()
    bgp_table['dump_init'] = list()
    bgp_table['dump'] = list()
    bgp_table['dump_close'] = list()

    with open(files[-1]) as data_file:
        for line in data_file.readlines():
            content = json.loads(line)
            bgp_table[content['event_type']].append(content)

    return bgp_table


def bgp_controller(filename, time, simulation=False, last_run=True):
    # Prefix table containing information regarding the previous run
    prev_pt = PrefixTable(
        max_routes = conf['max_routes'],
        max_age = 0,
        min_bytes = 0,
        packet_sampling=1
    )
    if os.path.exists(conf['latest_data_file']):
        prev_pt.load_from_csv(conf['latest_data_file'], conf['csv_delimiter'], read_ext_data=True)

    # Prefix table containing information about this run, unfiltered and unmodified
    raw_pt = PrefixTable(
        max_routes = 0,
        max_age = 0,
        min_bytes = 0,
        packet_sampling=conf['packet_sampling']
    )
    raw_pt.load_from_csv(filename, conf['csv_delimiter'], read_ext_data=False)

    # Prefix table containing information about this run
    new_pt = PrefixTable(
        max_routes = conf['max_routes'],
        max_age = conf['max_age'],
        min_bytes = conf['min_bytes'],
        packet_sampling=conf['packet_sampling']
    )
    new_pt.copy_prefixes(raw_pt)

    # We join the old prefix list with the new one and then we filter routes to get
    # only the routes we want
    new_pt.join_prefix_tables(prev_pt)

    new_pt.filter_routes()

    bgp_table = load_bgp_file()

    for plugin in conf['plugins']:
        plugin_class = locate('bgp_controller.plugins.%s' % plugin)
        plugin = plugin_class(
            conf = conf,
            data_file=filename,
            raw_pt = raw_pt,
            new_pt = new_pt,
            prev_pt = prev_pt,
            bgp_table = bgp_table,
            time = time,
            simulation = simulation,
            last_run = last_run
        )
        plugin._execute()


def run_simulation(folder):
    files = os.listdir(folder)
    files = [os.path.join(folder, f) for f in files] # add path to each file

    total_runs = len(files)
    count = 0

    last_run = False

    for f in files:
        time = "-".join(f.split('.')[0].split('-')[1:])
        if count + 1 == total_runs:
            last_run = True
        bgp_controller(f, time, simulation=True, last_run=last_run)
        count += 1


if __name__ == '__main__':
    args = configure_parser()

    content = open(args.config, 'r')
    conf = yaml.load(content)

    if args.action == 'simulate':
        simulation = True
        run_simulation(conf['pmacct_data_folder'])
    elif args.action == 'run':
        simulation = False
        time = datetime.now().strftime('%Y%m%d-%H%M')
        bgp_controller(conf['pmacct_data_file'], time)
