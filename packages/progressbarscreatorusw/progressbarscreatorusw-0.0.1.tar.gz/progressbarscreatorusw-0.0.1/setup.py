
from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Create progress bars in your console'
LONG_DESCRIPTION = 'It is a package that allows you to create progress bars and markers in your console. You can also change the color and the look of the progress bar'

# Setting up
setup(
    name="progressbarscreatorusw",
    version=VERSION,
    author="Dominik Krenn",
    author_email="<i96774080@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['progressbars', 'marker', 'bars'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
