import re
import tempfile

import shutil
from pathlib import Path
from zipfile import ZipFile
import struct

import pkg_resources
from PIL import Image
import os
import math

from werkzeug.utils import secure_filename

from faf.tools.lua import from_lua

# Ratio of resource icon size to map size
RESOURCE_ICON_RATIO = 20.0 / 1024


class MapFile:
    def __init__(self, map_path, validate=True):
        self.map_path = map_path
        self._data = None
        self._dds_image = None
        self._validate = validate

        self._is_zip = map_path.endswith('.zip')

    def _read_save_file(self, file_pointer):
        lua_code = file_pointer.read()
        self._data['save'] = from_lua(lua_code)

    def _read_map(self, fp):
        fp.seek(16)
        self._data['size'] = (
            struct.unpack('f', fp.read(4))[0],
            struct.unpack('f', fp.read(4))[0]
        )
        fp.seek(fp.tell() + 6)
        dds_size = struct.unpack('i', fp.read(4))[0]
        # Skip DDS header
        fp.seek(fp.tell() + 128)

        self._data['dds'] = fp.read(dds_size)

    def _load_mapdata(self):
        if self._is_zip:
            self.load_mapdata_from_zip()
        else:
            self.load_mapdata_from_folder()

    def load_mapdata_from_folder(self):
        if self._validate:
            validate_map_folder(self.map_path, self._validate)

        for path in Path(self.map_path).iterdir():
            filename = path.name
            if filename.endswith('.scmap'):
                with path.open('rb') as fp:
                    self._read_map(fp)

            elif filename.endswith('_save.lua'):
                with path.open('r') as fp:
                    self._read_save_file(fp)

            # TODO the name of the _scenario.lua file should be read from scenario info
            elif filename.endswith('_scenario.lua'):
                with path.open('r') as fp:
                    self.data['scenario'] = read_scenario_file(fp)

    def load_mapdata_from_zip(self):
        if self._validate:
            validate_map_zip_file(self.map_path, self._validate)

        with ZipFile(self.map_path) as zip:
            for member in zip.namelist():
                # TODO the name of the .scmap file should be read from scenario info
                if member.endswith('.scmap'):
                    tmp_dir = tempfile.mkdtemp()
                    try:
                        # TODO use TemporaryDirectory() when no longer bound to Python 2.7
                        zip.extract(member, tmp_dir)
                        with open(os.path.join(tmp_dir, member), 'rb') as fp:
                            self._read_map(fp)
                    finally:
                        shutil.rmtree(tmp_dir)

                # TODO the name of the _save.lua file should be read from scenario info
                elif member.endswith('_save.lua'):
                    with zip.open(member, 'r') as fp:
                        self._read_save_file(fp)

                # TODO the name of the _scenario.lua file should be read from scenario info
                elif member.endswith('_scenario.lua'):
                    with zip.open(member, 'r') as fp:
                        self.data['scenario'] = read_scenario_file(fp)

    @property
    def data(self):
        if self._data is None:
            self._data = {}
            self._load_mapdata()

        return self._data

    def _get_dds_image(self):
        if self._dds_image is None:
            raw = self.data['dds']
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

        map_name = extract_map_name(self.data['scenario'])
        version = self.data['scenario']['ScenarioInfo']['map_version']

        target_path_str = str(target_path)
        if not os.path.exists(target_path_str):
            os.makedirs(target_path_str)

        resized_image.save(os.path.join(target_path_str, generate_preview_file_name(map_name, version)))

    def add_markers(self, target_image, mass_image=None, hydro_image=None, army_image=None):
        markers = self.data['save']['Scenario']['MasterChain']['_MASTERCHAIN_']['Markers']
        for marker_name, marker_data in markers.items():
            if marker_data['resource']:
                if mass_image and marker_data['type'] == 'Mass':
                    self._add_marker(mass_image, marker_data, target_image)
                elif hydro_image and marker_data['type'] == 'Hydrocarbon':
                    self._add_marker(hydro_image, marker_data, target_image)

            elif army_image and marker_data['type'] == 'Blank Marker' and marker_name.startswith("ARMY_"):
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


def generate_preview_file_name(display_name, version):
    return generate_folder_name(display_name, version) + ".png"


def generate_zip_file_name(display_name, version):
    return generate_folder_name(display_name, version) + ".zip"


def generate_folder_name(display_name, version):
    return secure_filename('{}.v{:0>4}'.format(display_name.lower(), version))


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


def generate_zip(zip_file_or_folder, target_dir):
    """
    Generates a FAF conform map ZIP file. This includes:

        1. Generate a folder name based on the map's display name and version
        2. Put all files into that folder
        3. Update the folder names in the *_scenario.lua
        4. Put everything into a ZIP file

    :param zip_file_or_folder: the zip file or folder to parse
    :return: the path to the generated zip file
    """

    path = Path(zip_file_or_folder)

    # TODO use TemporaryDirectory() when no longer bound to Python 2.7
    tmp_dir = tempfile.mkdtemp()
    try:
        if path.is_file():
            validate_map_zip_file(str(path), False)
            with ZipFile(str(path)) as zip:
                zip.extractall(tmp_dir)
        elif path.is_dir():
            shutil.copytree(zip_file_or_folder, os.path.join(tmp_dir, os.path.basename(zip_file_or_folder)))
        else:
            raise ValueError("Not a directory nor a file: " + zip_file_or_folder)

        old_folder_name = os.listdir(tmp_dir)[0]
        map_folder = os.path.join(tmp_dir, old_folder_name)

        map_info = parse_map_info(map_folder, validate=False)
        new_folder_name = generate_folder_name(map_info['display_name'], map_info['version'])

        for file in Path(map_folder).glob('*_scenario.lua'):
            stash_file_path = Path(file.parent, 'stash_scenario.lua.tmp')
            shutil.move(str(file), str(stash_file_path))

            with stash_file_path.open('r') as stash_file:
                with file.open('w') as new_file:
                    for line in stash_file:
                        line = line.replace('/maps/' + map_info['folder_name'], '/maps/' + new_folder_name)
                        new_file.write(line)

        return shutil.make_archive(target_dir + "/" + new_folder_name, 'zip', root_dir=tmp_dir, base_dir=tmp_dir)
    finally:
        shutil.rmtree(tmp_dir)


def parse_map_info(zip_file_or_folder, validate=True):
    """
    Returns a broad description of the map, has the form:
    {
        'version': 6,
        'display_name': 'Core Prime Canyon Fort 12P',
        'name': 'coreprimecanyonfort12P',
        'folder_name': 'coreprimecanyonfort12P.v0006',
        'description': '<LOC coreprimecanyonfort12P.v0006_Description>40x40 12 Player Map',
        'type': 'skirmish',
        'size': (2048, 2048),
        'battle_type': 'FFA',
        'max_players': 12
    }

    :param zip_file_or_folder: the zip file or folder to parse
    :param validate: whether the file should be validated (exceptions will be thrown for invalid/missing values)
    """
    path = Path(zip_file_or_folder)

    lua_data = None
    if path.is_dir():
        validate_map_folder(path, validate)

        for file in path.glob('*_scenario.lua'):
            with file.open() as fp:
                lua_data = read_scenario_file(fp)
            break

    elif path.is_file():
        validate_map_zip_file(str(path), validate)

        with ZipFile(zip_file_or_folder) as zip:
            for member in zip.namelist():
                if member.endswith('_scenario.lua'):
                    with zip.open(member) as file:
                        lua_data = read_scenario_file(file)
                        break
    else:
        raise ValueError("Not a directory nor a file: " + zip_file_or_folder)

    size = lua_data['ScenarioInfo'].get('size')
    map_info = {
        'version': lua_data['ScenarioInfo'].get('map_version'),
        'display_name': _strip(lua_data['ScenarioInfo'].get('name')),
        'name': extract_map_name(lua_data),
        'folder_name': extract_folder_name(lua_data),
        'description': _strip(lua_data['ScenarioInfo'].get('description')),
        'type': _strip(lua_data['ScenarioInfo'].get('type')),
        'size': (size[1], size[2]) if size else None,
        'battle_type': lua_data['ScenarioInfo']['Configurations']['standard']['teams'][1]['name'].strip(),
        'max_players': len(lua_data['ScenarioInfo']['Configurations']['standard']['teams'][1]['armies'])
    }

    return map_info


def _strip(string):
    return string.strip() if string else None


def extract_map_name(lua_data):
    map_name_search = re.search('([^/]+)\.scmap', lua_data['ScenarioInfo']['map'].strip())
    if not map_name_search:
        raise ValueError("Map file is not specified in scenario file")
    map_name = map_name_search.group(1)
    return map_name


def extract_folder_name(lua_data):
    return lua_data['ScenarioInfo']['map'].split('/')[2]


def read_scenario_file(file):
    content = file.read()
    content = content if isinstance(content, str) else content.decode('utf-8')
    return from_lua(content)


def validate_scenario_file(file):
    info = read_scenario_file(file)
    if 'version' not in info:
        raise ValueError("Scenario file is missing version key: {}".format(file))
    if 'ScenarioInfo' not in info:
        raise ValueError("Scenario file does not contain ScenarioInfo: {}".format(file))
    for key in ['name', 'description', 'type', 'size', 'map', 'save', 'script', 'map_version']:
        if key not in info['ScenarioInfo']:
            raise ValueError("ScenarioInfo table missing key {}".format(key))


required_files = {
    '.*\.scmap': lambda f: True,
    '.*_save\.lua': lambda f: True,
    '.*_scenario\.lua': validate_scenario_file,
    '.*_script\.lua': lambda f: True,
}


def validate_map_folder(folder, validate=True):
    path = Path(folder)

    if not path.is_dir():
        raise ValueError("{} not a directory".format(folder))

    folder_files = [file for file in path.iterdir()]
    required_files_found = {}
    for file_pattern, validator in required_files.items():
        for fname in folder_files:
            if re.match(file_pattern, str(fname)):
                if validate:
                    with open(str(fname)) as fp:
                        validator(fp)
                required_files_found[file_pattern] = True

    for file_pattern in required_files:
        if not required_files_found.get(file_pattern):
            raise KeyError("Missing a file of the form {}".format(file_pattern))


def validate_map_zip_file(path, validate=True):
    required_files_found = {}
    with ZipFile(path) as zip:
        if zip.testzip():
            raise ValueError("Corrupted zip file")
        for file in zip.infolist():
            for file_pattern, validator in required_files.items():
                if re.match(file_pattern, str(file.filename)):
                    if validate:
                        validator(zip.open(file))
                    required_files_found[file_pattern] = True

    for file_pattern in required_files:
        if not required_files_found.get(file_pattern):
            raise KeyError("Missing a file of the form {}".format(file_pattern))
