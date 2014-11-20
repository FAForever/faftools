__author__ = 'Sheeo'


def to_lua(value):
    lua = []
    if isinstance(value, dict):
        lua.append('{')
        items = value.items()
        for k, v in items[:len(items)-1]:
            lua.append(''.join([to_lua(k), '=', to_lua(v), ',']))
        k, v = items[len(items)-1]
        lua.append(''.join([to_lua(k), '=', to_lua(v)]))
        lua.append('}')
    elif isinstance(value, str):
        lua.append(''.join(['"', value, '"']))
    else:
        lua.append(repr(value))
    return "".join(lua)