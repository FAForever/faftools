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
    :return: a list of packed mod dictionaries
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
    modfiles = []
    for mount, vfs_point in mod_info['mountpoints'].items():
        mount_id = db_ids.get(mount.lower(), '0')
        mount_path = mod_folder / mount
        logger.info("Mountpoint: {}, path: {}, id: {}".format(mount, mount_path, mount_id))
        commit = subprocess.check_output(['git',
                                          '-C',
                                          str(mount_path),
                                          'rev-parse',
                                          'HEAD']).decode().strip()
        logger.info("Using commit: {}".format(commit))
        shasum = subprocess.check_output(['tar cf - ' + shlex.quote(str(mount_path))
                                          + '| shasum'], shell=True).decode().split(' ')[0].strip()
        logger.info("Current shasum: {}".format(shasum))
        cache_name = mount_path.name + "." + shasum + ".zip"
        cache_path = mod_folder / 'build' / cache_name
        logger.info("Cache path: {}".format(cache_path))
        if not cache_path.exists():
            # Build archive
            subprocess.check_output(['git',
                                     '-C',
                                     str(mount_path),
                                     'archive', shlex.quote(commit),
                                     shlex.quote(mount),
                                     '-o' + str(cache_path), '-9'])
            logger.info("{} was changed, rebuilding".format(mount_path, shasum))
        else:
            logger.info("{} (ID: {}) not changed".format(mount_path.name, mount_id))

        md5sum = subprocess.check_output(['md5sum', str(cache_path)]).decode().split(' ')[0].strip()
        modfiles.append({'filename': mount_path.name,
                         'path': cache_path,
                         'md5': md5sum,
                         'sha1': shasum,
                         'id': mount_id})
    return modfiles

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    build_mod(Path('.'))
