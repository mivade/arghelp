from setuptools import setup, find_packages
from arghelp import __version__

with open("README.rst", "r") as readme:
    long_description = readme.read()

setup(
    name="arghelp",
    version=__version__,
    packages=find_packages(include="arghelp"),
    author="Michael V. DePalatis",
    author_email="mike@depalatis.net",
    url="https://github.com/mivade/arghelp",
    license="TBD",
    description="argparse helpers",
    long_description=long_description,
    setup_requires=[
        "pytest-runner",
    ],
    tests_require=[
        "pytest",
        "pytest-cov",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
    ],
)
