import inspect
import os

from .database import Database
from .Functions import *
from .functions_handler import FunctionsHandler


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
        for i in os.listdir(os.getcwd()+"\\src\\MZscript\\Functions"):
            if i.endswith(".py") and i != "__init__.py":
                exec(f"""
tempmod = {i[:-3]}.setup(self)
tempmods.append(tempmod)
for i in inspect.getmembers(tempmod, inspect.ismethod):
    functions.append(i)""")
        for line in self.all_funcs:
            try:
                for i in functions:
                    if i[0][5:].lower() == line[1:].lower():
                        self.funcs[line] = i[1]
                        break
                else:
                    print(f"WARNING: for command \"{line}\" not exists function found.")
            except NameError as e:
                print(f"WARNING: for command \"{line}\" not exists function found.")
        self.sync_functions(self.funcs)
        for i in tempmods:
            i.sync_functions(self.funcs)