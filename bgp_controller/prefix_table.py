class Prefix:
    def __init__(self, prefix, mask, packets, bytes, date, sampling=1):
        self.prefix = prefix
        self.mask = mask
        self.packets = int(packets*sampling)
        self.bytes = int(bytes*sampling)
        self.date = date

    def __eq__(self, other):
        return self.prefix == other.prefix and self.mask == other.mask

    def __str__(self):
        return '%s/%s, packets: %s, bytes: %s, date: %s' %\
               (self.prefix, self.mask, self.packets, self.bytes, self.date)

    def __hash__(self):
        return hash(self.prefix) ^ hash(self.mask)

    def get_prefix(self):
        return '%s/%s' % (self.prefix, self.mask)

    def get_prefix_network(self):
        return self.prefix

    def get_prefix_mask(self):
        return self.mask

    def get_bytes(self):
        return self.bytes

    def get_packets(self):
        return self.packets


class PrefixTable:
    def __init__(self, packet_sampling=1):
        self.packet_sampling = packet_sampling
        self.prefix_set = set()
        self.prefixes = dict()
        self.expired_prefixes = 0

    def __len__(self):
        return len(self.prefix_set)

    def __iter__(self):
        for p in self.prefixes.items():
            yield(p[1])

    def get(self, prefix):
        return self.prefixes[prefix]

    def remove(self, prefix):
        self.prefix_set.remove(prefix.get_prefix())
        del(self.prefixes[prefix.get_prefix()])

    def add(self, prefix):
        self.prefix_set.add(prefix.get_prefix())
        self.prefixes[prefix.get_prefix()] = prefix

    def common_prefixes(self, pt):
        """
        Args:
            * pt: A PrefixTable object
        Returns:
            A set containing all prefixes present both in the current PrefixTable and in pt
        """
        return self.prefix_set & pt.prefix_set

    def missing_prefixes(self, pt):
        """
        Args:
            * pt: A PrefixTable object
        Returns:
            A set containing all prefixes present in the current object but not in pt
        """
        return self.prefix_set - pt.prefix_set

    def get_total_bytes(self):
        return sum(p.get_bytes() for p in self.prefixes.values())

    def prefix_present(self, prefix):
        return prefix.get_prefix() in self.prefix_set

    def get_prefixes(self):
        return self.prefixes.values()

    '''
    def replace_prefix_table(self, dictionary):
        self.prefixes = dict(dictionary)
        self.prefix_set = set(self.prefixes.keys())

    def iteritems(self):
        for key, value in self.prefixes.iteritems():
            yield key, value

    def copy_prefixes(self, pt):
        self.prefixes = dict(pt.prefixes)
        self.prefix_set = set(pt.prefix_set)

    def set_max_routes(self, max_routes):
        self.max_routes = max_routes

    def get_max_routes(self):
        return self.max_routes

    def set_max_age(self, max_age):
        self.max_age = max_age

    def get_max_age(self):
        return self.max_age

    def set_min_bytes(self, min_bytes):
        self.min_bytes = min_bytes

    def get_min_bytes(self):
        return self.min_bytes

    def set_packet_sampling(self, packet_sampling):
        self.packet_sampling = packet_sampling

    def get_packet_sampling(self):
        return self.packet_sampling

    def get_total_bytes(self):
        return sum(p.get_bytes() for p in self.prefixes.values())

    def load_from_csv(self, file_name, csv_delimiter, read_ext_data=False):
        with open(file_name, "rb") as f:
            reader = csv.DictReader(f, delimiter=csv_delimiter)

            for p in reader:
                packets = int(p['PACKETS']) * self.packet_sampling
                bytes = int(p['BYTES']) * self.packet_sampling

                prefix = Prefix(p['DST_IP'], p['DST_MASK'], packets, bytes)

                if read_ext_data:
                    prefix.set_age(int(p['AGE']))
                    prefix.set_avg_bytes(int(p['AVG_BYTES']))
                    prefix.set_avg_packets(int(p['AVG_PACKETS']))

                if prefix.get_bytes() > self.min_bytes:
                    # FIXME This is due to pmacct duplicates prefixes. Inefficient as hell so we should fix it
                    if self.prefix_present(prefix):
                        self.get(prefix.get_prefix()).average(prefix)
                    else:
                        self.add(prefix)

    def join_prefix_tables(self, pt):
        continuing_prefixes = self.common_prefixes(pt)
        old_prefixes = pt.missing_prefixes(self)

        # We "average" bytes and packets and reset the age on continuing routes
        for p in continuing_prefixes:
            self.get(p).reset_age()
            self.get(p).average(pt.get(p))

        # We increment age on the old routes
        for p in old_prefixes:
            self.add(pt.get(p))
            self.get(p).increment_age()

    def filter_routes(self):
        if self.max_routes == 0 or len(self) < self.max_routes:
            pass
        else:
            num_prefixes = len(self)
            if self.get_max_age() > 0:
                prefixes = set(v for k, v in self.iteritems() if v.get_age() <= self.get_max_age())
            else:
                prefixes = set(v for k, v in self.iteritems())

            self.expired_prefixes = num_prefixes - len(prefixes)
            prefixes = sorted(prefixes, key=lambda x: x.bytes, reverse=True)[:self.get_max_routes()]
            self.replace_prefix_table({x.get_prefix(): x for x in prefixes})
    '''