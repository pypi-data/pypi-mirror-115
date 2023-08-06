import typing as _typing


class ChannelInfo:
    def __init__(self, *args, **kwargs):
        self.sensor = kwargs.get("sensor", "")
        self.pressure_high = kwargs.get("pressure_high", None)
        self.pressure_hihi = kwargs.get("pressure_hihi", None)


class Channel:
    def __init__(
        self,
        name: str = "",
        prefix: str = "",
        num: int = 0,
        info: dict = None,
        enable: bool = True,
        **kwargs
    ):
        if not info:
            info = {}

        self.name = name
        self.num = num
        self.prefix = prefix
        self.enable = enable
        self.info: _typing.Optional[ChannelInfo] = None
        if info:
            self.info = ChannelInfo(**info)

    def __repr__(self):
        return "{}(prefix={},name={})".format(
            self.__class__.__name__, self.prefix, self.name
        )


class DeviceInfo:
    def __init__(self, **kwargs):
        self.config = kwargs.get("config", "")
        self.rack = kwargs.get("rack", 0)
        self.sector = kwargs.get("sector", "")
        self.serial_id = kwargs.get("serial_id", -1)

    def __repr__(self):
        return "{}(config={})".format(self.__class__.__name__, self.config)


class Device:
    def __init__(
        self,
        prefix: str = "",
        info: dict = None,
        channels: dict = None,
        enable=True,
        **kwargs
    ):
        if not info:
            info = {}
        if not channels:
            channels = {}

        self.enable = enable
        self.info = info
        self.prefix = prefix
        self.channels: _typing.List[Channel] = []
        self._generateChannels(channels)

        self.info: _typing.Optional[DeviceInfo] = None
        if info:
            self.info = DeviceInfo(**info)

    def getChannelByPrefix(self, prefix: str) -> Channel:
        for channel in self.channels:
            if channel.prefix == prefix:
                return

    def _generateChannels(self, data):
        for k, v in data.items():
            if v.__class__.__name__ == Channel.__class__.__name__:
                self.channels.append(v)
            else:
                self.channels.append(Channel(name=k, **v))

    def __repr__(self):
        return "{}(prefix={},enabled={})".format(
            self.__class__.__name__, self.prefix, self.enable
        )


class Beaglebone:
    def __init__(self, ip: str = "", devices: list = None):

        if not devices:
            devices = []

        self.ip = ip
        self.devices: _typing.List[Device] = []
        self._generateDevices(devices)

    def _generateDevices(self, data):
        for d in data:
            if d.__class__.__name__ == Device.__class__.__name__:
                self.devices.append(d)
            else:
                self.devices.append(Device(**d))

    def __repr__(self):
        return "{}(ip={},devices={})".format(
            self.__class__.__name__, self.ip, self.devices
        )


def getDevicesFromBeagles(
    beagles: _typing.List[Beaglebone],
) -> _typing.List[Device]:
    """Generate devices from beagle"""
    devices: _typing.List[Device] = []
    for beagle in beagles:
        for device in beagle.devices:
            devices.append(device)
    return devices


def getDevicesFromList(data: list) -> _typing.List[Device]:
    """Load datamodel objects from a list of dictionaries"""
    devices: _typing.List[Device] = []
    for d in data:
        devices.append(Device(**d))
    return devices


def getBeaglesFromList(data: dict) -> _typing.List[Beaglebone]:
    """Load datamodel objects from dictionary"""
    beagles: _typing.List[Beaglebone] = []
    for k, v in data.items():
        beagle = Beaglebone(ip=k, devices=v)
        beagles.append(beagle)

    return beagles
