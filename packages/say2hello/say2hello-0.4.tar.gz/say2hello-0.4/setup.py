#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2021/8/7 17:05
# @Author  : JiangWenKe
# @Site    : 
# @File    : setup.py
# @Software: PyCharm

from setuptools import setup, find_packages

setup(
    name="say2hello",
    version="0.4",
    license="MIT Licence",

    url="https://github.com/wenkejiang/say2hello",
    author="jiangwenke",
    author_email="jiangwenke@yeah.net",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[]
)

