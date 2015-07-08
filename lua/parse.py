try:
    import lupa

    def from_lua(input: str):
        """
        Use Lupa as a parser by actually running the code
        :param input:
        :return:
        """
        lua = lupa.LuaRuntime()
        lua.execute(input)
        return lua.globals()
except ImportError:
    # TODO: Have a fallback parser
    pass
