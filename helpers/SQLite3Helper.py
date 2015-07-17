import sqlite3 as lite
import os
from datetime import datetime

class SQLite3Helper:
    def __init__(self, database):
        if not os.path.isfile(database):
            raise Exception("Database file doesn't exist: %s" % database)

        self.database=database
        self.conn = None

    def connect(self):
        self.conn = lite.connect(database=self.database)
        self.conn.row_factory = lite.Row

    def close(self):
        if self.conn is not None:
            self.conn.close()

    def _execute_query(self, query, args=()):
        try:
            self.conn.row_factory = lite.Row
            cur = self.conn.cursor()
            cur.execute(query, args)
            result = cur.fetchall()
        except lite.OperationalError:
            raise Exception('The following query failed:\n%s' % query)
        return result

    def get_dates(self):
        query = '''SELECT DISTINCT stamp_updated from acct;'''
        return [datetime.strptime(d[0], '%Y-%m-%d %H:%M:%S') for d in self._execute_query(query)]

    def get_dates_in_range(self, start_time, end_time):
        query = ''' SELECT DISTINCT stamp_updated
                    from acct
                    WHERE datetime(stamp_updated) BETWEEN datetime(?) AND datetime(?);
                '''
        return [datetime.strptime(d[0], '%Y-%m-%d %H:%M:%S') for d in self._execute_query(query, [start_time, end_time])]

    def aggregate_data_per_field(self, start_time, end_time):
        query = ''' SELECT as_dst,SUM(bytes)
                    from acct
                    WHERE
                    datetime(stamp_updated) BETWEEN datetime(?) AND datetime(?)
                    GROUP by as_dst
                    ORDER BY SUM(bytes) DESC;
                '''
        return self._execute_query(query, [start_time, end_time])

    def aggregate_per_as(self, start_time, end_time):
        query = ''' SELECT as_dst,SUM(bytes)
                    from acct
                    WHERE
                    datetime(stamp_updated) BETWEEN datetime(?) AND datetime(?)
                    GROUP by as_dst
                    ORDER BY SUM(bytes) DESC;
                '''
        return self._execute_query(query, [start_time, end_time])

    def timeseries_per_as(self, start_time, end_time, asn):
        query = ''' SELECT SUM(bytes)
                    from acct
                    WHERE
                    datetime(stamp_updated) BETWEEN datetime(?) AND datetime(?)
                    AND
                    as_dst = ?
                    GROUP by as_dst, stamp_updated;
                '''
        return self._execute_query(query, [start_time, end_time, asn])

    def aggregate_per_prefix(self, start_time, end_time):
        query = ''' SELECT ip_dst,SUM(bytes)
                    from acct
                    WHERE
                    datetime(stamp_updated) BETWEEN datetime(?) AND datetime(?)
                    GROUP by ip_dst
                    ORDER BY SUM(bytes) DESC;
                '''
        return self._execute_query(query, [start_time, end_time])

    def timeseries_per_prefix(self, start_time, end_time, prefix):
        query = ''' SELECT SUM(bytes)
                    from acct
                    WHERE
                    datetime(stamp_updated) BETWEEN datetime(?) AND datetime(?)
                    AND
                    ip_dst = ?
                    GROUP by ip_dst, stamp_updated;
                '''
        return self._execute_query(query, [start_time, end_time, prefix])

    def get_total_traffic(self, start_time, end_time):
        query = ''' SELECT SUM(bytes)
                    FROM acct
                    WHERE
                    datetime(stamp_updated) BETWEEN datetime(?) AND datetime(?);
                '''
        return self._execute_query(query, [start_time, end_time])[0][0]

    def offloaded_bytes(self, num_prefixes, start_time, end_time):
        query = ''' SELECT SUM(bytes) FROM (
                        SELECT ip_dst, mask_dst, SUM(bytes) AS bytes
                        from acct
                        WHERE
                        datetime(stamp_updated) BETWEEN datetime(:start_time) AND datetime(:end_time)
                        GROUP BY ip_dst, mask_dst
                        ORDER BY SUM(bytes) DESC
                        LIMIT %d
                    );
                ''' % num_prefixes
        args = {
            'start_time': start_time,
            'end_time': end_time,
            'num_prefixes': num_prefixes,
        }
        return self._execute_query(query, args)[0][0]
