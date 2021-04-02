#!/usr/bin/env python3

import sys
sys.path.insert(0, '/misc/linux/centos7/x86_64/local/stow/python-3.6/lib/python3.6/site-packages/')
from wsgiref.handlers import CGIHandler
from app import app
CGIHandler().run(app)

