#!/bin/bash

LOG_FILE_REGEX=".*.log"

find logs/ -type f -type f -regex "$LOG_FILE_REGEX" -printf '%T@\t%p\n' |
sort -t $'\t' -g |
tail -n 1 |
cut -d $'\t' -f 2- |
xargs tail -f
