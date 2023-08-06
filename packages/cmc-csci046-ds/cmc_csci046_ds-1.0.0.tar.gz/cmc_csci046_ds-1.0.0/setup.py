import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cmc_csci046_ds",
    version="1.0.0",
    description="Python implementation of common tree-based data structures.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/n8stringham/containers-ds",
    license="BSD3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["containers"],
    include_package_data=True,
    install_requires=["hypothesis", "pytest"],
)

