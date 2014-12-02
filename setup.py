from setuptools import setup, find_packages
from pip.req import parse_requirements


# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt')

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='sir',
    version='0.01',
    py_modules=['sir'],
    packages = find_packages(),
    install_requires=reqs,
    entry_points='''
        [console_scripts]
        sir=sir:cli
    ''',
    include_package_data=True,
)