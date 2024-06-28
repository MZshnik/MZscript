import inspect
import os

from .database import Database
from .functions_handler import FunctionsHandler
import sys
import os
sys.path.append(os.path.dirname(__file__))

class FunctionsCore(FunctionsHandler):
    def __init__(self, client, db_warns: bool = False, debug_log: bool = False):
        super().__init__()
        self.db_warns = db_warns
        self.debug_log = debug_log
        self.client = client
        self.database = Database()
        self.load_functions()

    def load_functions(self):
        functions = []
        tempmods = []
        for i in [i for i in os.walk(os.path.dirname(__file__)+"/Functions") if not i[0].endswith("__pycache__")]:
            for j in i[2]:
                if j.endswith(".py") and j != "__init__.py":
                    exec(f"""
try:
    from .Functions.{i[0].replace(os.path.dirname(i[0]), "").replace("/", "").replace("\\", "")} import {j[:-3]} 
except:
    from .Functions import {j[:-3]}
tempmod = {j[:-3]}.setup(self)
tempmods.append(tempmod)
for k in inspect.getmembers(tempmod, inspect.ismethod):
    functions.append(k)""")
        for line in self.all_funcs:
            try:
                for i in functions:
                    if i[0][5:].lower() == line[1:].lower():
                        self.funcs[line] = i[1]
                        break
                else:
                    print(f"WARNING: For function \"{line}\" not exists command found.")
            except NameError as e:
                print(f"WARNING: For function \"{line}\" not exists command found.")
        self.sync_functions(self.funcs)
        for i in tempmods:
            i.sync_functions(self.funcs)
