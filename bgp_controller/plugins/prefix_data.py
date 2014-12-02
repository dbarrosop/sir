from base import PrefixPlugin
import os
from shutil import copyfile


class SavePrefixData(PrefixPlugin):
    """
    Name:
        SavePrefixData
    Author:
        David Barroso <dbarroso@spotify.com>
    Description:
        Saves all the prefixes in new_pt in a CSV file with detailed information for further processing. The data
        saved will contain the following information::

            DST_IP;DST_MASK;PACKETS;BYTES;AVG_PACKETS;AVG_BYTES;AGE

    Requires:
        - new_pt
    Configuration:
        - latest_data_file: path to the file where to save the data
        - preserve_data_files: If set to True we will rotate the file latest_data_file appending the date to
            the filename. If set to False we will overwrite it and the previous content will be lost.
    """

    skip_simulation = False
    run_once_during_simulations = False

    def save_prefix_statistics(self):

        if os.path.isfile(self.conf['latest_data_file']) and self.conf['preserve_data_files']:
            old_data_file = '%s.%s' % (self.conf['latest_data_file'], self.time)
            copyfile(self.conf['latest_data_file'], old_data_file)

        with open(self.conf['latest_data_file'], "w") as f:
            f.write('DST_IP;DST_MASK;PACKETS;BYTES;AVG_PACKETS;AVG_BYTES;AGE\n')
            for p in self.new_pt.prefixes.items():
                f.write(p[1].csv())
            f.close()

    def run(self):
        self.save_prefix_statistics()
