# In this file we'll import the setuptools that we installed

import setuptools
from pathlib import Path

# Calling a method 'setup()' and passing few keyword arguments
setuptools.setup(
    # 1 - name should be unqiue so it won't conflict with another package at pypi.org
    name="dkpdf",
    # 2 - Version number according to us
    version="1.1",

    # for this we need to pass README.md file
    long_description=Path("README.md").read_text(),

    # Finally, what packages needs to be distributed, here 'dkpdf' is our package, and it has 2 modules
    # we need to tell to setuptools which modules nd packages we need to publish
    # find_packages() automatically fine packages we defined, and exclude the files we mention cause they don't have any source code
    packages=setuptools.find_packages(exclude=["test", "data"])
)
