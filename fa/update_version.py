from binascii import *
import struct
import os
import shutil

version = 3640

shutil.copyfile("ForgedAlliance.exe", "ForgedAlliance.%s.exe" % version)

exe = open("ForgedAlliance.exe", 'rb').read()

addr = [0xd3d3f, 0x47612c, 0x476665]

f = open("ForgedAlliance.%s.exe" % version, 'rb+')

for a in addr:
    print hexlify(exe[a+1:a+5])
    v = struct.pack("<L", version)
    print hexlify(v)
    f.seek(a+1, 0)
    f.write(v)

f.close()
