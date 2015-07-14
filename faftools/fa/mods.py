from marshmallow import Schema, fields
from faftools.lua import from_lua

class ModInfoSchema(Schema):
    name = fields.String(required=True)
    version = fields.Integer(required=True)
    copyright = fields.String()
    description = fields.String()
    author = fields.String()
    url = fields.Url()
    _faf_modname = fields.String()

    source = fields.Url()
    uid = fields.String()
    selectable = fields.Boolean(default=True)
    enabled = fields.Boolean(default=True)
    exclusive = fields.Boolean(default=False)
    ui_only = fields.Boolean(required=True)
    icon = fields.String()
    requires = fields.List(fields.String())
    conflicts = fields.List(fields.String())
    before = fields.List(fields.String())
    after = fields.List(fields.String())


def parse_mod_info(file):
    """
    Parse and validate the given mod_info.lua file, returning a Mod object
    :param file: path to file
    :return: Mod object
    """
    schema = ModInfoSchema()
    with file.open() as f:
        lua_table = from_lua(f.read())
    data, errors = schema.load(dict(lua_table))
    if not errors:
        return data
    else:
        raise ValueError(errors)

