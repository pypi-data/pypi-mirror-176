from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Easy DFA/NFA Visualization and much more'

# Setting up
setup(
    name="dfa_visual_demo",
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
