#!/usr/bin/env bash

python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip
find . -name "requirements.txt" -type f -exec ./venv/bin/pip3 install -r '{}' ';'