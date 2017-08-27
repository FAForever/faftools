#!/usr/bin/python3

"""
Synchronize content file with db

Reads map, mod and featured-mod information from db and ensures all content files
needed are present, pulling them from the prod server if necessary
"""

import subprocess
import requests
import shutil
import sys
import os

CONTENT_BASE = 'http://content.faforever.com/faf/'
FILE_BASE = '/opt/stable/content/faf/'

def query_db(query):
    table = subprocess.check_output(
        "docker exec stable_faf-db_1 mysql --login-path=faf_lobby faf_lobby -sN -e '{}'".format(query),
        shell=True
    )
    ret = []
    for line in table.split(b'\n')[:-1]:
        ret.append(line.split(b'\t'))
    return ret

def download_file(src, dst):
    print('Downloading {} -> {}'.format(src, dst))
    r = requests.get(src, stream=True)
    if r.status_code == 200:
        with open(dst, 'wb') as f:
            for chunk in r.iter_content(1024*1024):
                sys.stderr.write('.')
                sys.stderr.flush()
                f.write(chunk)
        print('\nDownload done')
        return True
    else:
        print('Error {}: {}'.format(r.status_code, r.reason))
        return False

def mode_file(path):
    shutil.chown(path, 'www-data', 'faforever')
    os.chmod(path, 0o664)

def sync_featured_mods():
    get_mods_query = "SELECT gamemod FROM game_featuredMods WHERE publish = 1"
    mods = [mod[0].decode() for mod in query_db(get_mods_query)]
    print("Founds mods: {}".format(mods))
    for mod in mods:
        files_query = "SELECT name FROM updates_{}_files".format(mod)
        filenames = [row[0].decode() for row in query_db(files_query)]
        for filename in filenames:
            path = 'updaterNew/updates_{}_files/{}'.format(mod, filename)
            url = CONTENT_BASE + path
            dest = FILE_BASE + path
            if os.path.isfile(dest):
                print('{} exists, skipping'.format(dest))
            else:
                if download_file(url, dest):
                    mode_file(dest)

def sync_maps():
    get_maps_query = "SELECT filename FROM map_version WHERE hidden = 0"
    maps = [m[0].decode() for m in query_db(get_maps_query)]
    for m in maps:
        path = 'vault/{}'.format(m)
        url = CONTENT_BASE + path
        dest = FILE_BASE + path
        if os.path.isfile(dest):
            print('{} exists, skipping'.format(dest))
        else:
            if download_file(url, dest):
                mode_file(dest)

def sync_mods():
    get_mods_query = "SELECT filename FROM mod_version WHERE hidden = 0"
    mods = [m[0].decode() for m in query_db(get_mods_query)]
    for m in mods:
        path = 'vault/{}'.format(m)
        url = CONTENT_BASE + path
        dest = FILE_BASE + path
        if os.path.isfile(dest):
            print('{} exists, skipping'.format(dest))
        else:
            if download_file(url, dest):
                mode_file(dest)


if __name__ == "__main__":
    sync_featured_mods()
    sync_mods()
    sync_maps()
