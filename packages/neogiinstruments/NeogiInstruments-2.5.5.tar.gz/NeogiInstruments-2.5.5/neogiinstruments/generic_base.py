from .ports import find_ports
import param
import panel as pn


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

    def __init__(self, modules, name):
        super().__init__()
        self.param["name"].constant = False
        self.name = name
        self.param["name"].constant = True
        self.modules = modules
        self.hwids = [self.modules[i]["hwid"] for i in self.modules]
        self.reload_devices()
        self.button.on_click(self.reload_devices)
        devices = list(self.devices.keys())
        if "software" in devices:
            self.instrument_selected = "software"
        elif len(devices) > 0:
            self.instrument_selected = devices[0]

    def reload_devices(self, event=None, debug=False):
        ports = find_ports()
        self.devices = {}
        for module in self.modules:
            if self.modules[module]["function"] == "default":
                mname = self.modules[module]["name"]
                for hwid in self.modules[module]["hwid"]:
                    if hwid == "software":
                        name = self.modules[module]["name"]
                        self.devices[name] = {"name": name, "hwid": "software", "serial_number": "software",
                                              "module": module, "port": "software"}
                    else:
                        for port in ports:
                            if debug == True:
                                print(hwid)
                                print(port.hwid.split(" ")[1].replace("VID:PID=", ""))
                            if str(hwid) == port.hwid.split(" ")[1].replace("VID:PID=", ""):
                                if port.serial_number in self.modules[module]["serial"] or self.modules[module]["serial"] == "any":
                                    name = f"{port.serial_number} - {port.name} - {mname} - {port.name}"
                                    self.devices[name] = {"name": port.name, "hwid": port.hwid,
                                                          "serial_number": port.serial_number, "module": module,
                                                          "port": port}
                self.param["instrument_selected"].objects = self.devices.keys()
            else:
                for device in self.modules[module]["function"]():
                    self.devices[device] = {"name": device, "hwid": device, "serial_number": device, "module": module,
                                            "port": device}
                self.param["instrument_selected"].objects = self.devices.keys()

    @param.depends("instrument_selected", watch=True)
    def load_device(self):
        module = self.devices[self.instrument_selected]["module"]
        self.instrument = self.modules[module]["module"].instrument(
            self.devices[self.instrument_selected]["port"])
        initialized = True

    def view(self):
        try:
            return pn.Column(self.param, self.instrument.widgets(), self.button)
        except:
            return pn.Column(self.param, self.button)

    def serve(self):
        self.view().show(port=5006)

    def update_to_serial(self, serial):
        for device in self.devices:
            if self.devices[device]["serial_number"] == serial:
                self.instrument_selected = device
