import typing as _typing


class ArchiverDisconnectedPV(_typing.NamedTuple):
    host_name: str
    pv_name: str
    connection_lost_at: str
    instance: str
    internal_state: str
    command_thread_id: str
    no_connection_as_of_epoch_secs: str
    last_known_event: str
    extras: dict


def _make_archiver_disconnected_pv(
    hostName,
    pvName,
    connectionLostAt,
    instance,
    internalState,
    commandThreadID,
    noConnectionAsOfEpochSecs,
    lastKnownEvent,
    **extras,
) -> ArchiverDisconnectedPV:
    return ArchiverDisconnectedPV(
        host_name=hostName,
        pv_name=pvName,
        connection_lost_at=connectionLostAt,
        instance=instance,
        internal_state=internalState,
        command_thread_id=commandThreadID,
        no_connection_as_of_epoch_secs=noConnectionAsOfEpochSecs,
        last_known_event=lastKnownEvent,
        extras=extras,
    )


class ArchiverPausedPV(_typing.NamedTuple):
    pv_name: str
    instance: str
    modification_time: str


def _make_archiver_paused_pv(pvName, instance, modificationTime, **extras):
    return ArchiverPausedPV(
        pv_name=pvName, instance=instance, modification_time=modificationTime
    )


asd = {
    "lastRotateLogs": "Never",
    "appliance": "lnls_control_appliance_1",
    "pvName": "PRO:MBTemp2:Ch3",
    "pvNameOnly": "PRO:MBTemp2:Ch3",
    "connectionState": "false",
    "lastEvent": "Never",
    "samplingPeriod": "1.0",
    "isMonitored": "false",
    "connectionLastRestablished": "Never",
    "connectionFirstEstablished": "Never",
    "connectionLossRegainCount": "0",
    "status": "Being archived",
}


class ArchiverStatusPVExtras:
    last_rotate_logs: str
    appliance: str
    pv_name_only: str
    connection_state: str
    last_event: str
    sampling_period: str
    is_monitored: str
    connection_last_restablished: str
    connection_first_established: str
    connection_loss_regain_count: str


class ArchiverStatusPV:
    pv_name: str
    status: str
    extras: _typing.Optional[ArchiverStatusPVExtras]


def _make_archiver_status_pv(pvName: str, status: str, **extras):
    return ArchiverStatusPV(
        pv_name=pvName,
        status=status,
        extras=None
        if extras
        else ArchiverStatusPVExtras(
            last_rotatelogs=extras["lastRotateLogs"],
            appliance=extras["appliance"],
            pv_name_only=extras["pvNameOnly"],
            connection_state=extras["connectionState"],
            last_event=extras["lastEvent"],
            sampling_period=extras["samplingPeriod"],
            is_monitored=extras["isMonitored"],
            connection_last_restablished=extras["connectionLastRestablished"],
            connection_first_established=extras["connectionFirstEstablished"],
            connection_loss_regain_count=extras["connectionLossRegainCount"],
        ),
    )
