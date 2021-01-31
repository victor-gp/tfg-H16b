from time import time
from datetime import datetime

class JobMetadata:

    @classmethod
    def init(cls, job_config, job_parameters):
        cls.job_config = job_config
        cls.job_parameters = job_parameters
        cls.total_iterations = job_parameters.total_iterations
        cls.start_time = time()

    @classmethod
    def mark_job_end(cls):
        cls.end_time = time()

    @classmethod
    def summary(cls):
        return f'job execution time: {cls.execution_time_in_minutes()}'

    @classmethod
    def to_dict(cls):
        return {
            '__job_metadata__': True,
            'date_time': datetime.fromtimestamp(cls.start_time).isoformat(),
            'execution_time_s': cls.execution_time(),
            'total_iterations': cls.total_iterations
        }

    @classmethod
    def execution_time(cls):
        return int(cls.end_time - cls.start_time)

    @classmethod
    def execution_time_in_minutes(cls):
        execution_time = cls.execution_time()
        return f'{execution_time//60}:{(execution_time%60):02d}'
