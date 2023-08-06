class TTBusDeviceAddress:
    def __init__(self, address, node):
        self.address = address
        self.node = node

    @property
    def id(self):
        return f"{self.address:02X}_{self.node:02X}"

    @property
    def as_tuple(self):
        return self.address, self.node

    def __str__(self):
        return f"{type(self).__name__}(0x{self.address:02X}, 0x{self.node:02X})"

    def __eq__(self, other):
        return self.as_tuple == other.as_tuple

    def __hash__(self) -> int:
        return hash(self.as_tuple)