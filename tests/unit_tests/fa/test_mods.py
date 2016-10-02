import pkg_resources
import pytest
from pathlib import Path

from faf.tools.fa.mods import parse_mod_info, validate_mod_folder

MAP_ZIP = pkg_resources.resource_filename('tests', 'data/example_mod')
MAP_FOLDER = pkg_resources.resource_filename('tests', 'data/example_mod.zip')


@pytest.mark.parametrize("file", [MAP_ZIP, MAP_FOLDER])
def test_parse_mod_info(file):
    mod_info = parse_mod_info(file)
    assert mod_info['name'] == 'Forged Alliance Forever'
    assert mod_info['version'] == 3642
    assert mod_info['_faf_modname'] == 'faf'
    assert mod_info['mountpoints']['env'] == '/env'


def test_validate_mod_folder():
    validate_mod_folder(Path('tests/data/example_mod/'))
