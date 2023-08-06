# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# with open("README.md") as f:
#     readme = f.read()

readme = """rigidPy is a library written in python with minimal dependency to compute"""

with open("LICENSE") as f:
    license = f.read()

setup(
    name="rigidpy",
    version="0.0.4",
    description="rigidpy package for rigidity analysis",
    long_description=readme,
    keywords="rigidity physics math python flexibility condensed matter",
    author="Varda Faghir Hagh, Mahdi Sadjadi",
    author_email="vardahagh@uchicago.edu",
    url="https://github.com/vfaghirh/rigidpy",
    license="MIT",
    packages=find_packages(exclude=("docs")),
    python_requires=">=3.5",
    package_data={},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
    ],
)
