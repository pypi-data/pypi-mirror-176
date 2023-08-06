#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Team 11
"""
import setuptools
setuptools.setup(
    name="dtree_id3", 
    author="Team 11",
    description="ID3 is a Machine Learning Decision Tree Classification Algorithm.",
    long_description="ID3 is a Machine Learning Decision Tree Classification Algorithm.",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)