#made by @percy_jackson_4 ©2021-2022
import os
import sys
 
from DaisyX.utils.logger import log
 
LOADED_MODULES = []
MOD_Extras = {}
 
 
def list_all_modules() -> list:
    modules_directory = "DaisyX/modules/Extras"
 
    all_modules = []
    for module_name in os.listdir(modules_directory):
        path = modules_directory + "/" + module_name
 
        if "__init__" in path or "__pycache__" in path:
            continue
 
        if path in all_modules:
            log.path("Modules with same name can't exists!")
            sys.exit(5)
 
        # One file module type
        if path.endswith(".py"):
            # TODO: removesuffix
            all_modules.append(module_name.split(".py")[0])
 
        # Module directory
        if os.path.isdir(path) and os.path.exists(path + "/__init__.py"):
            all_modules.append(module_name)
 
    return all_modules
 
 
ALL_MODULES = sorted(list_all_modules())
__all__ = ALL_MODULES + ["ALL_MODULES"]
 
