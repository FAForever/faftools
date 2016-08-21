import tempfile
from zipfile import ZipFile


import pkg_resources
import pytest
import shutil
from PIL import Image

from faf.tools.fa.maps import generate_map_previews, parse_map_info, generate_zip
import os

HYDRO_ICON = pkg_resources.resource_filename('static', 'map_markers/hydro.png')
MASS_ICON = pkg_resources.resource_filename('static', 'map_markers/mass.png')
ARMY_ICON = pkg_resources.resource_filename('static', 'map_markers/army.png')
MAP_ZIP = pkg_resources.resource_filename('tests', 'data/maps/random_map.zip')
MAP_FOLDER = pkg_resources.resource_filename('tests', 'data/maps/theta passage 5.v0001')


@pytest.mark.parametrize("hydro_icon", [HYDRO_ICON, None])
@pytest.mark.parametrize("mass_icon", [MASS_ICON, None])
@pytest.mark.parametrize("army_icon", [ARMY_ICON, None])
def test_generate_map_previews(tmpdir, mass_icon, hydro_icon, army_icon):
    small_previews_dir = tmpdir.mkdir("small_previews")
    large_previews_dir = tmpdir.mkdir("large_previews")

    generate_map_previews(MAP_ZIP, {128: small_previews_dir, 1024: large_previews_dir}, mass_icon, hydro_icon,
                          army_icon)

    small_files = small_previews_dir.listdir()
    large_files = large_previews_dir.listdir()

    assert len(small_files) == 1
    assert len(large_files) == 1

    with Image.open(small_files[0].strpath) as im:
        assert im.size == (128, 128)
    with Image.open(large_files[0].strpath) as im:
        assert im.size == (1024, 1024)


@pytest.mark.parametrize("hydro_icon", [HYDRO_ICON, None])
@pytest.mark.parametrize("mass_icon", [MASS_ICON, None])
@pytest.mark.parametrize("army_icon", [ARMY_ICON, None])
def test_generate_map_previews_from_folder(tmpdir, mass_icon, hydro_icon, army_icon):
    small_previews_dir = tmpdir.mkdir("small_previews")
    large_previews_dir = tmpdir.mkdir("large_previews")
    unpack_dir = tmpdir.mkdir("unpacked_map")

    with ZipFile(MAP_ZIP) as zip:
        zip.extractall(unpack_dir.strpath)

    map_folder = os.path.join(unpack_dir.strpath, unpack_dir.listdir()[0].strpath)

    generate_map_previews(map_folder, {128: small_previews_dir, 1024: large_previews_dir}, mass_icon, hydro_icon,
                          army_icon)

    small_files = small_previews_dir.listdir()
    large_files = large_previews_dir.listdir()

    assert len(small_files) == 1
    assert len(large_files) == 1

    with Image.open(small_files[0].strpath) as im:
        assert im.size == (128, 128)
    with Image.open(large_files[0].strpath) as im:
        assert im.size == (1024, 1024)


@pytest.mark.parametrize("file", [MAP_ZIP])
def test_parse_map_info(file):
    map_info = parse_map_info(file)

    assert map_info['version'] == 1
    assert map_info['display_name'] == 'Theta Passage 5'
    assert map_info['name'] == 'theta_passage_5'
    assert map_info['description'] == 'Balanced Version of Theta Passage 2. Now the Reclaim is equal at the top/' \
                                      'bottom and at the left/right side at the middle. Also there are no longer ' \
                                      'any stones hidden inside a Hill.'
    assert map_info['type'] == 'skirmish'
    assert map_info['battle_type'] == 'FFA'
    assert map_info['size'] == (256, 256)
    assert map_info['max_players'] == 4


def test_parse_map_info_folder():
    tmp_dir = tempfile.mkdtemp()
    try:
        # TODO use TemporaryDirectory() when no longer bound to Python 2.7
        with ZipFile(MAP_ZIP) as zip:
            zip.extractall(tmp_dir)

        test_parse_map_info(os.path.join(tmp_dir, 'theta_passage_5.v0001'))
    finally:
        shutil.rmtree(tmp_dir)


@pytest.mark.parametrize("file", [MAP_ZIP, MAP_FOLDER])
def test_generate_zip(file):
    # TODO use TemporaryDirectory() when no longer bound to Python 2.7
    tmp_dir = tempfile.mkdtemp()
    try:
        generate_zip(file, tmp_dir)

        assert os.path.isfile(tmp_dir + '/theta_passage_5.v0001.zip')
    finally:
        shutil.rmtree(tmp_dir)
