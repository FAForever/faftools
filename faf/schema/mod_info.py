from marshmallow import Schema, fields


class ModInfoSchema(Schema):
    """
    Represents data from a mod_info.lua file.
    """

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
    ui_only = fields.Boolean(default=False)
    icon = fields.String(default='mod_icon.dds')
    requires = fields.List(fields.String())
    conflicts = fields.Dict()
    before = fields.List(fields.String())
    after = fields.List(fields.String())
    mountpoints = fields.Dict()
