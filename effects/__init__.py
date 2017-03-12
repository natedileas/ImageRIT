effect_functions = {}

import importlib
import glob
from os.path import dirname, basename, isfile

modules = glob.glob(dirname(__file__)+"/*.py")

for file in [basename(f)[:-3] for f in modules if isfile(f)]:
    if file == '__init__':
        continue

    module = importlib.import_module(__name__ + '.' + file)

    if hasattr(module, 'effect_functions'):
        effect_functions.update(module.effect_functions)

del module, importlib, glob, dirname, basename, isfile, file, modules, f