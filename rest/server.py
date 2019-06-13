#!/usr/bin/env python3.6

import sys
from pkg.utils.console import panic


if __name__ == '__main__':
    if sys.version_info < (3, 6):
        panic('We need mininum Python verion 3.6 to run. Current version: %s.%s.%s' % sys.version_info[:3])
    print('All OK!')
