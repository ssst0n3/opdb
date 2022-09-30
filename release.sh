#!/usr/bin/env bash
rm opdb.egg-info/ dist/ -rf
python3 setup.py sdist
