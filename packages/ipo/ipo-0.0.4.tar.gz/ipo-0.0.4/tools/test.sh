#!/bin/bash

# © 2020, Midgard
# License: GPL-3.0-or-later
# This file is not available under the LGPL!

cd $(dirname "$0")/..

venv/bin/pip install pytest
exec venv/bin/pytest ./tests
