#!/usr/bin/python3

"""
  Mod updater script

  This script packs up mod files, writes them to /opt/stable/content/faf/updaterNew/.../, and updates the database.

  Code is mostly self-explanatory - read it from bottom to top.

  Mod information is read from a `patch_info.json` file, check the sample file for its structure.

"""

import subprocess
import shutil
import hashlib
import os
import zipfile
import tempfile
import sys
import json

sys.path.append(os.path.abspath("/opt/stable/faftools/faf/tools"))
from fa import update_version

def read_db(mod):
    """
      Read latest versions and md5's from db
    """
    query = "select uf.fileId, uf.version, uf.name, uf.md5 FROM (select fileId, MAX(version) as version from updates_{mod}_files group by fileId) as maxthings inner join updates_{mod}_files as uf on maxthings.fileId = uf.fileId and maxthings.version = uf.version;".format(mod=mod)
    table = subprocess.check_output(
        "docker exec stable_faf-db_1 mysql --login-path=faf_lobby faf_lobby -sN -e '{}'".format(query),
#            "docker exec -i stable_faf-db_1 mysql -u faf_lobby -pdD9J9zMvdCrLZF5Q faf_lobby -e '{}'".format(query),
#            "docker exec -i stable_faf-db_1 mysql -u root -pZQ9t7nmEcUm3TJv6 faf_lobby -e '{}'".format(query),
        shell=True
    )
    oldfiles = {}
    for line in table.split('\n'):
        if line != '':
            fields = line.split('\t')
            # key = fileId
            oldfiles[int(fields[0])] = {
                'version': fields[1],
                'name': fields[2],
                'md5': fields[3]
            }
    return oldfiles


def update_db(mod, fileId, version, name, md5, dryrun):
    queries = [
        "DELETE FROM updates_{mod}_files WHERE fileId={fileId} AND version={version}".format(mod=mod, fileId=fileId, version=version),
        "INSERT INTO updates_{mod}_files (fileId, version, name, md5, obselete) VALUES ({fileId}, {version}, \"{name}\", \"{md5}\", 0)".format(mod=mod, fileId=fileId, version=version, name=name, md5=md5)
    ]
    for query in queries:
        print("Running " + query)
        if not dryrun:
            subprocess.check_call(
                "docker exec stable_faf-db_1 mysql --login-path=faf_lobby faf_lobby -e '{}'".format(query),
    #            "docker exec -i stable_faf-db_1 mysql -u faf_lobby -pdD9J9zMvdCrLZF5Q faf_lobby -e '{}'".format(query),
    #            "docker exec -i stable_faf-db_1 mysql -u root -pZQ9t7nmEcUm3TJv6 faf_lobby -e '{}'".format(query),
                shell=True
            )

def calc_md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

# FIXME: None of these shell calls are space-in-filenames safe
def create_file(mod, fileId, version, name, source, target_dir, old_md5, dryrun):
    target_dir = target_dir + '/updates_{}_files'.format(mod)
    name = name.format(version)
    target_name = target_dir + '/' + name
    print("Processing {} (fileId {})".format(name, fileId))

    # rename == False is for straight copy of source file
    # rename == True is for moving a compiled file from its temporary location,
    # which also means changing fname
    rename = None
    # list -> zipfile
    if type(source) is list:
        print("Zipping {} -> {}".format(source, target_name))
        # make tempfile
        fo, fname = tempfile.mkstemp('_' + name, 'patcher_')
        zf = zipfile.ZipFile(os.fdopen(fo, 'w'), 'w', zipfile.ZIP_DEFLATED)
        for sm in source:
            zipdir(sm, zf)
        zf.close()
        rename = True
    elif source.endswith('ForgedAlliance.exe'):
        fo, fname = tempfile.mkstemp('_'+ name, 'patcher_')
        fo.close() # Don't need the handle
        update_version.update_exe_version(source, fname, version)
        rename = True
    else:
        rename = False
        fname = source

    checksum = calc_md5(fname)
    print('Compared checksums: Old {} New {}'.format(old_md5, checksum))

    if checksum != old_md5:
        print("Moving tempfile -> {}".format(target_name))
        if not dryrun:
            if rename:
                os.rename(fname, target_name)
            else:
                shutil.copy(fname, target_name)
        elif rename:
            print('Dry run, not moving tempfile. Please delete {}.'.format(fname))
    else:
        print("New {} file is identical to current version - skipping update".format(name))
        if rename:
            if not dryrun:
                os.unlink(fname)
            else:
                print('Dry run, not moving tempfile. Please delete {}.'.format(fname))

    if not dryrun:
        subprocess.call(
            "chgrp www-data {f}; chmod 660 {f}".format(f=target_name),
            shell=True
        )

    update_db(mod, fileId, version, name, checksum, dryrun)

def do_files(mod, version, files, target_dir, dryrun):
    # get old versions
    current_files = read_db(mod)
    for name, fileId, source in files:
        create_file(mod, fileId, version, name, source, target_dir, current_files.get(fileId,{}).get('md5'), dryrun)

if __name__ == '__main__':
    import sys

    args = sys.argv[1:]

    dryrun = False
    version = None
    mod = None
    usage = False
    target_dir = '/opt/stable/content/faf/updaterNew/'
    infofile = 'patch_info.json'
    while len(args) > 0:
        switch = args[0]
        if switch[0] == '-':
            if switch[1:] == 'n':
                dryrun = True
            elif switch[1:] == 'h':
                usage = True
            elif switch[1:] == 't':
                target_dir = args.pop(1)
            elif switch[1:] == 'i':
                infofile = args.pop(1)
            elif switch[1:] == 'm':
                mod = args.pop(1)
            else:
                print('Unknown commandline switch {}'.format(switch))
                usage=True
                break
        else:
            try:
                version = int(switch)
            except:
                print('Please pass a number for patch version')
                usage=True
                break
        args.pop(0)

    if usage:
        print("""
        Forged Alliance Forever featured mod patch compiler

        This script takes information about an FAF featured mod and updates it.

        Usage:

        make_patch.py <patch> [switches]

        Switches:
        -h\tPrint usage information
        -t DIR\tTarget dir for update files`
        -i INFOFILE\tPatch info file
        -n\tDry run (do not modify 'content' or db)
        -f\tFull update (do not skip mod files that have same hash in last version)
        """)
        sys.exit(1)

#    # target filename / fileId in updates_{mod}_files table / source files with version placeholder
#    # if source files is single string, file is copied directly
#    # if source files is a list, files are zipped
#    files = [
#        ('init_nomads.v{}.lua', 6, 'init_nomads.lua'),
#        ('nomads_movies.v{}.nmd', 9, ['movies']),
#        ('effects.v{}.nmd', 10, ['effects']),
#        ('env.v{}.nmd', 11, ['env']),
#        ('loc.v{}.nmd', 12, ['loc']),
#        ('lua.v{}.nmd', 13, ['lua']),
#        ('nomadhook.v{}.nmd', 14, ['nomadhook']),
#        ('nomads.v{}.nmd', 15, ['nomads']),
#        ('projectiles.v{}.nmd', 16, ['projectiles']),
#        ('sounds.v{}.nmd', 17, ['sounds']),
#        ('units.v{}.nmd', 18, ['units']),
#        ('textures.v{}.nmd', 19, ['textures']),
#    ]

    with open(infofile) as fp:
        info = json.load(fp)
        mod is None:
            mod = info['mod']
        if version is None:
            version = info['version']
        files = info['files']

    if mod is None or version is None:
        print('Please pass mod name and version either via commandline or in info file.')
        sys.exit(1)

    do_files(mod, version, files, target_dir, dryrun)
