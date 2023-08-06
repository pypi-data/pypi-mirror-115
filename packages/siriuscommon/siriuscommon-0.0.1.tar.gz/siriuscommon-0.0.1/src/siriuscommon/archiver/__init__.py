import requests as _requests
import typing as _typing

from .types import (
    ArchiverDisconnectedPV,
    ArchiverPausedPV,
    _make_archiver_disconnected_pv,
    _make_archiver_paused_pv,
    _make_archiver_status_pv,
)

_default_base_url = "https://10.0.38.42"


class ArchiverLoginException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ArchiverClient:
    def __init__(
        self,
        base_url: str = _default_base_url,
        username: _typing.Optional[str] = None,
        password: _typing.Optional[str] = None,
    ) -> None:

        self._mgmt_url = f"{base_url}/mgmt/bpl"
        self._authenticated = False

        self._session: _requests.Session = _requests.Session()

        if username and password:
            self.login(username, password)

    def login(self, username: str, password: str):
        data = {"username": username, "password": password}

        response = self._session.post(
            f"{self._mgmt_url}/login", data=data, verify=False
        )
        self._authenticated = (
            response.status_code == 200 and "authenticated" in response.text
        )
        if not self.authenticated:
            raise ArchiverLoginException(f"failed to authenticat user {username}")

    def pause_pv(self, pv_name: str):
        if not self.authenticated:
            raise ArchiverLoginException("operation requires authentication")

        if not pv_name:
            raise ValueError()

        response = self._session.get(f"{self._mgmt_url}/pauseArchivingPV?pv={pv_name}")
        if (
            response.status_code == 200
            and (f"Successfully paused the archiving of PV {pv_name}")
            or (f"PV {pv_name} is already paused") in response.text
        ):
            return True
        return False

    @property
    def authenticated(self):
        return self._authenticated


def getCurrentlyDisconnectedPVs(
    base_url: str = _default_base_url,
) -> _typing.List[ArchiverDisconnectedPV]:
    return [
        _make_archiver_disconnected_pv(**pv)
        for pv in _requests.get(
            f"{base_url}/mgmt/bpl/getCurrentlyDisconnectedPVs", verify=False
        ).json()
    ]


def getPausedPVsReport(
    base_url: str = _default_base_url,
) -> _typing.List[ArchiverPausedPV]:
    return [
        _make_archiver_paused_pv(**pv)
        for pv in _requests.get(
            f"{base_url}/mgmt/bpl/getPausedPVsReport", verify=False
        ).json()
    ]


def getMatchingPVs(search: str, base_url: str = _default_base_url) -> _typing.List[str]:
    return [
        pv
        for pv in _requests.get(
            f"{base_url}/retrieval/bpl/getMatchingPVs?pv={search}&limit=500",
            verify=False,
        ).json()
    ]


def getPVStatus(search: str, base_url: str = _default_base_url):
    return [
        _make_archiver_status_pv(**pv)
        for pv in _requests.get(
            f"{base_url}/mgmt/bpl/getPVStatus",
            params={"pv": search, "reporttype": "short"},
            verify=False,
        ).json()
    ]
