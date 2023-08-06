#!/usr/bin/env python
from siriuscommon.archiver import getPausedPVsReport

if __name__ == "__main__":
    pvs = getPausedPVsReport()
    for pv in pvs:
        print(pv.pv_name)
