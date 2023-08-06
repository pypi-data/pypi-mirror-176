import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
os.chdir(here)


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="py2cpg",
    version="0.0.6",
    author="ShiftLeft Inc.",
    author_email="claudiu@shiftleft.io",
    description="Placeholder package for ShiftLeft's Python analyzer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
