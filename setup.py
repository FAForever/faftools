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
    install_requires=['docopt', 'pathlib', 'marshmallow', 'marshmallow_jsonapi'],
    package_data={'': ['faf/tools/lua/fa_functions.lua', 'faf/tools/fa/map_icons/*.png']},
    include_package_data=True
)
