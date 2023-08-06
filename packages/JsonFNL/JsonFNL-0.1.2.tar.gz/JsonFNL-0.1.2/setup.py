import sys
from setuptools import setup

extra = {}

setup(
    name='JsonFNL',
    version='0.1.2',
    license='BSD',
    url='https://github.com/dgs3/json_fnl',
    author='Dave Sayles',
    author_email='sayles.dave@gmail.com',
    description='Find and lint json files.',
    long_description="file: README.md",
    long_description_content_type="text/markdown",
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
