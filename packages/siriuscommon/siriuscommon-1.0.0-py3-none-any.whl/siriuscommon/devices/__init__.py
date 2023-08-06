#!/usr/bin/env python
import logging as _logging
import typing as _typing

import requests as _requests

from .. import get_logger

_logger = get_logger(level=_logging.INFO)
TIMEFMT = "%d/%m/%Y %H:%M:%S"
API_CANDIDATES = [
    "10.0.38.42:26001",
    "10.0.38.46:26001",
    "10.0.38.59:26001",
    "localhost:8080",
]
_TIMEOUT = 5


class RemoteAPI(Exception):
    pass


def checkCandidates() -> str:
    for ip in API_CANDIDATES:
        url = "http://{}".format(ip)
        try:
            if _requests.get(url + "/status", timeout=2).text == "Healthy!":
                _logger.info('Using remote url "{}"'.format(url))
                return url + "/devices"
        except Exception:
            _logger.warning('Remote url "{}" unavailable'.format(url))
            pass
    raise RemoteAPI("No remote API available")


def getMBTemp() -> _typing.List[dict]:
    """MBTemp json from upstream @return dict following the data_model pattern"""
    return _requests.get(
        checkCandidates(), verify=False, params={"type": "mbtemp"}, timeout=_TIMEOUT
    ).json()


def getMKS() -> _typing.List[dict]:
    """MKS json from upstream @return dict following the data_model pattern"""
    return _requests.get(
        checkCandidates(), verify=False, params={"type": "mks"}, timeout=_TIMEOUT
    ).json()


def getAgilent() -> _typing.List[dict]:
    """Agilent json from upstream @return dict following the data_model pattern"""
    return _requests.get(
        checkCandidates(), verify=False, params={"type": "agilent"}, timeout=_TIMEOUT
    ).json()


def getDevicesDict(data: dict) -> _typing.Iterable[dict]:
    """Device generator from json"""
    for _ip, beagle in data.items():
        for device in beagle:
            yield device


def getChannelsDict(data: dict) -> _typing.Iterable[_typing.Tuple[str, str, dict]]:
    """Tuple of (device prefix, channel_name, channel_data) generator from json"""
    for _ip, beagle in data.items():
        for device in beagle:
            for channel_name, channel_data in device["channels"].items():
                yield device["prefix"], channel_name, channel_data


if __name__ == "__main__":
    # for ip, dev in getAgilent().items():
    data = getAgilent()
    for device, channel_name, channel_data in getChannelsDict(data):
        print(device, channel_name, channel_data["prefix"])
