__author__ = 'Sheeo'

from faftools import lua


def test_emits_string():
    assert lua.emit.to_lua('python string') == '"python string"'


def test_emits_number():
    assert lua.emit.to_lua(5) == '5'


def test_emits_dictionary():
    assert lua.emit.to_lua({'some_key':'some-value', 'other-key':42})\
           == '{"some_key"="some-value","other-key"=42}'