from distutils.core import setup
from setuptools import find_packages

import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="COMCscraper",
    version="0.0.2",
    author="Jared Randall",
    author_email="jaredtroyrandall@gmail.com",
    description="A webscraping package for COMC.com",
    long_description=long_description,
    license = 'MIT',
    long_description_content_type="text/markdown",
    url="https://github.com/jared-randall/COMCscraper",
    project_urls={
        "Bug Tracker": "https://github.com/jared-randall/COMCscraper/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "COMCscraper/src"},
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires = [
    'numpy',
    'pandas',
    'bs4',
    'requests'
]
)



#if __name__ == '__main__':
 #   setup(**setup_args, install_requires=install_requires)