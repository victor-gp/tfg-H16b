from app.models.discrete_plane import DiscretePlane
from app.models.dynamical_system import DynamicalSystem

class BaseScanParameters:

    def __init__(self, job_config):
        dynamical_system_dict = job_config['dynamical_system']
        self.dynamical_system = DynamicalSystem(*dynamical_system_dict.values())

        intg_precision_exp10 = job_config['trajectory_integration']['precision']
        self.intg_precision = 10 ** intg_precision_exp10
        self.intg_limit = job_config['trajectory_integration']['limit']

        scan_resolution_exp10 = job_config['phase_space_scan']['resolution']
        self.scan_resolution = 10 ** scan_resolution_exp10

        scan_min_x = job_config['phase_space_scan']['min_x']
        scan_max_x = job_config['phase_space_scan']['max_x']
        scan_min_y = job_config['phase_space_scan']['min_y']
        scan_max_y = job_config['phase_space_scan']['max_y']
        self.scan_space = DiscretePlane(
            scan_min_x, scan_max_x, self.scan_resolution,
            scan_min_y, scan_max_y, self.scan_resolution
        )

        self.scan_range = self.scan_space.range()
        self.total_iterations = self.compute_total_iterations()


    def compute_total_iterations(self):
        initial_positions = self.scan_space.range()
        # cannot reuse the attribute cause iterables can only be traversed once!

        return sum([1 for xy in initial_positions])
