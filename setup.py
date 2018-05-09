from distutils.core import setup
from setuptools import find_packages

setup(
    name='faftools',
    version='0.1',
    url='http://www.faforever.com',
    packages=['faf'] + find_packages(),
    license='GPLv3',
    author='Michael Sondergaard',
    author_email='sheeo@faforever.com',
    description='faftools project',
    requires=['lupa'],
    install_requires=['docopt',
                      'lupa',
                      'marshmallow==2.13.1',
                      'marshmallow-jsonapi',
                      'pathlib',
                      'requests',
                      'pytest-cov',
                      'pytest-mock',
                      'werkzeug'],
    include_package_data=True
)
