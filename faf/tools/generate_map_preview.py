"""
Generates map preview files for a specified map. The files are generated into subdirectories of <target_dir>.

Usage:
   generate_map_preview <map_zip_or_folder> <target_dir>

Options:
   --file=<file>   The binary file to update [default: ForgedAlliance.exe]
"""
import os

from docopt import docopt

from faf.tools.fa.maps import generate_map_previews

if __name__ == '__main__':
    arguments = docopt(__doc__)
    map_zip_or_folder = arguments.get('<map_zip_or_folder>')
    target_dir = arguments.get('<target_dir>')

    generate_map_previews(map_zip_or_folder, {
        128: os.path.join(target_dir, 'small'),
        512: os.path.join(target_dir, 'large')
    })

    print("Previews generated for: %s".format(map_zip_or_folder))
