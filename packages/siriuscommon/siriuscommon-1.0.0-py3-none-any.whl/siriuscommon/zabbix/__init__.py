import typing as _typing
from datetime import datetime as _datetime

import requests as _requests
from pyzabbix import ZabbixAPI as _ZabbixAPI

from .. import get_logger
from .types import ZabbixHistory, ZabbixTrend, _make_zabbix_history, _make_zabbix_trend

_logger = get_logger(__name__)


class ZabbixItem(object):
    def __init__(
        self,
        data,
    ) -> None:
        self,
        self.itemid: str = data["itemid"]
        self.value_type: int = int(data["value_type"])
        self.hostid: str = data["hostid"]
        self.name: str = data["name"]
        self.lastvalue: _typing.Any = data["lastvalue"]
        self.key_: str = data["key_"]
        self.data = data

    def __str__(self) -> str:
        return str(self.data)


class ZabbixClient:
    def __init__(
        self, user: str, password: str, server: str = "https://10.0.38.46:20093"
    ) -> None:

        self._session = _requests.Session()
        self._session.verify = False
        self._api: _ZabbixAPI = _ZabbixAPI(server=server, session=self._session)
        self._api.login(
            user=user,
            password=password,
        )

    def get_item(self, itemid: str) -> _typing.Optional[ZabbixItem]:
        response = self._api.do_request(
            method="item.get",
            params={
                "itemids": itemid,
            },
        )
        result = response["result"]
        if len(result) == 1:
            return ZabbixItem(result[0])
        else:
            return None

    def get_items_from_host(self, host: str) -> _typing.List[ZabbixItem]:
        response = self._api.do_request(
            method="item.get",
            params={
                "host": host,
            },
        )
        return [ZabbixItem(data) for data in response["result"]]

    def get_item_trends(
        self,
        itemid: str,
        time_from: _typing.Optional[_datetime] = None,
        time_till: _typing.Optional[_datetime] = None,
    ) -> _typing.List[ZabbixTrend]:
        item = self.get_item(itemid=itemid)
        if not item:
            raise Exception("Item not found")

        payload: _typing.Dict[str, _typing.Union[str, int, _typing.List]] = {
            "itemids": itemid,
            "sortfield": "clock",
            "output": [
                "itemid",
                "clock",
                "num",
                "value_avg",
                "value_min",
                "value_max",
            ],
            "history": item.value_type,
        }
        if time_from:
            payload["time_from"] = int(time_from.timestamp())

        if time_till:
            payload["time_till"] = int(time_till.timestamp())

        response = self._api.do_request("trend.get", payload)
        return [_make_zabbix_trend(data) for data in response["result"]]

    def get_item_history(
        self,
        itemid: str,
        time_from: _typing.Optional[_datetime] = None,
        time_till: _typing.Optional[_datetime] = None,
    ) -> _typing.List[ZabbixHistory]:
        item = self.get_item(itemid=itemid)
        if not item:
            raise Exception("Item not found")

        payload: _typing.Dict[str, _typing.Union[str, int]] = {
            "itemids": itemid,
            "sortfield": "clock",
            "output": "extend",
            "history": item.value_type,
        }
        if time_from:
            payload["time_from"] = int(time_from.timestamp())

        if time_till:
            payload["time_till"] = int(time_till.timestamp())

        response = self._api.do_request("history.get", payload)
        return [_make_zabbix_history(data) for data in response["result"]]
