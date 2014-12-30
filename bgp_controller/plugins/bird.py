from base import PrefixPlugin

import os


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
        - policy_file: path to the file where to save the prefix list
        - reload_bird: Whether to reload bird or not.
    Example:
        Configuration example::

            Bird:
              policy_file: '/Users/dbarroso/Documents/workspace/pmacct_data/allow_prefixes.bird'
              reload_bird: True
    """
    skip_simulation = False
    run_once_during_simulations = True

    def run(self):
        policy_file = self.conf['Bird']['policy_file']

        of = open(policy_file, 'w')
        # header
        of.write('function allow_prefixes() {\n  return net ~ [\n')

        # allowed prefixes
        for p in self.new_pt.get_prefixes()[0:-1]:
            of.write('    %s,\n' % p.get_prefix())

        # last prefix does not have a comma
        of.write('    %s\n' % self.new_pt.get_prefixes()[-1].get_prefix())
        of.write('  ];\n}\n')
        of.close()

        if self.conf['Bird']['reload_bird']:
            os.system("birdc configure")
