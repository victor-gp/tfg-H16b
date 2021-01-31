import numpy as np
from math import hypot # euclidean norm to zero
import logging

from app.functions.integrate_trajectory import integrate_step_by_step
from app.models.scan_maps.interloop import InterloopScanMap
from app.models.job_metadata import JobMetadata
from app.utils.heartbeat import Heartbeat


def scan_interloop(scan_params):
    ode = scan_params.dynamical_system.eval
    intg_precision = scan_params.intg_precision
    intg_limit = scan_params.intg_limit
    stationary_x, stationary_y = scan_params.stationary_point

    scan_map = InterloopScanMap(scan_params)

    for (x0, y0) in scan_params.scan_range:
        xn, yn = integrate_step_by_step(ode, x0, y0, intg_precision, intg_limit)
        bit = eval_trajectory(x0, y0, xn, yn, stationary_x, stationary_y)

        scan_map.project(x0, y0, bit)
        Heartbeat.increase_iterations(1)

    JobMetadata.mark_job_end()

    return scan_map


def eval_trajectory(x0, y0, xn, yn, stationary_x, stationary_y):
    distance_0 = hypot((x0 - stationary_x), (y0 - stationary_y))
    distance_n = hypot((xn - stationary_x), (yn - stationary_y))
    bit = int(distance_n > distance_0)
    # inbound loop = 0, outbound loop = 1

    return bit
