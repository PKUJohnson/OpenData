# encoding: UTF-8

from setuptools import setup, find_packages
from opendatatools import __version__ as ver
import codecs
import os


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname), 'r', encoding='utf-8').read()


def read_install_requires():
    with codecs.open('requirements.txt', 'r', encoding='utf-8') as f:
        res = f.readlines()
    res = list(map(lambda s: s.replace('\n', ''), res))
    return res

setup(
    # Install data files specified in MANIFEST.in file.
    include_package_data=True,
    #package_data={'': ['*.json', '*.css', '*.html']},
    # Package Information
    name='OpenDataTools',
    url='https://github.com/PKUJohnson/OpenData',
    version=ver,
        license='Apache 2.0',
    # information
    description='Open source data tools.',
    long_description="",
    keywords="data,crawler,free",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
    ],
    # install
    install_requires=read_install_requires(),
    packages=find_packages(),
    # author
    author='PKUJohnson'
)
