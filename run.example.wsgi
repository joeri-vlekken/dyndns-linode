#! /path/to/.virtualenvs/dyndns-linode/bin/python3

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/path/to/application/')
from app import app as application
application.secret_key = 'oareipgjeroiugheroiughreqoiguehioe'
