#coding=utf-8
from distutils.core import setup
import setuptools

packages = ['dvd_weather']

setup(
    name = 'dvd_weather-weather',
    version = '1.3',
    author = 'DD',
    author_email = 'd.avid-5@qq.com',
    description = 'look at the py project, it is easy',
    packages = packages,
    package_dir = {'requests': 'requests'}
)