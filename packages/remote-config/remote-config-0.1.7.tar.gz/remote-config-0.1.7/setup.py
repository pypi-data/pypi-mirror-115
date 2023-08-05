import os
import re

from setuptools import setup, find_packages


PACKAGE = "remote_config"
NAME = "remote-config"
DESCRIPTION = "Remote config and feature toggle based on Consul."
AUTHOR = "Loja Integrada"
AUTHOR_EMAIL = "suporte@lojaintegrada.com.br"
URL = "https://github.com/lojaintegrada/remote-config"
METADATA = dict(
    re.findall("__([a-z]+)__ = \"([^']+)\"", open("{}/__init__.py".format(PACKAGE)).read()))
VERSION = METADATA['version']

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="MIT",
    url=URL,
    packages=find_packages(exclude=['tests']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
    ],
    zip_safe=False,
    tests_require=['pytest','pytest-cov'],
    install_requires=[
        "python-consul==1.1.0",
        "APScheduler==3.7.0",
        "jsonschema==3.2.0"
    ])
