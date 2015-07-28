import uuid
from setuptools import setup, find_packages
from pip.req import parse_requirements

version = '0.9'

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
    # Uncomment lines below when building RPM for EOS
    # data_files=[
    #     ('/etc/nginx/external_conf', ['deployment_files/eos/conf/sir_nginx.conf']),
    #     ('/etc/uwsgi', ['deployment_files/eos/conf/sir_nginx.conf']),
    #     ('/etc/uwsgi', ['deployment_files/eos/conf/sir_nginx.conf']),
    #     ('/usr/bin', ['deployment_files/eos/bin/pmacct']),
    #     ('/usr/sbin', ['deployment_files/eos/sbin/sfacctd']),
    #     ('/lib', ['deployment_files/eos/lib/libjansson.so.4']),
    #     ('/mnt/drive/sir/pmacct/etc/', ['deployment_files/eos/conf/pmacct.conf']),
    # ]
)
