from app.functions.scan_phase_space.heatmap import scan_heatmap as _scan_heatmap
from app.functions.scan_phase_space.sign_change import scan_sign_change as _scan_sign_change
from app.functions.scan_phase_space.interloop_v2 import scan_interloop as _scan_interloop_v2
from app.functions.scan_phase_space.interloop_v3 import scan_interloop as _scan_interloop_v3
from app.parameters.base_scan import BaseScanParameters
from app.parameters.interloop import InterloopScanParameters
from app.parameters.heatmap import HeatmapScanParameters

import logging
from app.utils.config_logging import config_logging
from app.models.job_metadata import JobMetadata
from app.utils.heartbeat import Heartbeat
from app.utils.adapt_json import to_json
from app.utils.io_wrapper import IOWrapper


def scan_heatmap(args, job_config):
    run(args, job_config, _scan_heatmap, HeatmapScanParameters)

def scan_sign_change(args, job_config):
    run(args, job_config, _scan_sign_change, BaseScanParameters)

def scan_interloop_v2(args, job_config):
    run(args, job_config, _scan_interloop_v2, InterloopScanParameters)

def scan_interloop_v3(args, job_config):
    run(args, job_config, _scan_interloop_v3, InterloopScanParameters)


def run(args, job_config, scan_function, scan_parameters_class):
    config_logging(job_config)
    IOWrapper.config_compute_output(args, job_config)

    scan_parameters = scan_parameters_class(job_config)
    JobMetadata.init(job_config, scan_parameters)
    Heartbeat.init(JobMetadata)

    results = scan_function(scan_parameters)

    logging.info(JobMetadata.summary())
    IOWrapper.print_to_stderr(JobMetadata.summary())

    output_dict = {
        'job_metadata': JobMetadata.to_dict(),
        'job_config': job_config,
        'job_results': results.to_dict()
    }
    IOWrapper.write(to_json(output_dict))
