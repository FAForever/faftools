import shlex
import subprocess
import logging

from pathlib import Path

from .mods import validate_mod_folder, parse_mod_info

logger = logging.getLogger(__name__)


def build_mod(mod_folder):
    """
    Perform deployment of game code (FA repo) on this machine

    :param mod_folder Path: local path to the mod
    :return: (status: str, description: str)
    """
    validate_mod_folder(mod_folder)
    mod_folder = Path(mod_folder)
    mod_info = parse_mod_info(mod_folder / 'mod_info.lua')
    mod_name, _faf_modname, version = mod_info['name'], mod_info['_faf_modname'], mod_info['version']
    logger.info("Building mod: {}, version {} as {}".format(mod_name, version, _faf_modname))
    db_ids = {
        # Map from directory name -> database ID.
        # We'll get rid of this eventually. I swear
        'effects': 11,
        'env': 12,
        'loc': 13,
        'lua': 14,
        'meshes': 15,
        'modules': 17,
        'projectiles': 18,
        'schook': 19,
        'textures': 20,
        'units': 21,
        'etc': 22
    }
    for mount, vfs_point in mod_info['mountpoints'].items():
        mount = mod_folder / mount
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
        shasum = subprocess.check_output(['tar cf - ' + shlex.quote(str(mount))
                                          + '| shasum'], shell=True).decode().split(' ')[0].strip()
        cache_name = mount.name + "." + shasum + ".zip"
        cache_path = mod_folder / 'build' / cache_name
        if not cache_path.exists():
            # Build archive
            subprocess.check_output(['git', 'archive', shlex.quote(commit), shlex.quote(mount.name), '-o' + str(cache_path), '-9'])
            md5sum = subprocess.check_output(['md5sum', str(cache_path)]).decode().split(' ')[0].strip()
            logger.info("{} was changed, new md5sum: {}".format(mount, md5sum))
        else:
            logger.info("{} (ID: {}) not changed".format(mount.name, db_ids.get(mount.name, 'unknown')))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    build_mod(Path('.'))
