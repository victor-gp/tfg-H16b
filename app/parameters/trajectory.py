from math import ceil
from app.models.dynamical_system import DynamicalSystem

class TrajectoryParameters:

    def __init__(self, job_config):
        dynamical_system_dict = job_config['dynamical_system']
        self.dynamical_system = DynamicalSystem(*dynamical_system_dict.values())

        self.x_0 = job_config['trajectory']['x_0']
        self.y_0 = job_config['trajectory']['y_0']
        intg_precision_exp10 = job_config['trajectory_integration']['precision']
        self.intg_precision = 10 ** intg_precision_exp10
        self.intg_limit = job_config['trajectory_integration']['limit']

        self.total_iterations = self.compute_total_iterations()


    def compute_total_iterations(self):
        return ceil(self.intg_limit / self.intg_precision)
