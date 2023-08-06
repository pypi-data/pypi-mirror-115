from setuptools import find_packages, setup
from multi_validator.version import __version__

setup(
    name='multi_validator',
    packages=find_packages(),
    version=__version__,
    description='This will validate multiple data type, i.e. phone number, email, name, age, weight, etc',
    author='Neel Ratan Guria',
    #install_requires=['mongoengine'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
)
