# Featured Mod patch creation script

## Featured Mod structure

Featured mods consist of files that are downloaded either to `bin` or `gamedata`. Featured mod releases ("patches") are numbered sequentially. A full patchset at version `n` consists of all files that belong to the mod at the highest available version that is `<= n`.

There are two tables in the db for every featured mod, `updates_<mod>` and `updated_<mod>_files`. The first one notes the filename and the path for the file. The second one has information about specific versions.

There is also a content server that serves the files referenced in the db.

Database example, for the nomads mod:

```
mysql> select * from updates_nomads;
+----+-------------------+----------+
| id | filename          | path     |
+----+-------------------+----------+
|  6 | init_nomads.lua   | bin      |
|  9 | nomads_movies.nmd | gamedata |
| 10 | effects.nmd       | gamedata |
| 11 | env.nmd           | gamedata |
| 12 | loc.nmd           | gamedata |
| 13 | lua.nmd           | gamedata |
| 14 | nomadhook.nmd     | gamedata |
| 15 | nomads.nmd        | gamedata |
| 16 | projectiles.nmd   | gamedata |
| 17 | sounds.nmd        | gamedata |
| 18 | units.nmd         | gamedata |
| 19 | textures.nmd      | gamedata |
+----+-------------------+----------+
12 rows in set (0.00 sec)

mysql> describe updates_nomads_files;
+----------+----------------------+------+-----+---------+----------------+
| Field    | Type                 | Null | Key | Default | Extra          |
+----------+----------------------+------+-----+---------+----------------+
| id       | int(10) unsigned     | NO   | PRI | NULL    | auto_increment |
| fileId   | smallint(5) unsigned | NO   | MUL | NULL    |                |
| version  | int(11)              | NO   |     | NULL    |                |
| name     | varchar(45)          | NO   |     | NULL    |                |
| md5      | varchar(45)          | NO   |     | NULL    |                |
| obselete | tinyint(1)           | NO   |     | 0       |                |
+----------+----------------------+------+-----+---------+----------------+
6 rows in set (0.00 sec)

```

The query to get the current patchset is a handful:

```
mysql> select uf.* FROM (select fileId, MAX(version) as version from updates_nomads_files group by fileId) as maxthings inner join updates_nomads_files as uf on maxthings.fileId = uf.fileId and maxthings.version = uf.version;
+-----+--------+---------+-----------------------+----------------------------------+----------+
| id  | fileId | version | name                  | md5                              | obselete |
+-----+--------+---------+-----------------------+----------------------------------+----------+
| 127 |      6 |      61 | init_nomads.v61.lua   | c3f3ca8e9f1245114ca9f23ae471f8a7 |        0 |
|  69 |      7 |      61 | nomads.v61.nmd        | 3b9a59ce008f8565b52782f9848b47a5 |        0 |
|  14 |      8 |       2 | fafnomads.nmd         | 6a9b9dc8afbdd10f7c53a85680e538e1 |        0 |
|  70 |      9 |      61 | nomads_movies.v61.nmd | 886615203eb636bc5ff0092a3cd9a3ba |        0 |
| 128 |     10 |      61 | effects.v61.nmd       | b7050be45228a1aceda8ee6e59c191d8 |        0 |
| 129 |     11 |      61 | env.v61.nmd           | 0a655f032da8466851a6382c4471d02c |        0 |
| 130 |     12 |      61 | loc.v61.nmd           | 38f350b346d0621ccd97be8d87654694 |        0 |
| 131 |     13 |      61 | lua.v61.nmd           | 0925ea1a650efd93be96cc3f63cab4a0 |        0 |
| 132 |     14 |      61 | nomadhook.v61.nmd     | 40173a237850ec5fcd43d1233c053e9c |        0 |
| 133 |     15 |      61 | nomads.v61.nmd        | f6ced953ac7ffbd634ebb07609d7a6f7 |        0 |
| 134 |     16 |      61 | projectiles.v61.nmd   | 845a48fd9519008bc7eefc529930676d |        0 |
| 135 |     17 |      61 | sounds.v61.nmd        | 0b4a9b5204f97de377647b6766fba200 |        0 |
| 136 |     18 |      61 | units.v61.nmd         | acbea859d1e59e7a1f5a36e702704519 |        0 |
| 137 |     19 |      61 | textures.v61.nmd      | b2ff198d454166f65ad9bcbecf2d61ea |        0 |
+-----+--------+---------+-----------------------+----------------------------------+----------+
14 rows in set (0.01 sec)

```

To create a new patchset, the following things need to be done:

1. Create the new files
2. Compare new files with old files by checking md5sum
3. Add files that changed to the db and copy them to the content server

## Patch Info

The `patch_info.json` file is necessary to tell the patch creation script (`make_patch.py`) which source files go into which pack.

The structure is as follows:

* mod: Defines which mod - put null there to require mod name being passed to `make_patch.py` on the commandline in case of mods that are deployed with multiple versions
* version: mod version
* files: List of filesets
    * target filename, with `{}` placeholder for patch version
    * file id for the file, corresponding to the `updates_<mod>` table
    * source file - can be a single string, which means file is copied as-is, or a list of files and folders, which are zipped together

Example:

```
{
    "mod": "nomads",
    "files": [
        ["init_nomads.v{}.lua", 6, "init_nomads.lua"],
        ["nomads_movies.v{}.nmd", 9, ["movies"]],
        ["effects.v{}.nmd", 10, ["effects"]],
        ["env.v{}.nmd", 11, ["env"]],
        ["loc.v{}.nmd", 12, ["loc"]],
        ["lua.v{}.nmd", 13, ["lua"]],
        ["nomadhook.v{}.nmd", 14, ["nomadhook"]],
        ["nomads.v{}.nmd", 15, ["nomads"]],
        ["projectiles.v{}.nmd", 16, ["projectiles"]],
        ["sounds.v{}.nmd", 17, ["sounds"]],
        ["units.v{}.nmd", 18, ["units"]],
        ["textures.v{}.nmd", 19, ["textures"]]
    ]
}
```

## Patch Creation Script

The `make_patch.py` script is your one-stop shop to create a new patchset.

**Important**: Run it with the cwd (current directory) set to the source repository of the mod you want to package.

The script executes the following steps:

* Parse arguments (run `make_patch.py -h` to get a list of accepted arguments)
* Read the `patch_info.json` file
* Get the current version of the mod files with their md5sums from the db
* Make new mod files
* For all mod files with a different md5sum, put the file in the content server directory and update the db
