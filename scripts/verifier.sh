#!/usr/bin/env bash
set -euo pipefail

python_command=python3
if [[ -x .venv/bin/python ]]; then
	python_command=.venv/bin/python
fi

"$python_command" -m coverage run --branch --source=backend -m unittest discover -s tests -v
"$python_command" -m coverage report --fail-under=80
