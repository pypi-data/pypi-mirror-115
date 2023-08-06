#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="substitutionstring", # Replace with your own username
    version="0.2.0",
    author="François Konschelle, Unité IAM, CHU-Bordeaux, France",
    author_email="via.issue@only.please",
    description="Manipulate substitution of string, as for instance deletion and insertion, without loss of information, and allow some algebra of the underneath Substitution object. Can be usefull for any manipulation of string, as version control system, natural language processing, or string comparison in a general sense. The simplest way of using this package is throw the SubstitutionString object, which handles the machinery of the Substitution applied to a given string.",
    license="GNU GENERAL PUBLIC LICENSE v.3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://framagit.org/nlp/substitutionstring",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
    ],
    python_requires='>=3.6',
)


