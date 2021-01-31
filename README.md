# tfg-H16b

The code for my bachelor's thesis (TFG) in Informatics Engineering, carried out under the supervision of Professor Grigori Astrakharchik.

A numerical exploration of the second part of Hilbert's 16th problem.

## Requirements

### Install dependencies with Poetry

The project runs on Python 3.6.9. You may want to install it with [pyenv](https://github.com/pyenv/pyenv).

It uses [Poetry](https://python-poetry.org/) for dependency management. Poetry declares package dependencies in `pyproject.toml`, locks them to a specific version in `poetry.lock` and installs them on an isolated virtual environment for the project. Installation instructions for Poetry are [here](https://python-poetry.org/docs/#installation).

With Python 3.6.9 and Poetry installed, just run the following commands in the project's root directory:

```bash
poetry install
poetry shell
```

The application will probably work on later versions of Python and the dependencies, but I can't make any guarantees.

### Build the Docker image

Alternatively, the project provides a Dockerfile to build an environment with all the requirements installed.

You can execute `script/spawn_docker_shell.sh` to run the container with the necessary volumes.

## Usage

### Command-line interface

The application has a single entry point: `app/cli.py`. It provides two commands: `compute` for running the jobs and `view` for visualizing their results.

For `compute`, you are required to provide a job configuration file, the output path is optional:

```bash
python -m app.cli compute -j jobs/sign_change_test.yaml -o results/example.json
```

For `view`, you are required to provide an input file:

```bash
python -m app.cli view -i results/example.json
```

If you run this in an environment without GUI, like the Docker shell, the plot is saved to `results/example.png`.

Find more information about the commands and their options in `docs/cli-reference.txt`.

### Job configuration files

Job configuration files define the parameters that inform a `compute` execution.

Here's an example:

```yaml
# jobs/sign_change_test.yaml
job_type: scan_sign_change
logging:
  level: DEBUG
  file:
dynamical_system:
  a1: 1
  b1: 1
  c1: 0
  alpha1: 0
  beta1: 1
  a2: -10.0
  b2: 2.2
  c2: 0.7
  alpha2: -72.7778
  beta2: 0.0015
trajectory_integration:
  precision: -3
  limit: 10.0
phase_space_scan:
  resolution: -2
  min_x: -1.0
  max_x: 1.0
  min_y: -0.5
  max_y: 0.5
```

The application accepts the following job types: `compute_trajectory`, `scan_heatmap`, `scan_sign_change`, `scan_interloop_v2` and `scan_interloop_v3`.

For more information on writing configurations for a particular job type, refer to `docs/job-config-reference/`.

### Utility scripts

Directory `scripts/` provides a number of utilities that streamline interactions with the application.

For instance, there is `less_last_result.sh` to display the most recent results file in human-readable format, `tail_last_log.sh` to watch the log for a running job, or `test.sh` to perform a visual test for a given job type.

You can also `$ source script/functions` to load functions like `last_h16b_json`, which returns the path to the latest `compute` results file.

Lastly, there are a few scripts (prefixed `2mt` and `mt`) to access and operate within the MinoTauro GPU cluster.

All scripts should be executed from the project's root directory. Those that `view` results require Poetry.

## License

MIT
