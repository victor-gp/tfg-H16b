#!/bin/bash

python -c 'print("\n" + "    CLI reference\n")'

poetry run python -m app.cli -h

python -c 'print("\n" + "="*80 + "\n\n" + "    COMPUTE\n")'

poetry run python -m app.cli compute -h

python -c 'print("\n" + "="*80 + "\n\n" + "    VIEW\n")'

poetry run python -m app.cli view -h

echo
