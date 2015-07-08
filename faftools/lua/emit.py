def to_lua(value):
    """
    Convert arbitrary python types to a serialized lua string
    :param value:
    :return:
    """
    lua = []
    if isinstance(value, dict):
        if value == {}:
            return "{}"
        lua.append('{')
        items = value.items()
        for k, v in items:
            lua.append(''.join([k, '=', to_lua(v), ',']))
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
