import glob
from datetime import datetime
import json


class FSHelper:
    def __init__(self, base_path='./data'):
        self.base_path = base_path
        files = [f.split('/')[-1] for f in glob.glob('{}/bgp-*'.format(self.base_path))]
        self.neighbors = set([n.split('-')[1].replace('_', '.') for n in files])
        dates = sorted(set([n.split('-')[2].replace('.txt', '') for n in files]))
        self.dates = [datetime.strptime(d, '%Y_%m_%dT%H_%M_%S') for d in dates]

    def get_bgp_prefixes(self, date):
        date = date.replace('-', '_').replace(':', '_')

        prefixes = dict()

        for n in self.neighbors:
            prefixes[n] = dict()
            f = 'bgp-{}-{}'.format(n, date).replace('.', '_')

            with open('{}/{}.txt'.format(self.base_path, f)) as data_file:
                for line in data_file.readlines():
                    data = json.loads(line)

                    if data['event_type'] == 'dump':
                        prefixes[n][data['ip_prefix']] = data

        return prefixes
