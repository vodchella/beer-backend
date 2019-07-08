import importlib
import os
from glob import glob
from pkg.utils.logger import DEFAULT_LOGGER


def dynamic_import(path, module, prompt, module_imported_string):
    DEFAULT_LOGGER.info(prompt)
    for md in [os.path.basename(x)[:-3] for x in glob(f'{path}/*.py') if x[-11:] != '__init__.py']:
        importlib.import_module(f'{module}.{md}')
        DEFAULT_LOGGER.info(module_imported_string % md)
