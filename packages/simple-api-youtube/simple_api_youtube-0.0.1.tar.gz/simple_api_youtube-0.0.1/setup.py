from setuptools import setup, find_packages
import os

VERSION = '0.0.1'
DESCRIPTION = 'basic youtube api.'

# Setting up
setup(
    name="simple_api_youtube",
    version=VERSION,
    author="Real72",
    author_email="real4ik.games@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['google-api-python-client','loguru'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)