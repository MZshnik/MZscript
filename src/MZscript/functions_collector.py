import inspect
import os
import logging
import importlib.util

from .database import Database
from .Functions import *
from .functions_handler import FunctionsHandler


class FunctionsCore(FunctionsHandler):
    def __init__(self, client, db_warns: bool, debug_log: bool, debug_console: bool):
        super().__init__()
        self.db_warns = db_warns
        self.debug_log = debug_log
        self.debug_console = debug_console
        self.client = client
        self.database = Database()
        self.funcs = {}
        self.load_functions()

    def load_functions(self):
        functions = []
        modules = []
        self.all_funcs = [func.lower() for func in self.all_funcs]

        functions_path = os.path.join(os.path.dirname(__file__), "Functions")
        for root, _, files in os.walk(functions_path):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    module_name = file[:-3]
                    module_path = os.path.join(root, file)
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        modules.append(module)

                        if hasattr(module, 'setup'):
                            module.setup(self)

                        for name, method in inspect.getmembers(module, inspect.isfunction):
                            functions.append((name, method))

        for func_name in self.all_funcs:
            func_key = func_name[1:]
            matched_func = next((method for name, method in functions if name.lower() == func_key), None)
            if matched_func:
                self.funcs[func_name] = matched_func
            else:
                logging.warning(f'WARNING: No command found for function "{func_name}".')

        self.sync_functions(self.funcs)
        for module in modules:
            if hasattr(module, 'sync_functions'):
                module.sync_functions(self.funcs)
