import argparse
from sys import argv, exit
from os import environ
from app.utils.parse_job_config import parse_job_config
import app.controllers.trajectory_controller as trajectory_controller
import app.controllers.scans_controller as scans_controller
import app.controllers.views_controller as views_controller


def main():
    parser = build_parser()
    if len(argv) == 1:
        parser.print_usage()
        exit(2)

    args = parser.parse_args()
    args.func(args)

def build_parser():
    main_parser = argparse.ArgumentParser()
    subparsers = main_parser.add_subparsers(title="commands")

    compute_parser = subparsers.add_parser('compute', description=compute_description)
    compute_parser.set_defaults(func=compute)
    add_compute_arguments(compute_parser)

    view_parser = subparsers.add_parser('view', description=view_description, epilog=view_epilog)
    view_parser.set_defaults(func=view)
    add_view_arguments(view_parser)

    return main_parser


def compute(args):
    job_config = parse_job_config(args)
    job_type = job_config['job_type']
    action = compute_routes[job_type]

    action(args, job_config)

compute_routes = {
    'compute_trajectory': trajectory_controller.compute_trajectory,
    'scan_heatmap': scans_controller.scan_heatmap,
    'scan_sign_change': scans_controller.scan_sign_change,
    'scan_interloop_v2': scans_controller.scan_interloop_v2,
    'scan_interloop_v3': scans_controller.scan_interloop_v3
}

def view(args):
    args.with_display = environ.get('DISPLAY') is not None
    views_controller.view(args)

compute_description = 'run a job according to the parameters declared in a configuration file'

def add_compute_arguments(parser):
    parser.add_argument('-j', '--job-config', required=True, type=str,
        help="File where the program should read the job's configuration. " +
             'Must be a file present in jobs/.')
    parser.add_argument('--job-type', required=False, type=str,
        help='Overrides the job type declared in the job configuration file.')
    parser.add_argument('-o', '--output-file', required=False, type=str,
        help='File where the program should write the results of the job. ' +
             'Must be relative to results/. Default is "results/$job_type-$timestamp.json".')
    parser.add_argument('--stdout', action='store_true',
        help='If set, the program writes its results to standard output.')

view_description = 'plot the results of a compute job'
view_epilog = ("If the application doesn't detect a display, such as when running inside Docker " +
              'or when in an SSH session, the plots are saved in the same directory as the input ' +
              'file, with the same name and .png extension.')

def add_view_arguments(parser):
    parser.add_argument('-i', '--input-file', required=True, type=str,
        help='File where the program should read the data to be plotted. ' +
             'Must be a file present in results/.')
    parser.add_argument('--stdin', action='store_true',
        help='If set, the program reads the data to be plotted from standard input.')
    parser.add_argument('--json', action='store_true',
        help='If set, prints the input file in human readable format instead of plotting.')


if __name__ == '__main__':
    main()
