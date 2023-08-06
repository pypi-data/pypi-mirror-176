from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A Basic DFA/NFA visual representation'
LONG_DESCRIPTION = 'A package that allows you to easily create DFA/NFA representations'

# Setting up
setup(
    name="DFA_Visualization",
    version=VERSION,
    author="Maggioros Spiros",
    author_email="spirosastro@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
