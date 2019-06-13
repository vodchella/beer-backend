#!/usr/bin/env python3.6

import pid
import sys
import tempfile
import yaml
from pkg.config import CONFIG, CFG_FILE
from pkg.utils.console import panic
from pkg.utils.logger import LOGGER


if __name__ == '__main__':
    if sys.version_info < (3, 6):
        panic('We need mininum Python verion 3.6 to run. Current version: %s.%s.%s' % sys.version_info[:3])

    pid_file = 'beer-rest'
    pid_dir = tempfile.gettempdir()
    pid_ok = False
    try:
        with pid.PidFile(pid_file, piddir=pid_dir) as p:
            pid_ok = True
            LOGGER.info('MyBeer REST server started')
            LOGGER.info('PID: %s' % p.pid)
            LOGGER.info(f'Config loaded from {CFG_FILE}:\n{yaml.dump(CONFIG, default_flow_style=False)}')
    except:
        if pid_ok:
            raise
        else:
            LOGGER.critical(f'Something wrong with {pid_dir}/{pid_file}.pid. Maybe it\'s locked?')
