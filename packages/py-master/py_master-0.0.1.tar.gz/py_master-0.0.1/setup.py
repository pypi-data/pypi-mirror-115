#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_master",
    version="0.0.1",
    author="patrickxu",
    author_email="patrickxu@wiatec.com",
    description="common package",
    license='MIT License',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/patrickxu1986/py_master",
    packages=setuptools.find_packages(),
    platforms='any',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)


import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_master",
    version="0.0.1",
    author="patrickxu",
    author_email="patrickxu@wiatec.com",
    description="common package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/patrickxu1986/py_master",
    project_urls={
        "Bug Tracker": "https://github.com/patrickxu1986/py_master/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)