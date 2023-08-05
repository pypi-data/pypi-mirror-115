#!/bin/zsh

./cleanup.sh

./venv/bin/python setup.py sdist
twine upload dist/*