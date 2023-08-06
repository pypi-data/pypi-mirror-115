# -*- coding: UTF-8 -*-
import os
 
import setuptools
 
setuptools.setup(
    name="package_test_czh",
    version="00.01.05",
    keywords="demo",
    description="A demo for python packaging.",
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            "README.md"
        )
    ).read(),
	long_description_content_type="text/markdown",
    author="chenzhihao2",      # 替换为你的Pypi官网账户名
    author_email="1040791159@qq.com",  # 替换为你Pypi账户名绑定的邮箱
    packages=setuptools.find_packages(),
    license="MIT",
	
	install_requires=[
        'protobuf',
    ]
)