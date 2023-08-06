from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.4'
DESCRIPTION = 'To create/merge 2D or 3D patches.'
LONG_DESCRIPTION = 'This package performs two tasks: 1. generates patches, and 2. marge patches.'

# Setting up
setup(
    name="jenti",
    version=VERSION,
    author="Mrinal Kanti Dhar",
    author_email="<mrinal054@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    license="MIT",
    url="https://github.com/mrinal054/patch_and_merge",
    packages=find_packages(),
    install_requires=[''],
    keywords=['python', 'patch', 'merge'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)