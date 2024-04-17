#!/usr/bin/env python
from setuptools import setup
import versioneer

setup(
    version="0.16.4.dev",
    cmdclass=versioneer.get_cmdclass(),
)
