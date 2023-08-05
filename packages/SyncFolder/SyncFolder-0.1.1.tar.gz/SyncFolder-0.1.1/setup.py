# -*- coding: utf-8 -*-
from os.path import dirname, abspath, join, exists

from setuptools import setup, find_packages

long_description = None
if exists("README.rst"):
    with  open("README.rst") as file:
        long_description = file.read()

install_reqs = [req for req in
                open(abspath(join(dirname(__file__), 'requirements.txt')))]

setup(
    name='SyncFolder',
    entry_points={'console_scripts': ['syncfolder=SyncFolder.processor:sync']},
    version="0.1.1",
    description="Python package for synchronizing folders.",
    long_description_content_type="text/x-rst",
    long_description=long_description,
    author='songs18',
    author_email='songhaohao2018@cqu.edu.cn',
    license='MIT',
    packages=find_packages(),
    platforms=['all'],
    url="https://github.com/songs18/SyncFolder",
    zip_safe=False,
    include_package_data=True,
    install_requires=install_reqs,
    python_requires='>=3.3'
)
