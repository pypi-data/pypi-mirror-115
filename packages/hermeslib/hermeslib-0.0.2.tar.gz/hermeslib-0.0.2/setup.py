# -*- coding: utf-8 -*-
# ----------------------------------------------------------------
# @Time        : 2021/7/21 11:24
# @Author      : keheng
# @Version     ：python 3.6.8
# @File        : setup.py
# @Description :
# ----------------------------------------------------------------
# @Change Activity:
#         2021/7/21 : create new
# ----------------------------------------------------------------

from setuptools import setup, find_packages, find_namespace_packages

setup(
    name="hermeslib",
    version="0.0.2",
    keywords=("pip", "hermes", "valkyrie", "vantage", "keheng"),
    description="The support lib of hermes instrument",
    long_description="The support lib of hermes instrument",
    license="MIT Licence",

    url="https://github.com/keh123000/hermeslib",
    author="keheng",
    author_email="26467568@qq.com",

    packages=find_namespace_packages(include=["hermeslib", "hermeslib.*"], ),
    include_package_data=True,
    platforms="any",
    install_requires=['pyyaml', 'configparser']
)

# 1.  python setup.py bdist_wheel

# 2.  python setup.py check
#     python setup.py build
#     python setup.py sdist


#  twine upload dist/*
