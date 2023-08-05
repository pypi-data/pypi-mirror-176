from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='lc_pytools',#包名
    version='1.1.1',#版本
    description="for easy python",#包简介
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,#是否允许上传资源文件
    author='Linche',#作者
    author_email='2730136863@qq.com',#作者邮件
    maintainer='all',#维护者
    maintainer_email='',#维护者邮件
    license='MIT License',#协议
    url='',#github或者自己的网站地址
    packages=find_packages(),#包的目录
    classifiers=["Programming Language :: Python :: 3",
                 "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
                 "Operating System :: OS Independent", ],#设置编写时的python版本
    python_requires='>=3.5',#设置python版本要求
    install_requires=['itertools'],#安装所需要的库
    entry_points={
        'console_scripts': [
            ''],
    },#设置命令行工具(可不使用就可以注释掉)
    
)