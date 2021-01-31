from app.utils.io_wrapper import IOWrapper
import json
from app.utils.adapt_json import to_json
from matplotlib.pyplot import switch_backend as switch_matplotlib_backend

from app.models.trajectory import Trajectory
from app.models.scan_maps.heatmap import Heatmap
from app.models.scan_maps.sign_change import SignChangeSparseMap
from app.models.scan_maps.interloop import InterloopScanMap


def view(args):
    IOWrapper.config_input(args)

    job_data = IOWrapper.read()
    job_data_dict = json.loads(job_data)

    if args.json:
        echo(job_data_dict)
    else:
        plot(job_data_dict['job_results'], args.with_display)


def plot(results_dict, with_display):
    results_object = restore_results_object(results_dict)

    if with_display:
        results_object.plot()
    else:
        switch_matplotlib_backend('AGG')
        results_object.plot(save_path=IOWrapper.get_plot_path())


def restore_results_object(results_dict):
    if '__trajectory__' in results_dict:
        return Trajectory.from_dict(results_dict)
    elif '__heatmap__' in results_dict:
        return Heatmap.from_dict(results_dict)
    elif '__sign_change_sparse_map__' in results_dict:
        return SignChangeSparseMap.from_dict(results_dict)
    elif '__interloop_scan_map__' in results_dict:
        return InterloopScanMap.from_dict(results_dict)
    else: raise RuntimeError('Unrecognized results object')


def echo(job_data_dict):
    IOWrapper.config_echo_output()
    json_str = to_json(job_data_dict, human_readable=True)

    IOWrapper.write(json_str)
