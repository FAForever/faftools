import re
from pathlib import Path
from zipfile import ZipFile, ZipExtFile
import struct
# Wand seems to crash when using 32-bit env
# https://github.com/dahlia/wand/issues/247
#from wand.image import Image
#from wand.image import Image, COMPOSITE_OPERATORS
from PIL import Image
import subprocess
import os
import math


from faf.tools.lua import from_lua

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

class MapFile:
    preview_sizes = {'small': (100, 100), 'large': (1024, 1024)}
    preview_dir = None

    def __init__(self, map_path):
        self.filepath = map_path
        self.mapname = os.path.splitext(map_path)[0]
        self.preview_dir = os.path.dirname(map_path)
        self._data = None
        self._dds_image = None

    def load_mapdata(self):
        fp = open(self.filepath, 'rb')
        fp.seek(30)
        dds_size = struct.unpack('i', fp.read(4))[0]
        self._data['dds'] = fp.read(dds_size)

    @property
    def data(self):
        if self._data is None:
            self._data = {}
            self.load_mapdata()

        return self._data

    @property
    def dds_path(self):
        return os.path.join(self.preview_dir, '{}.dds'.format(self.mapname))

    def preview_path(self, size):
        return os.path.join(self.preview_dir, '{}.{}.png'.format(self.mapname, size))

    def preview_exists(self, size):
        return os.path.isfile(self.preview_path(size))

    def get_dds_image(self):
        if self._dds_image is None:
            # dds header is 128 bytes
            raw = self.data['dds'][128:]
            dim = int(math.sqrt(len(raw)) / 2)
            # bgra -> rgba
            b, g, r, a = Image.frombuffer('RGBA', (dim, dim), raw, 'raw', 'RGBA', 0, 1).split()
            self._dds_image = Image.merge('RGBA', (r, g, b, a))

        return self._dds_image

    def generate_preview(self, size):
        img = self.get_dds_image()
        preview = img.resize(self.preview_sizes[size])
        preview.save(self.preview_path(size))

    # alternative to Pillow, using ImageMagick command line
    def generate_preview_cmdline(self, size):
        dds_path = self.dds_path

        if not os.path.isfile(dds_path):
            dds_file = open(dds_path, 'wb')
            dds_file.write(self.data['dds'])
            dds_file.close()

        png_path = self.preview_path(size)
        params = ['convert', dds_path, "-resize", 'x'.join(self.preview_sizes[size]), png_path]
        subprocess.check_call(params)

        dds_path = self.dds_path
        if os.path.isfile(dds_path):
            os.remove(dds_path)

    def generate_previews(self):
        for size, _ in self.preview_sizes.items():
            if not self.preview_exists(size):
                self.generate_preview(size)

    def get_previews(self):
        self.generate_previews()

        paths = []
        for size, _ in self.preview_sizes.items():
            paths.append(os.path.abspath(self.preview_path(size)))

        return paths

def generate_map_previews(map_path):
    file = MapFile(map_path)
    file.generate_previews()


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

