#!/bin/bash

# © 2020, Midgard
# License: GPL-3.0-or-later
# This file is not available under the LGPL!

cd $(dirname "$0")/..

# Create virtualenv
python3 -m virtualenv venv/

# Install dependencies
venv/bin/pip install -e .
