try:
    import lupa

    def from_lua(input):
        """
        Use Lupa as a parser by actually running the code
        :param input:
        :return:
        """
        lua = lupa.LuaRuntime()
        lua.execute(input)

        def unfold_table(t, seen=None):
            result = {}
            for k, v in t.items():
                if not lupa.lua_type(v):  # Already a python type
                    result[k] = v
                elif lupa.lua_type(v) == 'table':
                    result[k] = dict(v)
            return result
        return unfold_table(lua.globals())
except ImportError as e:
    print("Ignoring lupa import error: %s" % e)
    lupa = None

    def from_lua(input):
        raise Exception("Can't parse lua code in this environment")
