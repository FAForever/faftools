import re
from pathlib import Path
from zipfile import ZipFile, ZipExtFile

import struct
from wand.drawing import Drawing

from faf.tools.lua import from_lua
from wand.image import Image, COMPOSITE_OPERATORS

# `id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
# `name` varchar(40) DEFAULT NULL,
# `description` longtext,
# `max_players` decimal(2,0) DEFAULT NULL,
# `map_type` varchar(15) DEFAULT NULL,
# `battle_type` varchar(15) DEFAULT NULL,
# `map_sizeX` decimal(4,0) DEFAULT NULL,
# `map_sizeY` decimal(4,0) DEFAULT NULL,
# `version` decimal(4,0) DEFAULT NULL,
# `filename` varchar(200) DEFAULT NULL,
# `hidden` tinyint(1) NOT NULL DEFAULT '0',
# `mapuid` mediumint(8) unsigned NOT NULL,
# PRIMARY KEY (`id`),
# UNIQUE KEY `Combo` (`name`,`version`),
# UNIQUE KEY `map_filename` (`filename`),
# KEY `mapuid` (`mapuid`)
# ) ENGINE=InnoDB AUTO_INCREMENT=5692 DEFAULT CHARSET=latin1;

def parse_map_info(zip_file_or_folder):
    """
    Returns a broad description of the map, has the form:
    {
        'map_name':
    }
    """
    path = Path(zip_file_or_folder)

    if path.is_dir():
        validate_map_folder(path)
    elif path.is_file():
        validate_map_zip_file(str(path))


def validate_scenario_file(file):
    if isinstance(file, ZipExtFile):
        data = "".join(map(lambda l: l.decode(), file.readlines()))
    else:
        data = "".join(file.readlines())
    info = from_lua(data)
    if 'version' not in info:
        raise ValueError("Scenario file is missing version key: {}".format(file))
    if 'ScenarioInfo' not in info:
        raise ValueError("ScenarioInfo file is missing ScenarioInfo key: {}".format(file))
    for key in ['name', 'description', 'type', 'size', 'map', 'save', 'script']:
        if key not in info['ScenarioInfo']:
            raise ValueError("ScenarioInfo table missing key {}".format(key))


required_files = {
    '.*.scmap': lambda f: True,
    '.*save.lua': lambda f: True,
    '.*scenario.lua': validate_scenario_file,
    '.*script.lua': lambda f: True,
}


def validate_map_folder(folder):
    path = Path(folder)

    if not path.is_dir():
        raise ValueError("{} not a directory".format(folder))

    folder_files = [file for file in path.iterdir()]
    required_files_found = {}
    for file_pattern, validator in required_files.items():
        for fname in folder_files:
            if re.match(file_pattern, str(fname)):
                validator(fname.open())
                required_files_found[file_pattern] = True

    for file_pattern in required_files:
        if not required_files_found.get(file_pattern):
            raise KeyError("Missing a file of the form {}".format(file_pattern))


def validate_map_zip_file(path):
    required_files_found = {}
    with ZipFile(path) as zip:
        if zip.testzip():
            raise ValueError("Corrupted zip file")
        for file in zip.infolist():
            for file_pattern, validator in required_files.items():
                if re.match(file_pattern, str(file.filename)):
                    validator(zip.open(file))
                    required_files_found[file_pattern] = True

    for file_pattern in required_files:
        if not required_files_found.get(file_pattern):
            raise KeyError("Missing a file of the form {}".format(file_pattern))

