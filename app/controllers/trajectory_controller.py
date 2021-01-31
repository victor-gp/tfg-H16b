from app.functions.integrate_trajectory import integrate_with_events
from app.parameters.trajectory import TrajectoryParameters
from app.models.trajectory import Trajectory

import logging
from app.utils.config_logging import config_logging
from app.models.job_metadata import JobMetadata
from app.utils.heartbeat import Heartbeat
from app.utils.adapt_json import to_json
from app.utils.io_wrapper import IOWrapper


def compute_trajectory(args, job_config):
    config_logging(job_config)
    IOWrapper.config_compute_output(args, job_config)

    job_parameters = TrajectoryParameters(job_config)
    integration_parameters = unpack_integration_parameters(job_parameters)

    JobMetadata.init(job_config, job_parameters)
    Heartbeat.init(JobMetadata)

    trajectory = Trajectory()
    observers = [trajectory, Heartbeat]

    integrate_with_events(*integration_parameters, observers)

    JobMetadata.mark_job_end()

    IOWrapper.print_to_stderr(JobMetadata.summary())
    output_dict = {
        'job_metadata': JobMetadata.to_dict(),
        'job_config': job_config,
        'job_results': trajectory.to_dict()
    }
    IOWrapper.write(to_json(output_dict))


def unpack_integration_parameters(job_parameters):
    ode = job_parameters.dynamical_system.eval
    x_0 = job_parameters.x_0
    y_0 = job_parameters.y_0
    intg_precision = job_parameters.intg_precision
    intg_limit = job_parameters.intg_limit

    return [ode, x_0, y_0, intg_precision, intg_limit]
