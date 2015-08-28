from distutils.core import setup
from setuptools import find_packages

setup(
    name='faftools',
    version='0.1',
    url='http://www.faforever.com',
    packages=['faf'] + find_packages(),
    license='GPLv3',
    author='Michael Sondergaard',
    author_email='sheeo@sheeo.dk',
    description='faftools project',
    requires=['lupa', 'docopt', 'pathlib', 'marshmallow']
)
