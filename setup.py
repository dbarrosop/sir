import uuid
from setuptools import setup, find_packages
from pip.req import parse_requirements

version = '0.15-0'

install_reqs = parse_requirements('requirements.txt', session=uuid.uuid1())
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='SIR',
    version=version,
    packages=find_packages(),
    description='SDN Internet Router',
    long_description=open('README.md').read(),
    author='David Barroso',
    author_email='dbarrosop@dravetech.com',
    license='Apache License, Version 2.0',
    url='https://github.com/dbarrosop/sir',
    install_requires=reqs,
    include_package_data=True,
    zip_safe=False,
)
