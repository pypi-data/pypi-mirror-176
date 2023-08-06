from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.1'
DESCRIPTION = 'Unified API for compartmental modeling'
LONG_DESCRIPTION = 'A package that allows creation/editing/sharing of compartmental models as well as a web application front end to interact with code.'

# Setting up
setup(
    name="compartmentsPlus",
    version=VERSION,
    author="ThreeStrings",
    author_email="<zack@ouhermans.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['streamlit', 'openpyxl', 'pandas', 'matplotlib'],
    keywords=['python', 'compartment', 'modeling', 'epidemiology', 'networks'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)