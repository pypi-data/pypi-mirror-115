#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent


setup(
    name="parselcode",
    version="0.1.3",
    description="Substitution based Cipher to Encrypt/Decrypt by mapping word structure to hindu birth chart houses",
    url="https://github.com/Puru-Malhotra/parselcode",
    author="Puru Malhotra",
    author_email="purumalhotra99@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["parselcode"],
    include_package_data=True,
    install_requires=["pandas","os-sys>=2.1"],
)

