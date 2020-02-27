import os.path
import glob
import sys
import inspect
from seer import data_collector_plugin

PYTHON_EXTENSION = '.py'
IGNORED_FILES = ['__init__.py']

modules = glob.glob(os.path.join(os.path.dirname(__file__), '*' + PYTHON_EXTENSION))

__all__ = [os.path.basename(f)[:-len(PYTHON_EXTENSION)] for f in modules if os.path.isfile(f) and os.path.basename(f) not in IGNORED_FILES]
from . import *

def gather_plugins():
	plugins = []
	for _, value in globals().items():
		for _, obj in inspect.getmembers(value, inspect.isclass):
			if obj != data_collector_plugin and issubclass(obj, data_collector_plugin):
				plugins.append(obj)

	return plugins