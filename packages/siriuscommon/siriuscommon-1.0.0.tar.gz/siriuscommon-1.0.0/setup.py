#!/usr/bin/env python
import pkg_resources
from setuptools import find_packages, setup

from src.siriuscommon import __author__, __version__


def get_abs_path(relative):
    return pkg_resources.resource_filename(__name__, relative)


def get_long_description() -> str:
    desc = ""
    with open(get_abs_path("README.md"), "r") as _f:
        desc += _f.read().strip()

    desc += "\n\n"

    with open(get_abs_path("CHANGES.md"), "r") as _f:
        desc += _f.read().strip()

    return desc


long_description = get_long_description()


with open(get_abs_path("requirements.txt"), "r") as _f:
    requirements = _f.readlines()

setup(
    author=__author__,
    classifiers=[
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
    ],
    description="Commons for Sirius applications",
    download_url="https://github.com/lnls-sirius/sirius-common",
    install_requires=requirements,
    include_package_data=True,
    license="GNU GPLv3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="siriuscommon",
    packages=find_packages(
        where="src",
        include=[
            "siriuscommon*",
        ],
    ),
    scripts=[
        "scripts/archiver-get-pv-status.py",
        "scripts/archiver-get-pvs-disconnected.py",
        "scripts/archiver-get-pvs-matching.py",
        "scripts/archiver-get-pvs-paused.py",
        "scripts/zabbix-get-item-history.py",
        "scripts/zabbix-get-item-trend.py",
        "scripts/zabbix-get-items-from-host.py",
    ],
    package_dir={"": "src"},
    python_requires=">=3.6",
    url="https://github.com/lnls-sirius/sirius-common/",
    version=__version__,
    zip_safe=True,
)
