# some of these have redundant utilities, change later
import os
import sys
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
# appends child dir to PATH
PRYTHON_SRC_PATH = os.getcwd() + "/prython_src"
sys.path.insert(0, PRYTHON_SRC_PATH) # inserts $(pwd)/prython_src to current path

import prython
from setuptools import setup
# build with $python3 setup.py sdist bdist_wheel
# Package publisher: $pip3 install twine
# Sanity check with $python3 -m twine check dist/*
# Upload to test registry with $python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# Upload to registry with $python3 -m twine upload dist/*
# Local install $ python3 setup.py develop
# This call to setup() does all the work
setup(
    name="prython",
    version=prython.__version__,
    description="Runtime microdebugger for Python, inspire by Ruby's pry gem.",
    long_description=README,
    long_description_content_type="text/markdown",
    url=prython.__main_repo_url__,
    author="Otavio Ehrenberger",
    author_email="ehren.dev.mail@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["prython"],
    include_package_data=False,
    install_requires=["pathlib ; python_version<'3.4'"],
    entry_points={
        "console_scripts": [
            "prython=prython.__main__:main",
        ]
    },
)
