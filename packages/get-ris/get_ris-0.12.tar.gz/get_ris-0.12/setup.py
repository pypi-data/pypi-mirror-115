#-*- encoding: UTF-8 -*-
from setuptools import setup

setup(
    name = "get_ris",          # 包名
    version = "0.12",              # 版本信息
    packages = ['get_ris_pack'],  # 要打包的项目文件夹
    include_package_data=True,    # 自动打包文件夹内所有数据
    zip_safe=True,                # 设定项目包为安全，不用每次都检测其安全性

    install_requires = [          # 安装依赖的其他包
    'requests',
    ],

    # 设置程序的入口为hello
    # 安装后，命令行执行hello相当于调用hello.py中的main方法
    entry_points={
        'console_scripts':[
            'get_ris = get_ris_pack.get_ris:start',
            'get_ris_pdf = get_ris_pack.get_ris:start_pdf'
        ]
     },
    # 如果要上传到PyPI，则添加以下信息
    author = "Felix",
    author_email = "qiyu_sjtu@gmail.com",
    description = "Script to download RIS and import into EndNote"
 )
