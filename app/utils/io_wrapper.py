from sys import stdin, stdout, stderr
from datetime import datetime as dt
from os.path import relpath, commonprefix
from signal import signal, SIGPIPE, SIG_DFL


class IOWrapper:

    @classmethod
    def read(cls):
        if cls.stdin:
            return stdin.read()
        else:
            with open(cls.input_path, 'r') as f:
                return f.read()

    @classmethod
    def write(cls, str):
        if cls.stdout:
            signal(SIGPIPE, SIG_DFL)
            stdout.write(str)
        else:
            with open(cls.output_path, 'w') as f:
                f.write(str)

    @classmethod
    def print_to_stderr(cls, str):
        print(str, file=stderr)


    @classmethod
    def config_input(cls, args):
        if args.stdin:
            cls.stdin = True
        else:
            cls.stdin = False
            validate(args.input_file)
            cls.input_path = args.input_file

    @classmethod
    def config_compute_output(cls, args, job_config):
        if args.stdout:
            cls.stdout = True
        else:
            cls.stdout = False
            job_type = job_config['job_type']
            cls.output_path = which_output_path(args.output_file, job_type)

    @classmethod
    def config_echo_output(cls):
        cls.stdout = True

    @classmethod
    def get_plot_path(cls):
        return json_to_png_extension(cls.input_path)


def which_output_path(output_file_path, job_type):
    if output_file_path is not None:
        validate(output_file_path)
        return output_file_path
    else:
        return f'results/{default_output_filename(job_type)}'

def default_output_filename(job_type):
    timestamp = dt.now().strftime("%Y%m%dT%H%M%S")
    return f'{job_type}-{timestamp}.json'

def json_to_png_extension(json_path):
    path_without_extension, _ = json_path.rsplit('.json', 1)
    return f'{path_without_extension}.png'

def validate(path):
    given_path = relpath(path)
    results_dir = relpath('results/')

    if commonprefix([given_path, results_dir]) != results_dir:
        raise ValueError(
            f'Invalid path: {given_path}. It must be inside directory {results_dir}.'
        )
