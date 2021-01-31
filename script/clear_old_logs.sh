#!/bin/bash

set -euo pipefail

KEEP_LATEST_DEFAULT=10
KEEP_LATEST=${1:-$KEEP_LATEST_DEFAULT}

if ! [[ $KEEP_LATEST =~ ^[0-9]+$ ]] ; then
   echo "clear_old_logs: invalid number of logs to keep: ‘$KEEP_LATEST’." \
        "default is $KEEP_LATEST_DEFAULT" >&2
   exit 1
fi

LOG_FILE_REGEX='.*.log'

find logs/ -maxdepth 1 -type f -regex "$LOG_FILE_REGEX" -printf '%T@\t%p\n' |
sort -t $'\t' -g |
head -n "-${KEEP_LATEST}" |
cut -d $'\t' -f 2- |
xargs rm
