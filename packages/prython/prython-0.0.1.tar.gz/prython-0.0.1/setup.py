import constants

from setuptools import setup
# build with $python3 setup.py sdist bdist_wheel
# Package publisher: $pip3 install twine
# Sanity check with $python3 -m twine check dist/*

# This call to setup() does all the work
setup(
    name="prython",
    version=constants.PRYTHON_VERSION,
    description="Runtime microdebugger for Python, inspire by Ruby's pry gem.",
    long_description=constants.README,
    long_description_content_type="text/markdown",
    url=constants.GITHUB_REPO_URL,
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
    #install_requires=["feedparser", "html2text"],
    entry_points={
        "console_scripts": [
            "prython=prython.__main__:main",
        ]
    },
)
