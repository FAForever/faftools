try:
    import lupa
    import os

    def from_lua(lua_code):
        """
        Use Lupa as a parser by actually running the code
        :param lua_code: the code to be executed
        :return:
        """

        fa_functions_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fa_functions.lua')

        lua = lupa.LuaRuntime()
        with open(fa_functions_path, 'r') as fp:
            lua.execute(fp.read())

        lua.execute(lua_code)

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
