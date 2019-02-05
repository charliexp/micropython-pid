#!/bin/sh

python3 -m coverage run ./test/unit.py && python3 -m coverage report -m && python3 -m coverage html
