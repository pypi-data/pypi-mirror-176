from distutils.core import setup
from setuptools import find_packages


setup(
    name='duote',  # 对外模块的名字
    version='0.1.9',  # 版本号
    description='测试版本,基本功能',  # 描述
    author='JinxAndLux',  # 作者
    install_requires=['requests'],  # 依赖
    author_email='yby1234@hotmail.com',
    py_modules=['duote*'],  # 要发布的模块
    packages=find_packages(
        # All keyword arguments below are optional:
        where='.',  # '.' by default
        include=['*'],  # ['*'] by default
        exclude=[],  # empty by default
    ),
)
