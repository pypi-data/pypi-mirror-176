from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'It used to generate expected data and validate expected . '
LONG_DESCRIPTION = 'It used to generate expected data and validate expected . Used for mostly in automation purpose '

# Setting up
setup(
    name="debugdata",
    version=VERSION,
    author="Chetan",
    author_email="chetankolhe72@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['data validator', 'expected data generator'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    fullname="Chetan Kolhe",
    url="https://github.com/automation-lib/debugdata"
)
