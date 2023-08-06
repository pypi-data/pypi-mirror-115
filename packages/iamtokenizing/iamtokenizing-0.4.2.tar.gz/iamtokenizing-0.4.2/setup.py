#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as file:
    long_description_ = file.read()
    
with open('requirements.txt', 'r') as file:
    requirements_ = [line.strip() for line in file.readlines()
                     if not line.startswith('#')]
    
setuptools.setup(
    name="iamtokenizing",
    version="0.4.2",
    author="François Konschelle - IAM CHU Bordeaux France",
    author_email="no_email@please.org",
    description="Simple tokenizers: n-grams and chargrams splitting, white space splitting, or splitting using configurable REGEX expression. Based on Span objects from the tokenspan package.",
    long_description=long_description_,
    long_description_content_type="text/markdown",
    license="GNU GENERAL PUBLIC LICENSE v.3",
    url="https://framagit.org/nlp/iamtokenizing/",
    packages=setuptools.find_packages(),
    install_requires = requirements_,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
    ],
    python_requires='>=3.7',
)
