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
    install_requires=['docopt==0.6.2',
                      'lupa==1.4',
                      'marshmallow==2.13.1',
                      'marshmallow-jsonapi==0.15.1',
                      'pathlib==1.0.1',
                      'requests==2.18.4',
                      'pytest-cov==2.5.1',
                      'pytest-mock==1.6.2',
                      'werkzeug==0.12.2'],
    include_package_data=True
)
