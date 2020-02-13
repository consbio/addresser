import os

from setuptools import setup

import addresser

with open(os.path.join(os.path.dirname(__file__), "README.rst"), "r") as f:
    long_description = f.read()

setup(
    name="addresser",
    description="A Python port of the `parse-address` npm library",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    keywords="address parser normalizer usa us parse-address",
    version=addresser.__version__,
    packages=["addresser"],
    tests_require=["pytest"],
    python_requires=">=3.4",
    url="https://github.com/consbio/addresser",
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
