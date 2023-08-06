#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-zenloop",
    version="0.1.0",
    description="Singer tap to extract Zenloop data",
    author="cargo.one",
    url="https://cargo.one",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_zenloop"],
    install_requires=[
        "singer-python==5.13.*",
        "requests==2.28.*",
        "pendulum==2.1.*",
    ],
    entry_points="""
    [console_scripts]
    tap-zenloop=tap_zenloop:main
    """,
    packages=["tap_zenloop"],
    package_data = {
        "schemas": ["tap_zenloop/schemas/*.json"]
    },
    include_package_data=True,
)
