from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A library with package'
LONG_DESCRIPTION = 'file: README.md'
# Setting up
setup(
    name="taskpackagelib",
    version=VERSION,
    author="ThMeyerNeu",
    author_email="<egor767680@gmial.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)
