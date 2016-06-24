from zipfile import ZipFile

from pathlib import Path

import pytest
from PIL import Image

from faf.tools.fa.maps import generate_map_previews
import os

HYDRO_ICON = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../../faf/tools/fa/map_icons/hydro.png')
MASS_ICON = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../../faf/tools/fa/map_icons/mass.png')
ARMY_ICON = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../../faf/tools/fa/map_icons/army.png')
MAP_ZIP = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../data/maps/theta_passage_5.v0001.zip')


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
