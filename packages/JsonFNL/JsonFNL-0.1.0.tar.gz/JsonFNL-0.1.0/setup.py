import sys
from setuptools import setup

extra = {}

if sys.version_info < (3, 3):
    sys.exit("Sorry, Python < 3.3 is not supported.")

setup(
    name='JsonFNL',
    version='0.1.0',
    license='BSD',
    url='https://github.com/dgs3/json_fnl',
    author='Dave Sayles',
    author_email='sayles.dave@gmail.com',
    description='Discover and lint json files.',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=["json_fnl"],
    **extra
)
