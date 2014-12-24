from bgp_controller.bgpc import BGPController

import argparse
import yaml
import sys

import logging
logger = logging.getLogger('sir')


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

def configure_logging(config):
    formatter = logging.Formatter('program=sir severity_label=%(levelname)s severity=%(levelno)s %(message)s')
    logger.setLevel(config['logging_level'])

    if config['log_to_stderr']:
        logging.basicConfig(level=config['logging_level'], stream=sys.stderr)
    if config['log_to_syslog']:
        handler = logging.handlers.SysLogHandler(('127.0.0.1', config['syslog_server_port']))
        handler.setFormatter(formatter)
        logger.addHandler(handler)


def cli():
    args = configure_parser()

    content = open(args.config, 'r')
    config = yaml.load(content)

    configure_logging(config)

    bgp_controller = BGPController(config)

    if args.action == 'simulate':
        bgp_controller.simulate()
    elif args.action == 'run':
        bgp_controller.run()

if __name__ == "__main__":
    cli()