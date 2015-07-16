from marshmallow import Schema, fields
from faftools.lua import from_lua

from pathlib import Path, PurePosixPath

class MapField(fields.Field):
    def __init__(self, from_cls, to_cls, **kwargs):
        super(MapField, self).__init__(**kwargs)
        self.from_cls = from_cls
        self.to_cls = to_cls

    def _serialize(self, value, attr, obj):
        return {self.from_cls.serialize(k, attr, obj):
                self.to_cls.serialize(v, attr, obj) for k, v in value.items()}

    def _deserialize(self, value):
        return {self.from_cls.deserialize(k):
                self.to_cls.deserialize(v) for k, v in dict(value).items()}

class ListField(fields.Field):
    def __init__(self, inner_cls, **kwargs):
        super(ListField, self).__init__(**kwargs)
        self.inner_cls = inner_cls

    def _serialize(self, value, attr, obj):
        return [self.inner_cls.serialize(val, attr, obj) for val in value]

    def _deserialize(self, value):
        return [self.inner_cls.deserialize(val) for val in value]

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
    ui_only = fields.Boolean(default=False)
    icon = fields.String(default='mod_icon.dds')
    requires = ListField(fields.String())
    conflicts = ListField(fields.String())
    before = ListField(fields.String())
    after = ListField(fields.String())
    mountpoints = MapField(fields.String(), fields.String())


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

def validate_mod_folder(folder):
    """
    Validate the mod found in folder
    :param folder:
    :return: True
    """
    schema = ModInfoSchema()
    with Path(folder, 'mod_info.lua').open() as f:
        lua_table = from_lua(f.read())
    data, errors = schema.load(dict(lua_table))
    if not errors:
        for subdir, vfs_point in data['mountpoints'].items():
            if not Path(folder, subdir).exists():
                raise KeyError("Mod doesn't contain folder for mountpoint: {}".format(subdir))
            if not PurePosixPath(vfs_point).is_absolute():
                raise ValueError("Mountpoint for {} is relative: {}".format(subdir, vfs_point))
    # TODO: Validate blueprints found using the non existing blueprint compiler

