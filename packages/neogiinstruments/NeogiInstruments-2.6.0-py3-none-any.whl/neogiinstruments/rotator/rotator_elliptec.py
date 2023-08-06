import elliptec

name = "elliptec"
hwid = ["0403:6015"]


def find_ports():
    return elliptec.find_ports()
    # more or less documentation on finding the rotator


# elliptec = { git = 'https://github.com/UNTNeogiLab/TL-rotation-control' }
# add line to pyproject.toml or package
class instrument:
    def __init__(self, port):
        self.rotator = elliptec.Motor(port.device)
        self.max_degree = 180
        self.min_degree = -180

    def home(self):
        self.degree = 0
        self.rotator.do_("home")

    def move_abs(self, value):
        val_dif = (value - self.degree) % 360
        self.move_rel(val_dif)

    def move_rel(self, val_dif):
        new_val = self.degree + val_dif
        while new_val > self.max_degree:
            new_val -= 360
            val_dif -= 360
        while new_val < self.min_degree:
            new_val += 360
            val_dif += 360
        val = self.rotator.deg_to_hex(abs(val_dif))
        self.rotator.set_('stepsize', val)
        if val_dif > 0:
            self.rotator.do_("forward")
            self.degree = (self.degree + val_dif)
        elif val_dif < 0:
            self.rotator.do_("backward")
            self.degree = (self.degree + val_dif)
        else:
            print("No change, moving 0 degrees")
