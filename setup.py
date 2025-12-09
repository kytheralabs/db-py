#!/usr/bin/env python
import os

from setuptools import setup, find_packages
from pkg_resources import parse_requirements

req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")

with open(req_file, "r") as inst_reqs:
    install_requires = [str(req) for req in parse_requirements(inst_reqs)]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="databricks_converter",
    version="0.0.9",
    author="aless10",
    description="It should convert a python module to databricks and viceversa.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aless10/convert-py-2-databricks",
    project_urls={
        "Bug Tracker": "https://github.com/aless10/convert-py-2-databricks/issues",
    },
    license='LICENSE',
    entry_points='[console_scripts]\n'
                 'databricks-converter=databricks_converter:main',
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)