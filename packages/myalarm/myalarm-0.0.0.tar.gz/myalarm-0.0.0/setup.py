from setuptools import setup, find_packages
import codecs
import os

VERSION = ''
DESCRIPTION = 'kailash'
LONG_DESCRIPTION = 'A package to perform alarm operations'

# Setting up
setup(
    name="myalarm",
    version=VERSION,
    author="kailash",
    author_email="kailashnakum365@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["datetime" , "playsound"],
    keywords=['set.alarm', 'alarm', 'myalarm', 'python tutorial', 'kailash'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)