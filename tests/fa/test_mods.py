from faftools.fa.mods import parse_mod_info, validate_mod_folder

from pathlib import Path

def test_parse_mod_info():
    test_file = Path('tests/data/example_mod/mod_info.lua')
    mod_info = parse_mod_info(test_file)
    assert mod_info['name'] == 'Forged Alliance Forever'
    assert mod_info['version'] == 3642
    assert mod_info['_faf_modname'] == 'faf'

def test_validate_mod_folder():
    validate_mod_folder(Path('tests/data/example_mod/'))
