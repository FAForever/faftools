from faf.tools import lua

def test_emits_string():
    assert lua.to_lua('python string') == '"python string"'


def test_emits_number():
    assert lua.to_lua(5) == '5'


def test_emits_empty_dictionary():
    assert lua.to_lua({}) == '{}'


def test_emits_dictionary():
    expected = {'some_key': 'some-value', 'other_key': 42}
    for k, v in lua.from_lua('result = ' + lua.to_lua(expected))['result'].items():
        assert expected[k] == v

def test_emits_empty_list():
    data = []
    assert data == list(lua.from_lua('result = ' + lua.to_lua(data))['result'].values())


def test_emits_list():
    data = ['a', 'b', 'c']
    assert data == list(lua.from_lua('result = ' + lua.to_lua(data))['result'].values())


def test_emits_variable_assignment():
    assert lua.to_lua(('var', 'value')) == 'var="value"'
