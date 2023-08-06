from setuptools import setup 
setup(name="ct_module",
version="0.20",
description="This a package for creatring a list of iam user from an environmet",
long_description="",
authors="Kuldip Sahdeo",
packages=['ct_module'],
install_requires=['boto3','datetime','pandas']
)