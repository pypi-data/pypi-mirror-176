#!/usr/bin/env python
# coding: utf-8

import setuptools

requirements = []

setuptools.setup(
    name="yutool",
    version="0.1.0",
    author="Piggy",
    author_email="scnjl@qq.com",
    description="tools for python",
    license="MulanPubL-2.0",
    url="https://github.com/kbrownehs18/yutool",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    python_requires=">=3.6"
)


