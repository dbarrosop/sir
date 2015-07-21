import sqlite3 as lite
import os
from datetime import datetime


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SQLite3Helper:

    def __init__(self, database):
        if not os.path.isfile(database):
            raise Exception("Database file doesn't exist: %s" % database)

        self.database = database
        self.conn = None

    def connect(self):
        self.conn = lite.connect(database=self.database)
        self.conn.row_factory = dict_factory

    def close(self):
        if self.conn is not None:
            self.conn.close()

    def _execute_query(self, query, args=(), commit=False):
        try:
            cur = self.conn.cursor()
            cur.execute(query, args)

            if commit:
                result = self.conn.commit()
            else:
                result = cur.fetchall()
        except lite.OperationalError:
            raise Exception('The following query failed:\n%s' % query)
        return result

    def aggregate_per_prefix(self, start_time, end_time, limit=0, net_masks='', exclude_net_masks=False):
        """ Given a time range aggregates bytes per prefix.

            Args:
                start_time: A string representing the starting time of the time range
                end_time: A string representing the ending time of the time range
                limit: An optional integer. If it's >0 it will limit the amount of prefixes returned.

            Returns:
                A list of prefixes sorted by sum_bytes. For example:

                [
                        {'key': '192.168.1.0/25', 'sum_bytes': 3000, 'as_dst': 345},
                        {'key': '192.213.1.0/25', 'sum_bytes': 2000, 'as_dst': 123},
                        {'key': '231.168.1.0/25', 'sum_bytes': 1000, 'as_dst': 321},
                ]
        """
        if net_masks == '':
            net_mask_filter = ''
        elif not exclude_net_masks:
            net_mask_filter = 'AND mask_dst IN ({})'.format(net_masks)
        elif exclude_net_masks:
            net_mask_filter = 'AND mask_dst NOT IN ({})'.format(net_masks)

        query = ''' SELECT ip_dst||'/'||mask_dst as key, SUM(bytes) as sum_bytes, as_dst
                    from acct
                    WHERE
                    datetime(stamp_updated) BETWEEN datetime(?) AND datetime(?)
                    {}
                    GROUP by ip_dst,mask_dst
                    ORDER BY SUM(bytes) DESC
                '''.format(net_mask_filter)

        if limit > 0:
            query += 'LIMIT %d' % limit

        return self._execute_query(query, [start_time, end_time])

    def aggregate_per_as(self, start_time, end_time):
        """ Given a time range aggregates bytes per ASNs.

            Args:
                start_time: A string representing the starting time of the time range
                end_time: A string representing the ending time of the time range

            Returns:
                A list of prefixes sorted by sum_bytes. For example:

                [
                        {'key': '6500', 'sum_bytes': 3000},
                        {'key': '2310', 'sum_bytes': 2000},
                        {'key': '8182', 'sum_bytes': 1000},
                ]
        """

        query = ''' SELECT as_dst as key, SUM(bytes) as sum_bytes
                    from acct
                    WHERE
                    datetime(stamp_updated) BETWEEN datetime(?) AND datetime(?)
                    GROUP by as_dst
                    ORDER BY SUM(bytes) DESC;
                '''

        return self._execute_query(query, [start_time, end_time])

    def get_dates(self):
        query = '''SELECT DISTINCT stamp_updated from acct ORDER BY stamp_updated ASC;'''
        return [datetime.strptime(d['stamp_updated'], '%Y-%m-%d %H:%M:%S') for d in self._execute_query(query)]

    def get_dates_in_range(self, start_time, end_time):
        query = ''' SELECT DISTINCT stamp_updated
                    from acct
                    WHERE datetime(stamp_updated) BETWEEN datetime(?) AND datetime(?);
                '''

        return [datetime.strptime(d['stamp_updated'], '%Y-%m-%d %H:%M:%S')
                for d in self._execute_query(query, [start_time, end_time])]

    def get_total_traffic(self, start_time, end_time):
        query = ''' SELECT SUM(bytes) as sum_bytes
                    FROM acct
                    WHERE
                    datetime(stamp_updated) BETWEEN datetime(?) AND datetime(?);
                '''

        return self._execute_query(query, [start_time, end_time])[0]['sum_bytes']

    def offloaded_bytes(self, num_prefixes, start_time, end_time):
        query = ''' SELECT SUM(bytes) as sum_bytes FROM (
                        SELECT ip_dst, mask_dst, SUM(bytes) AS bytes
                        from acct
                        WHERE
                        datetime(stamp_updated) BETWEEN datetime(:start_time) AND datetime(:end_time)
                        GROUP BY ip_dst, mask_dst
                        ORDER BY SUM(bytes) DESC
                        LIMIT %d
                    );
                ''' % num_prefixes
        args = {'start_time': start_time, 'end_time': end_time, 'num_prefixes': num_prefixes,}
        return self._execute_query(query, args)[0]['sum_bytes']

    def timeseries_per_as(self, start_time, end_time, asn):
        query = ''' SELECT SUM(bytes) as sum_bytes
                    from acct
                    WHERE
                    datetime(stamp_updated) BETWEEN datetime(?) AND datetime(?)
                    AND
                    as_dst = ?
                    GROUP by as_dst, stamp_updated
                    ORDER BY stamp_updated ASC;
                '''

        return [r['sum_bytes'] for r in self._execute_query(query, [start_time, end_time, asn])]

    def timeseries_per_prefix(self, start_time, end_time, prefix):
        ip_dst, mask_dst = prefix.split('/')
        query = ''' SELECT SUM(bytes) as sum_bytes
                    from acct
                    WHERE
                    datetime(stamp_updated) BETWEEN datetime(?) AND datetime(?)
                    AND
                    ip_dst = ? AND mask_dst = ?
                    GROUP by ip_dst, mask_dst, stamp_updated
                    ORDER BY stamp_updated ASC;
                '''

        return [r['sum_bytes'] for r in self._execute_query(query, [start_time, end_time, ip_dst, mask_dst])]

    def put_variables(self, name, content, category, extra_vars):
        query = ''' INSERT INTO variables VALUES (?, ?, ?, ?); '''
        self._execute_query(query, [name, content, category, str(extra_vars)], commit=True)

    def get_variables(self):
        query = ''' SELECT * FROM variables '''
        return self._execute_query(query)

    def get_variable(self, category, name):
        query = ''' SELECT * FROM variables WHERE category = ? AND name = ?; '''
        return self._execute_query(query, [category, name])

    def update_variable(self, old_name, old_category, name, content, category, extra_vars):
        query = ''' UPDATE variables
                    SET name = ?, content = ?, category = ?, extra_vars = ?
                    WHERE name = ? AND category = ?;
                '''
        self._execute_query(query, [name, content, category, str(extra_vars), old_name, old_category], commit=True)

    def delete_variable(self, category, name):
        query = ''' DELETE FROM variables WHERE name = ? AND category = ?;
                '''
        self._execute_query(query, [name, category], commit=True)

    def get_categories(self):
        query = ''' SELECT DISTINCT category FROM variables'''
        return [c['category'] for c in self._execute_query(query, [])]

    def filter_variables_category(self, category):
        query = ''' SELECT * FROM variables WHERE category = ?; '''
        return self._execute_query(query, [category])

    def get_flows(self, start_time, end_time):
        query = ''' SELECT ip_dst, mask_dst, bytes, packets, as_dst, stamp_updated
                            FROM acct
                            WHERE
                            datetime(stamp_updated) BETWEEN datetime(?) AND datetime(?);
                '''
        return self._execute_query(query, [start_time, end_time])
