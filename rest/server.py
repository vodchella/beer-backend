#!/usr/bin/env python3.6

import importlib
import os
import pid
import sys
import tempfile
import yaml
from glob import glob
from pkg.app import app, v1
from pkg.config import CONFIG, CFG_FILE
from pkg.constants.version import SOFTWARE_VERSION
from pkg.sanic_peewee import Peewee
from pkg.utils.errors import get_raised_error
from pkg.utils.console import panic
from pkg.utils.logger import DEFAULT_LOGGER


if __name__ == '__main__':
    if sys.version_info < (3, 6):
        panic('We need mininum Python verion 3.6 to run. Current version: %s.%s.%s' % sys.version_info[:3])

    try:
        host = CONFIG['rest']['listen_host']
        port = CONFIG['rest']['listen_port']
    except:
        DEFAULT_LOGGER.critical(get_raised_error(full=True))
        sys.exit(1)

    pid_file = f'beer-rest-{port}'
    pid_dir = tempfile.gettempdir()
    pid_file_full = f'{pid_dir}/{pid_file}.pid'
    pid_ok = False
    try:
        with pid.PidFile(pid_file, piddir=pid_dir) as p:
            pid_ok = True
            DEFAULT_LOGGER.info(f'{SOFTWARE_VERSION} starting, PID: {p.pid}, File: {pid_file_full}')
            DEFAULT_LOGGER.info(f'Config loaded from {CFG_FILE}:\n{yaml.dump(CONFIG, default_flow_style=False)}')

            peewee = Peewee('postgresqlext://postgres:postgres@localhost:5432/beer')
            db = peewee(app)
            app.db = db

            DEFAULT_LOGGER.info(f'Loading application modules...')
            for md in [os.path.basename(x)[:-3] for x in glob('./pkg/app/*.py') if x[-11:] != '__init__.py']:
                importlib.import_module(f'pkg.app.{md}')
                DEFAULT_LOGGER.info(f'... {md} loaded')

            app.blueprint(v1)
            app.host, app.port = host, port
            app.static_routes = list(filter(lambda r: r.name == 'static', app.router.routes_all.values()))
            app.run(host=host, port=port, access_log=False)
    except:
        if pid_ok:
            raise
        else:
            DEFAULT_LOGGER.critical(f'Something wrong with {pid_file_full}. Maybe it\'s locked?')
