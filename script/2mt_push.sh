#!/bin/bash

# update project files on MinoTauro

set -e
source .env

rsync -avzPh \
   --exclude='.git*' \
   --exclude=.vscode \
   --exclude=victor-utils \
   --exclude='.env' \
   --exclude='__pycache__' \
   --exclude='logs/*' \
   --exclude='results/*' \
   . "$BSC_USERNAME"@dt01.bsc.es:tfg-H16b
