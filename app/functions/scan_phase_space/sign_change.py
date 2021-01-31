import numpy as np
import logging

from app.functions.integrate_trajectory import integrate_next_step
from app.models.scan_maps.sign_change import SignChangeSparseMap
from app.models.job_metadata import JobMetadata
from app.utils.heartbeat import Heartbeat


# sign as in the partial derivative's sign
def scan_sign_change(scan_params):
    ode = scan_params.dynamical_system.eval
    intg_precision = scan_params.intg_precision

    scan_map = SignChangeSparseMap()

    for x, y in scan_params.scan_range:
        x_pre, y_pre = integrate_next_step(ode, x, y, 0., -intg_precision)
        x_post, y_post = integrate_next_step(ode, x, y, 0., intg_precision)

        evaluate_and_map(x_pre, y_pre, x, y, x_post, y_post, scan_map)
        Heartbeat.increase_iterations(1)

    JobMetadata.mark_job_end()

    return scan_map


def evaluate_and_map(x_pre, y_pre, x, y, x_post, y_post, scan_map):
    x_delta_1 = x - x_pre
    x_delta_2 = x_post - x

    if x_delta_1 * x_delta_2 < 0:
        if x_delta_1 < 0: scan_map.add_right_change(x,y)
        else: scan_map.add_left_change(x, y)

    y_delta_1 = y - y_pre
    y_delta_2 = y_post - y

    if y_delta_1 * y_delta_2 < 0:
        if y_delta_1 < 0: scan_map.add_up_change(x, y)
        else: scan_map.add_down_change(x, y)
