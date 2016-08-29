"""
Updates the version in the binary executable of the Forged Alliance game. Will write a new ForgedAlliance.version.exe file.

Usage:
   update_version <version> [--file=<file>]

Options:
   --file=<file>   The binary file to update [default: ForgedAlliance.exe]
"""
import struct
import shutil
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__)
    file, version = arguments.get('--file'), arguments.get('<version>')
    shutil.copyfile(file, "ForgedAlliance.%s.exe" % version)

    addr = [0xd3d3f, 0x47612c, 0x476665]
    f = open("ForgedAlliance.%s.exe" % version, 'rb+')

    for a in addr:
        v = struct.pack("<L", int(version))
        f.seek(a+1, 0)
        f.write(v)
    f.close()
    print("Saved ForgedAlliance.%s.exe".format(version))
