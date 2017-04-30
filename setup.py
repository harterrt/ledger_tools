from setuptools import find_packages, setup

dependencies = ['click', 'PyFunctional', 'pick']

setup(
    name='ledgertools',
    version='0.1',
    author='Ryan Harter (:harterrt)',
    author_email='harterrt@gmail.com',
    packages=find_packages(exclude=['tests']),
    install_requires=dependencies,
)
