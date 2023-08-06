#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Dawei Zhang
# Mail: dawei-msn@hotmail.com
# Created Time:  2022-11-07 12:07:34 AM
#############################################


from setuptools import setup, find_packages

setup(
    name = "bdlearn",
    version = "0.0.4",
    keywords = ["index","association"],
    description = "big data machine learning",
    long_description = "big data machine learning",
    license = "MIT Licence",

    url = "https://github.com/digbd/najia",
    author = "Dawei Zhang",
    author_email = "dawei-msn@hotmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['pandas','numpy']
)

