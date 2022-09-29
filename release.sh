#!/usr/bin/env bash
tar czvf pystack.tar.gz pystack
tar czvf opdb.tar.gz --exclude=.git --exclude=.idea --exclude=*.tar.gz --exclude=pystack --exclude=venv .