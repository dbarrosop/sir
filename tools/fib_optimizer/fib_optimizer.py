#!/usr/bin/env python

# TODO check range is ok

from pySIR.pySIR import pySIR

import sys
import json
import random


def _split_tables(s):
    lem = set()
    lpm = set()

    for p in s:
        if p.split('/')[1] == '24':
            lem.add(p)
        else:
            lpm.add(p)
    return lem, lpm


def get_variables():
    v = sir.get_variables_by_category_and_name('apps', 'fib_optimizer').result[0]
    return json.loads(v['content'])


def get_date_range():
    # These are dates for which we have flows. We want to "calculate" the range we want to use
    # to calculate the topN prefixes
    dates = sir.get_available_dates().result

    if len(dates) < conf['age']:
        sd = dates[0]
    else:
        sd = dates[-conf['age']]
    ed = dates[-1]
    return sd, ed


def inc_exc_prefixes():

    i_lem, i_lpm = _split_tables(conf['include_prefixes'])
    e_lem, e_lpm = _split_tables(conf['exclude_prefixes'])

    return i_lem, i_lpm, e_lem, e_lpm


def get_top_prefixes():
    limit_lem = int(conf['max_lem_prefixes']) - len(inc_lem) + len(exc_lem)
    lem = set([p['key'] for p in sir.get_top_prefixes(
            start_time=start_time,
            end_time=end_time,
            limit_prefixes=limit_lem,
            net_masks=conf['lem_prefixes'],
        ).result]) - exc_lem | inc_lem
    limit_lpm = int(conf['max_lpm_prefixes']) - len(inc_lpm) + len(exc_lpm)
    lpm = set([p['key'] for p in sir.get_top_prefixes(
            start_time=start_time,
            end_time=end_time,
            limit_prefixes=limit_lpm,
            net_masks=conf['lem_prefixes'],
            exclude_net_masks=1,
        ).result]) - exc_lpm | inc_lpm
    return lem, lpm


def get_bgp_prefix_lists():
    bgp_p = sir.get_bgp_prefixes(date=end_time).result
    p = set()

    for p_data in bgp_p.values():
        p = p | set(p_data.keys())

    return _split_tables(p)


def complete_prefix_list():
    def _complete_pl(pl, bgp_pl, num):
        if len(pl) < num:
            num = num - len(pl)
            bgp_pl = bgp_pl - pl
            return pl | set(random.sample(bgp_pl, num))
        else:
            return pl

    lem_pl = _complete_pl(lem_prefixes, bgp_lem, conf['max_lem_prefixes'])
    lpm_pl = _complete_pl(lpm_prefixes, bgp_lpm, conf['max_lpm_prefixes'])
    return lem_pl, lpm_pl


def build_prefix_lists():
    def _build_pl(name, prefixes):
        pl = 'ip prefix-list {}\n'.format(name)

        i = 1
        for p in prefixes:
            pl += '   seq {} permit {}\n'.format(i, p)
            i += 1

        with open('{}/{}'.format(conf['path'], name), "w") as f:
            f.write(pl)

    _build_pl('fib_optimizer_lpm', lpm_prefixes)

    lem_p = list(lem_prefixes)

    i = 1
    while 50000*i <= len(lem_prefixes):
        num = min(50000*i, len(lem_p))
        _build_pl('fib_optimizer_lem_{}'.format(i), lem_p[50000*(i-1):num])
        i += 1



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'You have to specify the base URL. For example: {} http://127.0.0.1:5000/api/v1.0'.format(sys.argv[0])
        sys.exit(0)
    elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print 'You have to specify the base URL. For example: {} http://127.0.0.1:5000/api/v1.0'.format(sys.argv[0])
        sys.exit(1)

    sir = pySIR(sys.argv[1])

    # We get the configuration for our application
    conf = get_variables()

    # The time range we want to process
    start_time, end_time = get_date_range()

    # We get the full BGP table availabe
    bgp_lem, bgp_lpm = get_bgp_prefix_lists()

    # "static" data
    inc_lem, inc_lpm, exc_lem, exc_lpm = inc_exc_prefixes()

    # We get the Top prefixes. Included and excluded prefixes are merged as well
    lem_prefixes, lpm_prefixes = get_top_prefixes()

    # If we have space left in the LEM/LPM we add some BGP prefixes
    lem_prefixes, lpm_prefixes = complete_prefix_list()

    # We build the files with the prefix lists
    build_prefix_lists()
