import inspect
import logging
import os
from datetime import datetime

from .database import Database
from .Functions import *
from .functions_handler import FunctionsHandler


class FunctionsCore(FunctionsHandler):
    """
    ## Collecting info about all settings and functions
    """
    def __init__(self, client, db_warns: bool, debug_log: bool, debug_console: bool):
        super().__init__()
        self.db_warns = db_warns
        self.debug_log = debug_log
        self.debug_console = debug_console
        self.client = client
        self.loaded_mods = []
        self.python_vars = {"uptime": datetime.now().timestamp()}
        self.database = Database()
        self.funcs = {}
        self.load_functions()

    def load_functions(self):
        """
        ## Load functions from "Functions" directory
        """
        functions = []
        self.loaded_mods = []
        self.all_funcs = [i.lower() for i in self.all_funcs]
        # get all files of directory .Functions
        for i in os.walk(os.path.dirname(__file__)+"/Functions"):
            # from all folders, subfolders, we get only files
            for j in i[2]:
                # for file in folder
                if j.endswith(".py") and j != "__init__.py":
                    # invoke setup function and get all in-class methods
                    # and we get this class from setup function
                    exec(f"""
tempmod = {j[:-3]}.setup(self)
self.loaded_mods.append(tempmod)
for k in inspect.getmembers(tempmod, inspect.ismethod):
    functions.append(k)""")

        # here we register methods to functions
        for line in self.all_funcs:
            try:
                for i in functions:
                    if i[0][5:].lower() == line[1:]:
                        self.funcs[line] = i[1]
                        break
                else:
                    logging.warning(f"WARNING: For function \"{line}\" not exists command found.")
            except NameError:
                logging.warning(f"WARNING: For function \"{line}\" not exists command found.")
        self.sync_functions(self.funcs)
        for i in self.loaded_mods:
            i.sync_functions(self.funcs)

    def add_function(self, func_name: str, func_method):
        # TODO: Make chosing type of function (logic/no arg/can be no arg)
        """
        ## Adds new $function to handlering
        
        ### Args:
            func_name (`str`): Name of function with $ in lowercase
            func_method (`function`): Function method to execute
        """
        self.funcs[func_name] = func_method
        self.all_funcs.append(func_name)
        self.sync_functions(self.funcs)
        for i in self.loaded_mods:
            i.sync_functions(self.funcs)