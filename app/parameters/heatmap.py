from app.parameters.base_scan import BaseScanParameters
from app.models.discrete_plane import DiscretePlane

class HeatmapScanParameters(BaseScanParameters):
    def __init__(self, job_config):
        super().__init__(job_config)

        projection_min_x = job_config['heatmap']['min_x']
        projection_max_x = job_config['heatmap']['max_x']
        resolution_x_exp10 = job_config['heatmap']['resolution_x']
        projection_res_x = 10 ** resolution_x_exp10
        projection_min_y = job_config['heatmap']['min_y']
        projection_max_y = job_config['heatmap']['max_y']
        resolution_y_exp10 = job_config['heatmap']['resolution_y']
        projection_res_y = 10 ** resolution_y_exp10

        self.projection_space = DiscretePlane(
            projection_min_x, projection_max_x, projection_res_x,
            projection_min_y, projection_max_y, projection_res_y
        )
