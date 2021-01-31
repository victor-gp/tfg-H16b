#!/bin/bash

# spawns a Docker-based bash shell with dependencies installed and the Poetry venv loaded

# the results and logs generated inside the container are accessible from outside.
# the container listens to jobs/, app/ and script/ so changes outside are reflected inside.
# container and volumes are removed on exit, but not the image.

# build the image if it doesn't exist
docker image inspect tfg-h16b &> /dev/null || docker build . -t tfg-h16b

docker run -it --rm \
   -v "$PWD/results":/home/user/tfg-H16b/results \
   -v "$PWD/logs":/home/user/tfg-H16b/logs \
   -v "$PWD/jobs":/home/user/tfg-H16b/jobs:ro \
   -v "$PWD/app":/home/user/tfg-H16b/app:ro \
   -v "$PWD/script":/home/user/tfg-H16b/script:ro \
   tfg-h16b
