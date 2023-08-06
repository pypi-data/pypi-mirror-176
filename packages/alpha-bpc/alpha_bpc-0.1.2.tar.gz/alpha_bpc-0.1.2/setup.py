#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.read().splitlines()


test_requirements = []

setup(
    author="Amir Arfan",
    author_email="amir.inaamullah.arfan@nmbu.no",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
    ],
    description="Python package for the Binary Patch Convolution framework",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="alpha_bpc",
    name="alpha_bpc",
    packages=find_packages(include=["alpha_bpc", "alpha_bpc.*", "examples"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/amirarfan/alpha_bpc",
    version="0.1.2",
    zip_safe=False,
)
