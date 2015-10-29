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
        return lua.globals()
except ImportError as e:
    print("Ignoring lupa import error: %s" % e)
    def from_lua(input):
        raise Exception("Can't parse lua code in this environment")
