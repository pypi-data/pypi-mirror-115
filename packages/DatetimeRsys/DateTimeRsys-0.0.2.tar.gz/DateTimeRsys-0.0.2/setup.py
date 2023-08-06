from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Python Library for DATE TIME finder from a String'
LONG_DESCRIPTION = 'This Library is the improved version of DATE TIME finder or matchers Libraries, Basically it will extract the date and time from a string which is having any kind of date time within the string it will return the dictionary which contains the date time.'

# Setting up
setup(
    name="DateTimeRsys",
    version=VERSION,
    author="Praveen Kumar Srivas",
    author_email="pks101295nit2017@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['regex','datefinder'],
    keywords=['date time','datetime'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)