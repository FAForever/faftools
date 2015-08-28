from marshmallow import Schema, fields
from faf.schema.fields import ListField, MapField


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
    requires = ListField(fields.String())
    conflicts = ListField(fields.String())
    before = ListField(fields.String())
    after = ListField(fields.String())
    mountpoints = MapField(fields.String(), fields.String())
