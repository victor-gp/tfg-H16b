import logging
from datetime import datetime as dt
from os.path import relpath, commonprefix


def config_logging(job_config):
    loglevel_option = job_config['logging']['level']
    log_file_option = job_config['logging']['file']
    job_type = job_config['job_type']

    logging.basicConfig(
        filename = which_log_filename(log_file_option, job_type),
        level = extract_loglevel(loglevel_option),
        format='[%(asctime)s] %(levelname)s -- %(name)s/%(module)s: %(message)s',
    )


def extract_loglevel(loglevel_option):
    numeric_loglevel = getattr(logging, loglevel_option.upper(), None)
    if not isinstance(numeric_loglevel, int):
        raise ValueError(f'Invalid log level: {loglevel_option}')

    return numeric_loglevel


def which_log_filename(log_file_path, job_type):
    if log_file_path is not None:
        validate(log_file_path)
        return log_file_path
    else:
        return f'logs/{default_log_filename(job_type)}'

def default_log_filename(job_type):
    timestamp = dt.now().strftime("%Y%m%dT%H%M%S")
    return f'{timestamp}-{job_type}.log'

def validate(path):
    given_path = relpath(path)
    logs_dir = relpath('logs/')

    if commonprefix([given_path, logs_dir]) != logs_dir:
        raise ValueError(
            f'Invalid path: {given_path}. It must be inside directory {logs_dir}.'
        )
