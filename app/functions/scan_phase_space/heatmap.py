import logging

from app.functions.integrate_trajectory import integrate_full_trajectory
from app.models.scan_maps.heatmap import Heatmap
from app.models.job_metadata import JobMetadata
from app.utils.heartbeat import Heartbeat


def scan_heatmap(scan_params):
    ode = scan_params.dynamical_system.eval
    intg_precision = scan_params.intg_precision
    intg_limit = scan_params.intg_limit

    heatmap = Heatmap(scan_params)

    for (x,y) in scan_params.scan_range:
        trajectory = integrate_full_trajectory(ode, x, y, intg_precision, intg_limit)
        project_trajectory_points(heatmap, trajectory)

        Heartbeat.increase_iterations(1)

    JobMetadata.mark_job_end()

    return heatmap

def project_trajectory_points(heatmap, trajectory):
    for x, y in trajectory:
        heatmap.project(x, y)
