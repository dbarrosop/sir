from base import Backend
import sqlite3 as lite
from bgp_controller.prefix_table import Prefix, PrefixTable

import os

class SQLite(Backend):

    def open(self):
        if not os.path.isfile(self.conf['sqlite_file']):
            raise Exception("Database file doesn't exist: %s"% self.conf['sqlite_file'])

        self.con = lite.connect(self.conf['sqlite_file'])

    def close(self):
        self.con.close()

    def _execute_query(self, query):
        try:
            cur = self.con.cursor()
            cur.execute(query)
            result = cur.fetchall()
        except lite.OperationalError:
            raise Exception('The following query failed:\n%s' % query)

        return result

    def _get_pt(self, list, sampling=1):
        pt = PrefixTable()

        for p in list:
            prefix = Prefix(p[0], p[1], p[2], p[3], p[4], sampling)
            pt.add(prefix)

        return pt

    def get_best_prefixes(self, start_time, end_time):
        query = ("""
                         SELECT ip_dst, mask_dst, AVG(bytes), AVG(packets), stamp_updated
                         FROM acct
                         WHERE datetime(stamp_updated) BETWEEN datetime('%s') AND datetime('%s')
                         GROUP BY ip_dst, mask_dst ORDER BY AVG(bytes) DESC
                         LIMIT %s;
                """) % (start_time, end_time, self.conf['max_routes'])
        return self._get_pt(self._execute_query(query), self.conf['packet_sampling'])

    def get_raw_prefixes(self, start_time, end_time):
        query = ("""
                         SELECT ip_dst, mask_dst, bytes, packets, stamp_updated
                         FROM acct
                         WHERE
                         datetime(stamp_updated) BETWEEN datetime('%s') AND datetime('%s')
                         AND
                         stamp_updated = (
                              SELECT MAX(stamp_updated) FROM acct
                              WHERE datetime(stamp_updated) BETWEEN datetime('%s') AND datetime('%s')
                         );
                """) % (start_time, end_time, start_time, end_time)
        return self._get_pt(self._execute_query(query), self.conf['packet_sampling'])

    def get_previous_prefixes(self, start_time, end_time):
        query = ("""
                         SELECT ip_dst, mask_dst, bytes, packets, stamp_updated
                         FROM best_prefixes
                         WHERE
                         datetime(stamp_updated) BETWEEN datetime('%s') AND datetime('%s')
                         AND
                         stamp_updated = (SELECT MAX(stamp_updated) FROM best_prefixes);
                """) % (start_time, end_time)

        return self._get_pt(self._execute_query(query))

    def save_prefix_table(self, prefix_table, date):
        cur = self.con.cursor()

        for prefix in prefix_table:
            values = (
                str(prefix.get_prefix_network()),
                prefix.get_prefix_mask(),
                prefix.get_packets(),
                prefix.get_bytes(),
                date.strftime('%Y-%m-%d %H:%M:%S')
            )
            cur.execute("INSERT INTO best_prefixes VALUES %s;" % (str(values)))

        self.con.commit()

    def save_dict(self, data_dict, db_table):
        columns = tuple(data_dict.keys())
        values = tuple(data_dict.values())

        cur = self.con.cursor()
        cur.execute("INSERT INTO %s %s VALUES %s;" % (db_table, str(columns), str(values)))
        self.con.commit()

    def get_data_from_table(self, table, filter=None):
        if filter is None:
            query = ("SELECT * FROM %s;") % table
        else:
            query = ("SELECT * FROM %s WHERE %s;") % (table, filter)
        return self._execute_query(query)

    def get_available_dates_in_range(self, start_time, end_time):
        query = ("""
                    SELECT stamp_updated FROM acct WHERE datetime(stamp_updated)
                    BETWEEN datetime('%s') AND datetime('%s')
                    GROUP BY stamp_updated;
                """) % (start_time, end_time)
        return self._execute_query(query)