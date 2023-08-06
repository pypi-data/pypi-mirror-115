#!/usr/bin/env python
# coding: utf-8

import setuptools 

setuptools.setup(
    name='testangle', # 项目的名称,pip3 install get-time
    version='1.0.4', # 项目版本 
    author='xww', # 项目作者 
    author_email='axiaowwa@163.com', # 作者email 
    url='https://github.com/1abner1/tianshou', # 项目代码仓库
    description='撰写一个简单的列子', # 项目描述 
    packages=setuptools.find_packages(), # 包名 
    install_requires=['pillow','tensorboard','torch'],
    classifiers =[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)

