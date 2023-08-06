# dynamic loading based on Dashboard code
# Version 3 dynamic loader
import os
import warnings
from importlib import import_module
from pathlib import Path

from .generic_base import Instrument
from .instrumenttype import InstrumentType

here = str(Path(__file__).resolve().parent)
directory_name = here.replace(str(Path(__file__).resolve().parent.parent), "").replace("/", "")  # gross solution

for directory in os.scandir(here):
    if directory.is_dir() and not directory.name.__contains__("__"):
        modules = []
        for file in os.listdir(directory):
            dname = str(directory.name).replace(here, "")
            if str(file).__contains__(f"{dname}_"):
                sname = str(file).replace(".py", "")
                try:
                    module = import_module(f"{directory_name}.{directory.name}.{sname}")
                    try:
                        serial = module.serial_number
                    except:
                        serial = "any"
                    try:
                        function = module.get_devices
                    except:
                        function = None
                    modules.append(InstrumentType(module.name, module, module.hwid, serial, function))
                except Exception as ex:
                    print(f"{file} import failed")
                    print(ex)
        globals()[directory.name] = Instrument(modules=modules, name=directory.name)
    elif directory.name.__contains__("ports"):
        globals()["ports"] = import_module(f"{directory_name}.ports")
    elif not directory.name.__contains__("__"):
        file = directory.name
        if not (str(file).__contains__("base") or str(file).__contains__("type")):
            sname = file.replace(".py", "")
            try:
                module = import_module(f"{directory_name}.{sname}")
                try:
                    name = module.name
                    hwid = module.hwid
                    try:
                        serial = module.serial_number
                    except:
                        serial = "any"
                    try:
                        function = module.get_devices
                    except:
                        function = None
                    modules = [InstrumentType(name, module, hwid, serial, function)]
                    globals()[name] = Instrument(modules=modules, name=name)
                except:
                    name = sname
                    warnings.warn(
                        f"{sname} not properly formatted, implement name and hwid and create a class to use properly.")
                    globals()[name] = module
            except Exception as ex:
                print(f"{file} import failed")
                print(ex)
