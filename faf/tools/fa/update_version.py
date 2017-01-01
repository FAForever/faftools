"""
Updates the version in the binary executable of the Forged Alliance game. Will write a new ForgedAlliance.version.exe
file.

Usage:
   update_version <version> [--file=<file>] [--dest=<dest>]

Options:
   --file=<file>   The binary file to update [default: ForgedAlliance.exe]
   --dest=<dest>   The folder path where to create the patched filed [default: .]
"""
import os
import struct
import shutil
import logging

from docopt import docopt

logger = logging.getLogger(__name__)

def update_exe_version(source, destination, version):
    """
    :param source: Path to the static base copy of ForgedAlliance.exe - Hardcoded in API
    :param destination: Path this update is being copied to
    :param version: New mod version
    :return:
    """

    # os.path.join due to Python 2.7 compatibility
    destination = os.path.join(str(destination), "ForgedAlliance.%s.exe" % version)
    shutil.copyfile(str(source), str(destination))

    addr = [0xd3d3f, 0x47612c, 0x476665]
    f = open(str(destination), 'rb+')

    for a in addr:
        v = struct.pack("<L", int(version))
        f.seek(a+1, 0)
        f.write(v)
    f.close()
    logger.info("Saved ForgedAlliance.%s.exe" % version)
    return f

if __name__ == '__main__':
    arguments = docopt(__doc__)
    source, destination, version = arguments.get('--file'), arguments.get('--dest'), arguments.get('<version>')
    update_exe_version(source, destination, version)
