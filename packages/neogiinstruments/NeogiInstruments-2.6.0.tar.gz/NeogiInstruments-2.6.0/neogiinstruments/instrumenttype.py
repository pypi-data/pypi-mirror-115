from dataclasses import dataclass
from types import ModuleType
from typing import Callable
from typing import Dict, Union, List

from serial.tools.list_ports_common import ListPortInfo

from .ports import find_ports


@dataclass
class InstrumentType:
    name: str
    instrument_module: ModuleType
    hwid: List[str]
    serial_number: Union[List[str], str] = "any"
    function: Callable = None

    def find_devices(self):
        if self.function is None:
            return find_devices(self)
        else:
            return {device: Device(device, self, device, device, device) for device in self.function()}


@dataclass
class Device:
    name: str
    module: InstrumentType
    hwid: str = "software"
    serial_number: str = "software"
    port: Union[str, ListPortInfo] = "software"


def find_devices(instrument: InstrumentType) -> Dict[str, Device]:
    ports = find_ports()
    devices = {}
    for hwid in instrument.hwid:
        if hwid == "software":
            devices[instrument.name] = Device(instrument.name, instrument)
        else:
            for port in ports:
                if str(hwid) == port.hwid.split(" ")[1].replace("VID:PID=", ""):
                    if port.serial_number in instrument.serial_number or instrument.serial_number == "any":
                        name = f"{port.serial_number} - {port.name} - {instrument.name} - {port.name}"
                        devices[name] = Device(port.name, instrument, port.hwid, port.serial_number, port)
    return devices
