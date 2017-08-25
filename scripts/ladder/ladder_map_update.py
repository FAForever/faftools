#!/usr/bin/python2

import subprocess
import sys

def get_curr_maps():
    query = "docker exec -i stable_faf-db_1 mysql --login-path=faf_lobby faf_lobby -sN -e \"select lm.id, lm.idmap, mv.filename from ladder_map as lm join map_version as mv on lm.idmap = mv.id;\""
    mapstable = subprocess.check_output(
      query,
      shell=True
    )
    ladder_maps = []
    for line in mapstable.split('\n'):
        ladder_maps.append(line.split('\t'))
    return ladder_maps[:-1] # remove empty line

def find_maps(filenames):
    query = "select id, filename from map_version where "
    query = query + ' or '.join(["filename LIKE 'maps/{}.zip'".format(fn) for fn in filenames])
    print(query)
    mapstable = subprocess.check_output(
        "docker exec -i stable_faf-db_1 mysql --login-path=faf_lobby faf_lobby -sN -e \"{}\"".format(query),
        shell=True
    )
    maps = []
    for line in mapstable.split('\n'):
        maps.append(line.split('\t'))
    return maps[:-1]

def make_query(addmaps, outmaps):
    if len(addmaps) > 0:
        add_query = "INSERT INTO ladder_map (idmap) VALUES {};".format(
            ', '.join(['({})'.format(row[0]) for row in addmaps])
        )
        print(add_query)
    else:
        print('no maps to add!')

    if len(outmaps) > 0:
        delete_query = "DELETE FROM ladder_map WHERE {};".format(
            ' OR '.join(['id={}'.format(row[0]) for row in outmaps])
        )
        print(delete_query)
    else:
        print('no maps to delete!')


def print_ladder_maps(maps):
    print("\n".join(["\t".join(row) for row in maps]))

if __name__=='__main__':
    addmaps = []
    outmaps = []
  
    for arg in sys.argv[1:]:
        if arg.startswith('-'):
            outmaps.append(arg[1:])
        elif arg.startswith('+'):
            addmaps.append(arg[1:])
        else:
            print("Erroneous arg")
            sys.exit(1)

    curr_maps = get_curr_maps()
    print(curr_maps)

    if len(addmaps) > 0:
            addmaps = find_maps(addmaps)
    if len(outmaps) > 0:
            outmaps = find_maps(outmaps)

    print("Maps to remove:")
    print("id\tfilename")
    print_ladder_maps(outmaps)

    print("Maps to add:")
    print("id\tfilename")
    print_ladder_maps(addmaps)

    curr_map_ids = [map[1] for map in curr_maps]
    add_map_ids = [map[0] for map in addmaps]
    out_map_ids = [map[0] for map in outmaps]

#    print("Current ladder maps:")
#    print("id\tidmap\tfilename")
#    print_ladder_maps(curr_maps)

    real_addmaps = []
    real_outmaps = []

    new_maps = []
    for row in curr_maps:
        if row[1] not in out_map_ids:
            new_maps.append(['  '] + row)
        else:
            new_maps.append(['--'] + row)
            real_outmaps.append(row)

    for row in addmaps:
        if row[0] not in curr_map_ids:
                new_maps.append(['++','??'] + row)
                real_addmaps.append(row)

    print("New ladder maps:")
    print("diff\tid\tidmap\tfilename")
    print_ladder_maps(new_maps)

    make_query(real_addmaps, real_outmaps)
