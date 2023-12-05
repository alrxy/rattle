from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='rattle',
    version='0.1',
    description='rattle',
    url='https://github.com/georgiypetrov/rattle',
    author='xz',
    author_email='',
    license='MIT',
    packages=['rattle'],
    install_requires=required,
    zip_safe=False
)