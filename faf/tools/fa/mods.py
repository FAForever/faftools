# coding=utf-8
import os
from zipfile import ZipFile

from pathlib import Path, PurePosixPath
import logging

from werkzeug.utils import secure_filename

from faf.schema import ModInfoSchema
from faf.tools.lua import from_lua

logger = logging.getLogger(__name__)


def parse_mod_info(zip_file_or_folder):
    """
    Returns a broad description of the mod, has the form:
    {
        'display_name': 'All factions',
        'uid': '24a0c2f6-59b6-489e-a899-6cd342b2a0a9',
        'version': 2,
        'copyright': 'Copyright © 2008, Legion Darrath',
        'author': 'Legion Darrath',
        'ui_only': false,
        'description': 'Spawns the ACU\'s of all factions. You need to turn on prebuild units for this mod to work.',
    }

    :param zip_file_or_folder: the zip file or folder to parse
    """
    path = Path(zip_file_or_folder)

    lua_data = None
    if path.is_dir():
        for file in path.glob('mod_info.lua'):
            with file.open() as fp:
                lua_data = read_mod_info(fp)
            break

    elif path.is_file():
        with ZipFile(zip_file_or_folder) as zip:
            for member in zip.namelist():
                if os.path.basename(member) == 'mod_info.lua':
                    with zip.open(member) as file:
                        lua_data = read_mod_info(file)
                        break
    else:
        raise ValueError("Not a directory nor a file: " + str(zip_file_or_folder))

    data, errors = ModInfoSchema().load(dict(lua_data))
    if errors:
        raise ValueError(errors)

    return data


def read_mod_info(file):
    content = file.read()
    content = content if isinstance(content, str) else content.decode('utf-8')
    return from_lua(content)


def generate_thumbnail_file_name(display_name, version):
    return generate_folder_name(display_name, version) + ".png"


def generate_zip_file_name(display_name, version):
    return generate_folder_name(display_name, version) + ".zip"


def generate_folder_name(display_name, version):
    return '{}.v{:0>4}'.format(generate_file_name(display_name), version)


def generate_file_name(display_name):
    return secure_filename('{}'.format(display_name.lower()))


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
