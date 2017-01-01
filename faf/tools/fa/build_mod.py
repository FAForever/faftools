import subprocess
import logging

from pathlib import Path

from .mods import validate_mod_folder
import os

logger = logging.getLogger(__name__)


def build_mod(mod_folder, mod_info, temp_path):
    """
    Perform deployment of game code (FA repo) on this machine

    :param temp_path: path to temporary folder holding .zips
    :param mod_folder: local path to the mod's git repo
    :param mod_info: Data parsed from the mod_info.lua file
    :return: a list of packed mod dictionaries
    """
    validate_mod_folder(mod_folder)
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
    if not temp_path.exists():
        os.makedirs(str(temp_path))

    for codefolder, mount_point in mod_info['mountpoints'].items():  # Loop over the folders which need mounting
        mount_id = db_ids.get(codefolder.lower(), '0')  # Database id of the folder in question, to be passed on

        # Grab the HEAD commit for later use
        commit = subprocess.check_output(['git',
                                          '-C',
                                          str(mod_folder),
                                          'rev-parse',
                                          'HEAD']).decode().strip()
        logger.info("Using commit: {}".format(commit))

        zip_path = Path(str(temp_path) + "/" + codefolder + '.zip')  # eg; opt/stable/temp/lua.zip
        logger.info('Zip path: {}'.format(zip_path))

        # Build archive
        cmd = ['git', '-C', str(mod_folder), 'archive', '-o', str(zip_path), 'HEAD:' + codefolder + '/', '-9']
        logger.info(repr(cmd))
        subprocess.check_output(cmd)

        md5sum = subprocess.check_output(['md5sum', str(zip_path)]).decode().split(' ')[0].strip()
        modfiles.append({'filename': codefolder,
                         'path': zip_path,
                         'md5': md5sum,
                         'id': mount_id})
    return modfiles

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    build_mod(Path('.'), {}, Path('.'))
