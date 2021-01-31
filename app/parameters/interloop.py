from app.parameters.base_scan import BaseScanParameters

class InterloopScanParameters(BaseScanParameters):
    def __init__(self, job_config):
        super().__init__(job_config)

        self.intg_limit = self.intg_precision * 10
        self.stationary_point = (0., 0.)
