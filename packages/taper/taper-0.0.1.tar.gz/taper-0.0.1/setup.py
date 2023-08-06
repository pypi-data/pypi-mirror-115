#!/usr/bin/env python3

from setuptools import find_packages, setup

version = "0.0.1"

long_description = "Contains some data"

setup(
    name="taper",
    packages=find_packages(exclude=[]),
    version=version,
    description=("Contains some data"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="The Taper Authors",
    author_email="limsweekiat@gmail.com",
    url="https://github.com/greentfrapp/aglioolio",
    license="Apache License 2.0",
    keywords=[
        "pytorch",
    ],
    install_requires=["torch>=1.5.0", "numpy", "requests", "tqdm", "dill", "pandas"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
