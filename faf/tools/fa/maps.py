import re
from pathlib import Path
from zipfile import ZipFile, ZipExtFile
import struct

import pkg_resources
from PIL import Image
import os
import math

from faf.tools.lua import from_lua

# Ratio of resource icon size to map size
RESOURCE_ICON_RATIO = 0.01953125
MAX_MAP_FILE_SIZE = 256 * 1024 * 1024


class MapFile:
    def __init__(self, map_path):
        self.map_path = map_path
        self.mapname = os.path.splitext(os.path.basename(map_path))[0]
        self._data = None
        self._dds_image = None

        self._is_zip = map_path.endswith('.zip')

    def _read_save_file(self, file_pointer):
        lua_code = file_pointer.read()
        self._data['save'] = from_lua(lua_code)

    def _read_map(self, content):
        dds_size = struct.unpack('i', content[30:34])[0]
        self._data['size'] = (
            struct.unpack('f', content[16:20])[0],
            struct.unpack('f', content[20:24])[0]
        )
        self._data['dds'] = content[34:35 + dds_size]

    def _load_mapdata(self):
        if self._is_zip:
            validate_map_zip_file(self.map_path)

            with ZipFile(self.map_path) as zip:
                for member in zip.namelist():
                    filename = os.path.basename(member)
                    if filename.endswith('.scmap'):
                        if zip.getinfo(member).file_size > MAX_MAP_FILE_SIZE:
                            raise ValueError('Map is too big, max size is {} bytes'.format(MAX_MAP_FILE_SIZE))

                        self._read_map(zip.read(member))

                    elif filename.endswith('_save.lua'):
                        with zip.open(member, 'r') as fp:
                            self._read_save_file(fp)

        else:
            validate_map_folder(self.map_path)

            for path in Path(self.map_path).iterdir():
                filename = path.name
                if filename.endswith('.scmap'):
                    with open(str(path), 'rb') as fp:
                        self._read_map(fp.read())

                elif filename.endswith('_save.lua'):
                    with open(str(path), 'r') as fp:
                        self._read_save_file(fp)

    @property
    def data(self):
        if self._data is None:
            self._data = {}
            self._load_mapdata()

        return self._data

    def _get_dds_image(self):
        if self._dds_image is None:
            # dds header is 128 bytes
            raw = self.data['dds'][128:]
            dim = int(math.sqrt(len(raw)) / 2)
            # bgra -> rgba
            b, g, r, a = Image.frombuffer('RGBA', (dim, dim), raw, 'raw', 'RGBA', 0, 1).split()
            self._dds_image = Image.merge('RGBA', (r, g, b, a))

        return self._dds_image

    def generate_preview(self, size, target_path, mass_icon=None, hydro_icon=None, army_icon=None):
        map_image = self._get_dds_image()
        resized_image = map_image.resize((size, size))

        hydro_image = Image.open(hydro_icon).resize((int(size * RESOURCE_ICON_RATIO), int(
            size * RESOURCE_ICON_RATIO))) if hydro_icon else None

        mass_image = Image.open(mass_icon).resize((int(size * RESOURCE_ICON_RATIO), int(
            size * RESOURCE_ICON_RATIO))) if mass_icon else None

        army_image = Image.open(army_icon).resize((int(size * RESOURCE_ICON_RATIO), int(
            size * RESOURCE_ICON_RATIO))) if army_icon else None

        self.add_markers(resized_image, mass_image, hydro_image, army_image)

        resized_image.save(os.path.join(str(target_path), '{}.png'.format(self.mapname)))

    def add_markers(self, target_image, mass_image=None, hydro_image=None, army_image=None):
        markers = self.data['save']['Scenario']['MasterChain']['_MASTERCHAIN_']['Markers']
        for marker_name, marker_data in markers.items():
            if marker_data['resource']:
                if mass_image and marker_data['type'] == 'Mass':
                    self._add_marker(mass_image, marker_data, target_image)
                elif hydro_image and marker_data['type'] == 'Hydrocarbon':
                    self._add_marker(hydro_image, marker_data, target_image)

            elif army_image and marker_data['type'] == 'Blank Marker':
                self._add_marker(army_image, marker_data, target_image)

    def _add_marker(self, marker_image, marker_data, target_image):
        x = marker_data['position'][1]
        y = marker_data['position'][3]
        width = self.data['size'][0]
        height = self.data['size'][1]

        self._paint_on_image(marker_image, x / width, y / height, target_image)

    @staticmethod
    def _paint_on_image(image, x, y, target_image):
        offset_x = int(x * target_image.width - image.width / 2)
        offset_y = int(y * target_image.height - image.height / 2)

        if offset_x < image.width / 2:
            offset_x = int(image.width / 2)
        elif offset_x >= target_image.width - image.width:
            offset_x = int(target_image.width - image.width)

        if offset_y < image.height / 2:
            offset_y = int(image.height / 2)
        elif offset_y >= target_image.height - image.height:
            offset_y = int(target_image.height - image.height)

        r, g, b, a = image.split()
        top = Image.merge("RGB", (r, g, b))
        mask = Image.merge("L", (a,))
        target_image.paste(top, (offset_x, offset_y), mask)


def generate_map_previews(map_path, sizes_to_paths, mass_icon=None, hydro_icon=None, army_icon=None):
    """

    :param map_path: Path to the map file (.scmap) to generate the previews for
    :param sizes_to_paths: a dictionary that maps preview sizes (in pixels) to the directory in which the preview image should be generated in. Eg: {100: '/previews/small', 1024: '/previews/large'}
    :param hydro_icon: the path to the hydro marker image
    :param mass_icon: the path to the mass marker image
    :param army_icon: the path to the army marker image
    :return:
    """

    markers_dir = pkg_resources.resource_filename('static', 'map_markers')
    mass_icon = mass_icon if mass_icon else os.path.join(markers_dir, 'mass.png')
    hydro_icon = hydro_icon if hydro_icon else os.path.join(markers_dir, 'hydro.png')
    army_icon = army_icon if army_icon else os.path.join(markers_dir, 'army.png')

    file = MapFile(map_path)
    for size, path in sizes_to_paths.items():
        file.generate_preview(size, path, mass_icon, hydro_icon, army_icon)


# FIXME this has not been finished
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
    '.*\.scmap': lambda f: True,
    '.*_save\.lua': lambda f: True,
    '.*_scenario\.lua': validate_scenario_file,
    '.*_script\.lua': lambda f: True,
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
