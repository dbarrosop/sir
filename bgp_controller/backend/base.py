
# TODO Add methods and document

class Backend:

    def __init__(self, conf):
        self.conf = conf

    def open(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def get_last_prefix_table(self):
        raise NotImplementedError

    def save_prefix_table(self, prefix_table, db_table):
        raise NotImplementedError
