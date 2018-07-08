from setuptools import setup, find_packages

__version__ = '0.1'

setup(
    name='gpuzlogutils',
    version=__version__,
    author='Ben Wu',
    url='https://github.com/Ben-Wu/gpuz-log-utils',
    packages=find_packages(),
    install_requires=[
        'influxdb==5.1.0'
    ]
)