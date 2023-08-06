from setuptools import setup, find_packages
import codecs
import os
import atexit
import sys


VERSION = '9.0.1'
DESCRIPTION = 'hey'
LONG_DESCRIPTION = 'A package that allows to build simple streams ofvideo, audio and camera data.'

# Setting up
setup(
    name="gitlab-har-recorder",
    version=VERSION,
    author="scythe_abhi",
    author_email="scytheabhi97@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
