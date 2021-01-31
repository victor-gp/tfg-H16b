#!/bin/bash

# copy MinoTauro-generated files here

set -e
source .env

rsync -avzPh \
   --include=/{,results/{,'**'}} \
   --include=/{,logs/{,'**'}} \
   --include=/{,jobs/{,'**'}} \
   --exclude='*' \
   "$BSC_USERNAME"@dt01.bsc.es:tfg-H16b/ .
