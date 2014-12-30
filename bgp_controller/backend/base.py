class Backend:
    """
    This class defines all the methods and their input that a backend has to provide in order to be able to used by the
    BGPController.
    """

    def __init__(self, conf):
        self.conf = conf['backend_options']

    def open(self):
        """
        Opens the backend

        :return: None
        """
        raise NotImplementedError

    def close(self):
        """
        Closes the backend

        :return: None
        """

        raise NotImplementedError

    def get_best_prefixes(self, start_time, end_time, max_routes, packet_sampling):
        """
        This method will return the best prefixes within the specified range

        :param start_time: (datetime) Starting time for the time range
        :param end_time: (datetime) Ending time for the time range
        :param max_routes: (int) Maximum routes you want
        :param packet_sampling: (int) Packet sampling of the data stored
        :return: A PrefixTable containing the best prefixes within the specified range
        """
        raise NotImplementedError

    def get_raw_prefixes(self, start_time, end_time, packet_sampling):
        """
        This method will return all the prefixes within the specified range

        :param start_time: (datetime) Starting time for the time range
        :param end_time: (datetime) Ending time for the time range
        :param packet_sampling: (int) Packet sampling of the data stored
        :return: A PrefixTable containing all the prefixes within the specified range
        """
        raise NotImplementedError

    def get_previous_prefixes(self, start_time, end_time):
        """
        This method will return the latest best prefixes within the specified range

        :param start_time: (datetime) Starting time for the time range
        :param end_time: (datetime) Ending time for the time range
        :return: A PrefixTable containing all the latest best prefixes within the specified range
        """
        raise NotImplementedError

    def save_prefix_table(self, prefix_table, date):
        """
        This method will save a PrefixTable into the backend. In order to be unique a date must be specified.

        :param prefix_table: A PrefixTable.
        :param date: (datetime) Unique date to mark the prefixes.
        :return: None
        """
        raise NotImplementedError

    def save_dict(self, data_dict, db_table):
        """
        This will save a dictionary into a table. The columns of the dict will be the fields and the values, the values.

        :param data_dict: Dictionary to save.
        :param db_table: The table name
        :return: None
        """
        raise NotImplementedError

    def get_data_from_table(self, table, filter=None):
        """
        Will a list of lists where the first element is the schema definition (column names) and the rest of the
        elements are a list of values in the same order as column names.
        :param table: (str) Table to query.
        :param filter: (str) Optional filter to send to the query
        :return: A list of lists containing the column names as the first element and the values as the rest.
        """
        raise NotImplementedError

    def get_available_dates_in_range(self, start_time, end_time):
        """
        Given a time frame returns a list of valid dates with data.

        :param start_time: (datetime) Starting time for the time range
        :param end_time: (datetime) Ending time for the time range
        :return: A list of dates
        """
        raise NotImplementedError

    def purge_data(self, current_time):
        """
        This method will delete all of the old data in the database.

        :param current_time: (datetime) Current time
        :return: None
        """
        raise NotImplementedError
