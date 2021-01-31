from scipy.integrate import odeint
import numpy as np
from itertools import tee


def integrate_full_trajectory(ode, x, y, precision, limit):
    initial_point = [x, y]
    tspan = np.arange(0., limit + precision, precision)
    # limit + precision because arange does [start, stop)

    return odeint(ode, initial_point, tspan)


def integrate_end_to_end(ode, x, y, limit):
    initial_point = [x, y]
    tspan = [0, limit]

    return odeint(ode, initial_point, tspan)


def integrate_step_by_step(ode, x, y, precision, limit):
    while limit > 0:
        x, y = integrate_next_step(ode, x, y, 0, precision)
        limit -= precision

    return x, y


def integrate_next_step(ode, x, y, t_i, t_j):
    point = [x, y]
    tspan = [t_i, t_j]

    step = odeint(ode, point, tspan) # => [point_i, point_j]

    return step[1][0], step[1][1]


def integrate_with_events(ode, x_0, y_0, precision, limit, observers):
    tspan = np.arange(0., limit + precision, precision)
    pairwise_tspan = pairwise(tspan)

    for observer in observers:
        observer.new_point(x_0, y_0, 0.)

    point_i = [x_0, y_0]

    for time_i, time_j in pairwise_tspan:
        point_j = odeint(ode, point_i, [time_i, time_j])[1]

        for observer in observers:
            observer.new_point(*point_j, time_j)

        point_i = point_j


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)

    return zip(a, b)
