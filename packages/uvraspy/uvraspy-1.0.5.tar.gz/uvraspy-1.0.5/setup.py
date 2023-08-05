from setuptools import setup, find_packages
import codecs
import os
from setuptools.command.install import install


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    os.system("sudo apt install bluetooth libbluetooth-dev")

    # TODO: create service for the program
    # to start the program on boot


here = os.path.abspath(os.path.dirname(__file__))

long_description = 'A Python package for Raspberry Pi'

with codecs.open(os.path.join(here, "../README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.5'
DESCRIPTION = 'A Python package for Raspberry Pi'


def requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()


# Setting up
setup(
    name="uvraspy",
    version=VERSION,
    author="csM5-22-25",
    author_email="n.aukes@student.utwente.nl",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(include=['uvraspy', 'uvraspy.*']),
    install_requires=requirements(),
    keywords=['python', 'RasPy', 'uvedora', 'pihat', 'fedora', ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ],
    entry_points={
        'console_scripts': ['uvraspy=uvraspy.main:main'],
    }
)


# TODO: add more setup stuff
