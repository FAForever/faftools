from faftools.fa.mods import parse_mod_info

from pathlib import Path

def test_parse_mod_info():
    test_file = Path('tests/data/faf_mod_info.lua')
    mod_info = parse_mod_info(test_file)
    assert mod_info['name'] == 'Forged Alliance Forever'
    assert mod_info['_faf_modname'] == 'faf'
