__author__ = 'Sheeo'


def to_lua(value):
    lua = []
    if isinstance(value, dict):
        if value == {}:
            return "{}"
        lua.append('{')

        for key,v in value.items():
            lua.append(key + '=' + to_lua(v) + ',')

        lua.append('}')
    elif isinstance(value, list):
        if not value:
            return "{}"
        lua.append('{')

        for v in value:
            lua.append(to_lua(v) + ',')
        lua.append('}')
    elif isinstance(value, tuple):
        key, v = value
        return "".join([key, '=', to_lua(v)])
    elif isinstance(value, str):
        lua.append(''.join(['"', value, '"']))
    else:
        lua.append(repr(value))
    return "".join(lua)