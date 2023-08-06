#!python
import argparse

from siriuscommon.zabbix import ZabbixClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser("List zabbix items from host")
    parser.add_argument("host", help="host name")
    parser.add_argument("--user", "-u", help="zabbix user", required=True)
    parser.add_argument("--password", "-p", help="zabbix password", required=True)
    args = parser.parse_args()
    host = args.host.strip()

    client = ZabbixClient(user=args.user, password=args.password)
    res = client.get_items_from_host(host)

    print("item.id; item.name; item.hostid; hostname; item.lastvalue")
    for item in res:
        print(f"{item.itemid}; {item.name}; {item.hostid}; {host}; {item.lastvalue}")
