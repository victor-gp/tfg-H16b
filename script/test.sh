#!/bin/bash

# compute a quick job and plot its result.
# - takes the job configuration defined in jobs/$1_test.yaml
# - can patch the job type declared in the job config with $2 (optional)

# examples:
# script/test.sh interloop
# script/test.sh interloop scan_interloop_v2

set -e

if [[ -z "$1" ]]; then
   echo "test: a job config prefix is required!" \
        "the script prepends it to ‘_test.json’ and uses that for --job-config."
   exit 1
fi

JOB_CONFIG_PREFIX=$1

if [[ "$2" ]]; then
   JOB_TYPE_OPTION="--job-type $2";
fi

which_python() {
   if [ "$(hostname)" = nvblogin1 ]; then
      echo python3
   else
      echo poetry run python
   fi
}

local_python=$(which_python)

set -x

$local_python -m app.cli compute \
   --job-config jobs/"$JOB_CONFIG_PREFIX"_test.yaml \
   $JOB_TYPE_OPTION \
   --output-file results/test.json

$local_python -m app.cli view --input-file results/test.json

rm results/test.json
