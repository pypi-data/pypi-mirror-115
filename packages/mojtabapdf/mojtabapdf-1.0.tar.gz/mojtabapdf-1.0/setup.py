from os import name
from posixpath import expanduser
import setuptools
from pathlib import Path

from setuptools import version

setuptools.setup(
    name="mojtabapdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
