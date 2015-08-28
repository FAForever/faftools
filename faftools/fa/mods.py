from faf.schema.mod_info import ModInfoSchema
from faftools.lua import from_lua

from pathlib import Path, PurePosixPath

import logging
logger = logging.getLogger(__name__)


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
    :param folder: local path to the mod
    """
    folder = Path(folder)
    schema = ModInfoSchema()
    with (folder / 'mod_info.lua').open() as f:
        lua_table = from_lua(f.read())
    data, errors = schema.load(dict(lua_table))
    if not errors:
        for subdir, vfs_point in data['mountpoints'].items():
            if not (folder / subdir).exists():
                raise KeyError("Mod doesn't contain folder for mountpoint: {}".format(subdir))
            if not PurePosixPath(vfs_point).is_absolute():
                raise ValueError("Mountpoint for {} is relative: {}".format(subdir, vfs_point))
    # TODO: Validate blueprints found using the non existing blueprint compiler


