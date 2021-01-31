import yaml
from os.path import relpath, commonprefix


def parse_job_config(args):
    job_config_file = args.job_config
    validate(job_config_file)
    with open(job_config_file) as f:
        job_config = yaml.safe_load(f)

    if args.job_type is not None:
        job_config['job_type'] = args.job_type

    return job_config

def validate(path):
    given_path = relpath(path)
    jobs_dir = relpath('jobs/')

    if commonprefix([given_path, jobs_dir]) != jobs_dir:
        raise ValueError(
            f'Invalid path: {given_path}. It must be inside directory {jobs_dir}.'
        )
