#!/usr/bin/env python3.6

import copy
import pid
import sys
import tempfile
import yaml
from lib.sanic_peewee import Peewee
from pkg.config import CONFIG, CFG_FILE
from pkg.constants.version import SOFTWARE_VERSION
from pkg.rest import app, v1
from pkg.utils.dynamic_import import dynamic_import
from pkg.utils.console import panic
from pkg.utils.errors import get_raised_error
from pkg.utils.logger import DEFAULT_LOGGER


def get_settings():
    try:
        _host = CONFIG['rest']['listen_host']
        _port = CONFIG['rest']['listen_port']
        _pg_host = CONFIG['postgres']['host']
        _pg_port = CONFIG['postgres']['port']
        _pg_user = CONFIG['postgres']['user']
        _pg_pass = CONFIG['postgres']['pass']
        _pg_db = CONFIG['postgres']['db']
        return _host, _port, _pg_host, _pg_port, _pg_user, _pg_pass, _pg_db
    except:
        DEFAULT_LOGGER.critical(get_raised_error(full=True))
        sys.exit(1)


if __name__ == '__main__':
    if sys.version_info < (3, 6):
        panic('We need minimum Python version 3.6 to run. Current version: %s.%s.%s' % sys.version_info[:3])

    host, port, pg_host, pg_port, pg_user, pg_pass, pg_db = get_settings()

    pid_file = f'beer-rest-{port}'
    pid_dir = tempfile.gettempdir()
    pid_file_full = f'{pid_dir}/{pid_file}.pid'
    pid_ok = False
    try:
        with pid.PidFile(pid_file, piddir=pid_dir) as p:
            pid_ok = True

            secure_config = copy.deepcopy(CONFIG)
            secure_config['log']['logdna']['key'] = '*****'
            secure_config['postgres']['pass'] = '*****'

            DEFAULT_LOGGER.info(f'{SOFTWARE_VERSION} starting, PID: {p.pid}, File: {pid_file_full}')
            DEFAULT_LOGGER.info(f'Config loaded from {CFG_FILE}:\n{yaml.dump(secure_config, default_flow_style=False)}')

            peewee = Peewee(f'postgresqlext://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
            db = peewee(app)
            app.db = db

            dynamic_import('./pkg/rest',
                           'pkg.rest',
                           'Loading REST modules...',
                           '... %s loaded')

            app.blueprint(v1)
            app.host, app.port = host, port
            app.static_routes = list(filter(lambda r: r.name == 'static', app.router.routes_all.values()))
            app.run(host=host, port=port, access_log=False)
    except:
        if pid_ok:
            raise
        else:
            DEFAULT_LOGGER.critical(f'Something wrong with {pid_file_full}. Maybe it\'s locked?')
