#!/bin/sh
# TODO: Add other tests

PYTHONPATH='.' python3 tests/test_rigged_rng.py
PYTHONPATH='.' python3 tests/test_toroidal_node.py
