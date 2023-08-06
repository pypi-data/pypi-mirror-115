#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: LiangjunFeng
# Mail: zhumavip@163.com
# Created Time:  2018-4-16 19:17:34
#############################################

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "nnff",      #这里是pip项目发布的名称
    version = "0.2",  #版本号，数值大的会优先被pip
    keywords = ["pip", "nnff","framework"],
    description = "An neutral network file framwork.",
    long_description = "An neutral network file framwork.",
    license = "MIT Licence",
    url = "https://github.com/lzfshub/nnfileframe.git",     #项目相关文件地址，一般是github
    author = "LiuZhifei",
    author_email = "lzfsmail@gmail.com",
    packages = find_packages(),
    include_package_data = True,
    entry_points={'console_scripts': ['nnff=nnff.nnff:main']},
    platforms = "win",
    install_requires = [""]          #这个项目需要的第三方库
)

