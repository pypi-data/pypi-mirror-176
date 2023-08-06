import setuptools
from pathlib import Path

setuptools.setup(
    name="jackyleeutils",
    author="jackyleeutils",
    version="0.0.13",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    packages=setuptools.find_packages(
        exclude=["data", "tests", "scripts", "log"])
)
