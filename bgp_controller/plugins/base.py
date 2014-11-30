
class PrefixPlugin:
    skip_simulation = False
    run_once_during_simulations = False

    def __init__(self, conf, data_file, raw_pt, new_pt, prev_pt, bgp_table, time, simulation, last_run):
        self.conf = conf
        self.data_file = data_file
        self.raw_pt = raw_pt
        self.new_pt = new_pt
        self.prev_pt = prev_pt
        self.bgp_table = bgp_table
        self.time = time
        self.simulation = simulation
        self.last_run = last_run

    def _execute(self):
        if not self.simulation or (self.simulation and not self.skip_simulation):
            runnable = True
        else:
            runnable = False

        if not self.run_once_during_simulations or ( self.run_once_during_simulations and self.last_run):
            pass # We stick with the previous decision
        else:
            runnable = False

        if runnable:
            self.run()

    def run(self):
        raise NotImplementedError
