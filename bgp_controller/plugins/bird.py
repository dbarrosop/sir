from base import PrefixPlugin

import os
from shutil import copyfile

class Bird(PrefixPlugin):
    """
    Name:
        Bird
    Author:
        David Barroso <dbarroso@spotify.com>
    Description:
        Updates the prefix list that controls which prefix lists to install on the FIB and reloads bird.
    Requires:
        - new_pt
    Configuration:
        - bird_policy_file: path to the file where to save the prefix list
    """
    skip_simulation = False
    run_once_during_simulations = True

    def run(self):
        """
        Test2
        """
        #previous_policy_file = self.conf['bird_previous_policy_file']
        policy_file = self.conf['bird_policy_file']

        #if previous_policy_file is not None:
        #    if os.path.isfile(policy_file):
        #        copyfile(policy_file, '%s.previous' % policy_file)

        of = open(policy_file, 'w')
        #header
        of.write('function allow_prefixes() {\n  return net ~ [\n')

        #allowed prefixes
        for p in self.new_pt.get_prefixes()[0:-1]:
            of.write('    %s,\n' % p.get_prefix())

        #last prefix does not have a comma
        of.write('    %s\n' % self.new_pt.get_prefixes()[-1].get_prefix())
        of.write('  ];\n}\n')
        of.close()

        os.system("birdc configure")
