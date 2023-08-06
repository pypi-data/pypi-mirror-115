import os
import imp

from setuptools import setup, find_packages


version = imp.load_source(
    "ranger_cli.version", os.path.join("ranger_cli", "version.py")).version


setup(
    name="ranger-cli",
    version=version,
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "click>=7.1",
        "six>=1.16",
        "confuse>=1.4",
        "PyYAML>=5.4",
        "requests>=2.25",
        "urllib3>=1.26",
        "xmltodict>=0.12",
        "simplejson>=3.17",
        "rich>=10.2",
        "colorama>=0.4"
    ],
    entry_points={
        "console_scripts": [
            "ranger-cli = ranger_cli.cli:cli"
        ]
    },
    author="Deric Degagne",
    author_email="deric.degagne@gmail.com",
    description="A (unofficial) command-line interface for Apache Ranger public REST API.",
    url="https://github.com/degagne/ranger-cli",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires=">=3.6",
)