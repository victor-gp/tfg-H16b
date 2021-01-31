import logging
import time

class Heartbeat:

    @classmethod
    def init(cls, job_metadata):
        cls.iterations_count = 0
        cls.previous_beat_at = time.time()
        cls.min_seconds_between_beats = 10
        cls.job_metadata = job_metadata


    @classmethod
    def increase_iterations(cls, n_iter):
        cls.iterations_count += n_iter
        if cls.should_beat(): cls.beat()

    @classmethod
    def should_beat(cls):
        return time.time() - cls.previous_beat_at > cls.min_seconds_between_beats

    @classmethod
    def beat(cls):
        logging.info(cls.progress_report())
        cls.previous_beat_at = time.time()


    @classmethod
    def new_point(cls, x, y, t):
        cls.increase_iterations(1)


    @classmethod
    def progress_report(cls):
        completed_percentage = (cls.iterations_count / cls.job_metadata.total_iterations) * 100
        current_execution_time = int(time.time() - cls.job_metadata.start_time)
        time_in_minutes = f'{current_execution_time//60}:{(current_execution_time%60):02d}'

        return f'time: {time_in_minutes}, progress: {completed_percentage:.2f}%'
