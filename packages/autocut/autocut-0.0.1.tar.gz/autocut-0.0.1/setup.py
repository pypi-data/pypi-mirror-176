import sys
from setuptools import setup

message = 'autocut has no pypi release. Please install it by `pip install git+https://github.com/mli/autocut.git`'

argv = lambda x: x in sys.argv

if (argv('install') or  # pip install ..
        (argv('--dist-dir') and argv('bdist_egg'))):  # easy_install
    raise Exception(message)

if argv('bdist_wheel'):  # modern pip install
    raise Exception(message)

setup(
    name='autocut',
    version='0.0.1',
    description=message,
    license='Apache 2.0',
)


