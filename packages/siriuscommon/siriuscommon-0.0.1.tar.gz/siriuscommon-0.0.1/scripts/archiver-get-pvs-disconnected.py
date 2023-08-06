#!/usr/bin/env python
from siriuscommon.archiver import getCurrentlyDisconnectedPVs

if __name__ == "__main__":
    pvs = getCurrentlyDisconnectedPVs()
    for pv in pvs:
        print(pv.pv_name)
