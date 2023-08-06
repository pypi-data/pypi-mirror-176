from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.0'
DESCRIPTION = 'less typing'

# Setting up
setup(
    name="libraarby",
    version=VERSION,
    author="mishalol",
    author_email="misha5335758@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)