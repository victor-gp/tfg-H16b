#!/bin/bash

which_python() {
   if [ "$(hostname)" = nvblogin1 ]; then
      echo python3
   else
      echo poetry run python
   fi
}

RESULTS_FILE_REGEX=".*.json"

find results/ -type f -type f -regex "$RESULTS_FILE_REGEX" -printf '%T@\t%p\n' |
sort -t $'\t' -g |
tail -n 1 |
cut -d $'\t' -f 2- |
xargs $(which_python) -m app.cli view --json --input-file |
less
