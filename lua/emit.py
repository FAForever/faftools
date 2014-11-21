__author__ = 'Sheeo'


def to_lua(value):
    lua = []
    if isinstance(value, dict):
        if value == {}:
            return "{}"
        lua.append('{')
        items = value.items()
        for k, v in items[:len(items)-1]:
            lua.append(''.join([k, '=', to_lua(v), ',']))
        k, v = items[len(items)-1]
        lua.append(''.join([k, '=', to_lua(v)]))
        lua.append('}')
    elif isinstance(value, list):
        if not value:
            return "{}"
        lua.append('{')
        for k in value[:len(value)-1]:
            lua.append(''.join([to_lua(k), ',']))
        k = value[len(value)-1]
        lua.append(''.join([to_lua(k)]))
        lua.append('}')
    elif isinstance(value, tuple):
        k, v = value
        return "".join([k, '=', to_lua(v)])
    elif isinstance(value, str):
        lua.append(''.join(['"', value, '"']))
    else:
        lua.append(repr(value))
    return "".join(lua)