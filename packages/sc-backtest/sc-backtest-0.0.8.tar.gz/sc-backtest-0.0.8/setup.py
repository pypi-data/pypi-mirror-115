# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 13:24:03 2021

@author: chang.sun
"""

import setuptools

filepath = 'README.md'
 
setuptools.setup(
    # 项目的名称
    name="sc-backtest",
    #项目的版本
    version="0.0.8",
    # 项目的作者
    author="chang.sun",
    # 作者的邮箱
    author_email="ynsfsc@126.com",
    # 项目描述
    description="Index future simple stat and time-series backtest module",
    # 长描述
    long_description=open(filepath, encoding='utf-8').read(),
    # 以哪种文本格式显示长描述
    long_description_content_type="text/markdown",  # 所需要的依赖 
    install_requires=["pandas >= 1.2.4", "numpy >= 1.1", "ta >= 0.7.0"],  # 比如["flask>=0.10"]
    # 项目主页
    url="https://pypi.org/project/sc-backtest/",
    # 项目中包含的子包，find_packages() 是自动发现根目录中的所有的子包。
    packages=setuptools.find_packages(),
    # 其他信息，这里写了使用 Python3，MIT License许可证，不依赖操作系统。
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7"
)