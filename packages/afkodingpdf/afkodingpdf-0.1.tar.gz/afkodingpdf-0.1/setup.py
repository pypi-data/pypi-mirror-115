from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="afkodingpdf",
    version=0.1,
    long_description=Path("README.md").read_text(),
    packages=find_packages(exclude=["tests", "data"]),
)
