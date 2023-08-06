import typing as _typing
from datetime import datetime as _datetime


class ZabbixTrend(_typing.NamedTuple):
    data: dict
    timestamp: _datetime
    value_avg: str
    value_min: str
    value_max: str
    num: int


def _make_zabbix_trend(data: dict) -> ZabbixTrend:
    return ZabbixTrend(
        timestamp=_datetime.fromtimestamp(int(data["clock"])),
        value_avg=data["value_avg"],
        value_min=data["value_min"],
        value_max=data["value_max"],
        num=data["num"],
        data=data,
    )


class ZabbixHistory(_typing.NamedTuple):
    itemid: str
    value: str
    timestamp: _datetime
    data: dict


def _make_zabbix_history(data: dict):
    return ZabbixHistory(
        itemid=data["itemid"],
        value=data["value"],
        timestamp=_datetime.fromtimestamp(int(data["clock"])),
        data=data,
    )
