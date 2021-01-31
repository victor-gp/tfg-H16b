import numpy as np
import logging

from app.functions.integrate_trajectory import integrate_end_to_end
from app.models.scan_maps.interloop import InterloopScanMap
from app.models.job_metadata import JobMetadata
from app.utils.heartbeat import Heartbeat


def scan_interloop(scan_params):
    ode = scan_params.dynamical_system.eval
    intg_precision = scan_params.intg_precision
    intg_limit = scan_params.intg_limit
    scan_resolution = scan_params.scan_resolution
    stationary_x, stationary_y = scan_params.stationary_point

    scan_map = InterloopScanMap(scan_params)

    for (x, y) in scan_params.scan_range:
        x_ref, y_ref = reference_point(x, y, stationary_x, stationary_y, scan_resolution)
        trajectory = local_trajectory(ode, x, y, intg_precision)
        ref_trajectory = local_trajectory(ode, x_ref, y_ref, intg_precision)
        cmp = compare_trajectories(trajectory, ref_trajectory)

        scan_map.project(x, y, cmp)
        Heartbeat.increase_iterations(1)

    JobMetadata.mark_job_end()

    return scan_map


def reference_point(x, y, stationary_x, stationary_y, scan_resolution):
    dir = direction(stationary_x, stationary_y, x, y)
    x_ref = x + dir[0]*scan_resolution
    y_ref = y + dir[1]*scan_resolution
    return x_ref, y_ref

def direction(x1, y1, x2, y2):
    vector = [x2 - x1, y2 - y1]
    magnitude = np.linalg.norm(vector)
    # alt: distance = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    return vector/magnitude


def local_trajectory(ode, x, y, intg_precision):
    intg_limit = 10 * intg_precision
    return integrate_end_to_end(ode, x, y, intg_limit)


def compare_trajectories(trajectory, ref_trajectory):
    # 0 means the distance decreases, 1 the distance increases
    [tr_0, tr_n] = trajectory
    [ref_0, ref_n] = ref_trajectory
    delta_0 = distance(*tr_0, *ref_0)
    delta_n = distance(*tr_n, *ref_n)

    if delta_0 < delta_n: return 0
    if delta_0 > delta_n: return 1

def distance(x1, y1, x2, y2):
    vector = [x2 - x1, y2 - y1]
    return np.linalg.norm(vector)
