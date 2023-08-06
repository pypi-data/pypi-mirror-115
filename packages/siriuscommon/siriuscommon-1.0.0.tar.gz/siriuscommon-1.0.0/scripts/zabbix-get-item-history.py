#!/usr/bin/env python
import argparse
from datetime import datetime

from siriuscommon.zabbix import ZabbixClient

if __name__ == "__main__":
    fmt = "%d/%m/%Y %H:%M"
    _fmt = fmt.replace("%", "")
    parser = argparse.ArgumentParser("List zabbix item history")
    parser.add_argument("itemid", help="item id")
    parser.add_argument("tini", help=f"tIni {_fmt}")
    parser.add_argument("tend", help=f"tEnd {_fmt}")
    parser.add_argument("--user", "-u", help="zabbix user", required=True)
    parser.add_argument("--password", "-p", help="zabbix password", required=True)

    args = parser.parse_args()

    itemid = args.itemid.strip()
    tini = datetime.strptime(args.tini, fmt)
    tend = datetime.strptime(args.tend, fmt)

    client = ZabbixClient(user=args.user, password=args.password)
    res = client.get_item_history(itemid, tini, tend)

    print("item.value; timestamp")
    for item in res:
        print(f"{item.value}; {item.timestamp}")
