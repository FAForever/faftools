from distutils.core import setup
from setuptools import find_packages

from pip.req import parse_requirements

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
    install_requires=[str(r.req) for r in parse_requirements('requirements.txt', session=False)
                                 if r.req is not None],
    include_package_data=True
)
