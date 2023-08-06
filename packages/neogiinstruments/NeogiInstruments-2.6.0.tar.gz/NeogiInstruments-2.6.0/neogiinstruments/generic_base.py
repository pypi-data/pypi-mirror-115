from typing import Dict, List

import panel as pn
import param

from .instrumenttype import InstrumentType, Device


class Instrument:
    def __init__(self, modules, name="Untitled"):
        self.modules = modules
        self.name = name

    def __call__(self, name=None, *args, **kwargs):
        if name is None:
            name = self.name
        return InstrumentWrapper(self.modules, name)


class InstrumentWrapper(param.Parameterized):
    instrument_selected = param.ObjectSelector()
    button = pn.widgets.Button(name='Reload devices', button_type='primary')
    initialized = False
    old_methods: List[str] = []
    new_methods: List[str] = []
    devices: Dict[str, Device] = {}
    modules: List[InstrumentType]

    def __init__(self, modules: List[InstrumentType], name):
        super().__init__()
        self.param["name"].constant = False
        self.name = name
        self.param["name"].constant = True
        self.modules = modules
        self.hwids = [module.hwid for module in self.modules]
        self.reload_devices()
        self.button.on_click(self.reload_devices)
        devices = list(self.devices.keys())
        if "software" in devices:
            self.instrument_selected = "software"
        elif len(devices) > 0:
            self.instrument_selected = devices[0]

    def reload_devices(self, event=None):
        self.devices = {}
        for module in self.modules:
            self.devices = self.devices | module.find_devices()
        self.param["instrument_selected"].objects = self.devices.keys()

    @param.depends("instrument_selected", watch=True)
    def load_device(self):
        module = self.devices[self.instrument_selected].module
        self.instrument = module.instrument_module.instrument(self.devices[self.instrument_selected].port)
        self.old_methods = self.new_methods
        self._remove_old(self.old_methods)
        self.new_methods = [method for method in dir(self.instrument) if not method.startswith("__")]
        self._add_new(self.new_methods)  # The unholy runtime inheritance hack

    def view(self):
        try:
            return pn.Column(self.param, self.instrument.widgets(), self.button)
        except:
            return pn.Column(self.param, self.button)

    def serve(self):
        self.view().show(port=5006)

    def update_to_serial(self, serial):
        for device in self.devices:
            if self.devices[device].serial_number == serial:
                self.instrument_selected = device

    def _add_new(self, methods):
        for method in methods:
            setattr(self, method, getattr(self.instrument, method))

    def _remove_old(self, methods):
        for method in methods:
            delattr(self, method)
