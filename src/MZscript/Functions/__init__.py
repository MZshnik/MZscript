import os
import sys
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import importlib

for i in [i for i in os.walk(os.path.dirname(__file__)) if not i[0].endswith("__pycache__")][1:]:
    directory = i[0].replace(os.path.dirname(i[0])+"\\", ".").replace("\\", ".")
    for j in i[2]:
        if j.endswith(".py") and j != "__init__.py":
            importlib.import_module("."+j[:-3], directory)