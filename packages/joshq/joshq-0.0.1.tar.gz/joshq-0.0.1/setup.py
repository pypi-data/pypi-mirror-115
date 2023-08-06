from setuptools import setup, find_packages
import io
import os

NAME = "joshq"
DESCRIPTION = "Joshq is a package that checks for f-strings inside log statements"
EMAIL = "michael.karotsieris@gmail.com"
AUTHOR = "Michael Karotsieris, William Cragg"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.0.1"
REQUIRED = [
]

here = os.path.abspath(os.path.dirname(__file__))


try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Michael Karotsieri, William Cragg",
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(exclude=["test*"]),
    install_requires=REQUIRED,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ],
    setup_requires=["wheel"],
)