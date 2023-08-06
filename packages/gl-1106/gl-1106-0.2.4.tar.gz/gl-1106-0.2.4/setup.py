# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="gl-1106",  #
    version="0.2.4",
    description="hw2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://google.com/", # toto change to github page
    author="GuansLi",
    author_email="example@email.com", #
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["get_data"],  # todo: main folder
    include_package_data=True,
    install_requires=["numpy",
                      "polygon-api-client",
                      "sqlalchemy",
                      "matplotlib",
                      "pandas"]
)

# 1. install build tools
# pip install wheel twine

# 2. build the library
# python setup.py sdist bdist_wheel

# 3. check build results
# twine check dist/*                    --->  PASSED ???

# 4. upload the library to pypi
# twine upload dist/*

# https://pypi.org/project/gl-1106/0.2.4/


# upload code to github

# https://github.com/gl2392/gl-1106.git

