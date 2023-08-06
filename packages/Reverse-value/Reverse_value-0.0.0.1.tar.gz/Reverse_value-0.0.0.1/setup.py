from setuptools import setup, find_packages
import pathlib

VERSION = '0.0.0.1'
DESCRIPTION = 'A Reverse Swap package'
LONG_DESCRIPTION = 'A package that allows to Swap each and every value in a given string with its reverse value.'
HERE=pathlib.Path(__file__).parent
README=(HERE / 'README.md').read_text()
# Setting up
setup(
    name="Reverse_value",
    version=VERSION,
    author="Harshith Raj",
    author_email="<harshith1900@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python',],
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)