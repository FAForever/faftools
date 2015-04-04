#!/usr/bin/env python
import sys
import struct
import binascii
import string
import argparse
import zlib
from curses import ascii


# expects tshark on stdin as in:
# tshark -r game.pcap -R 'ip.addr==192.168.0.101' -T fields -d udp.port==6112,echo -e ip.src -e udp.srcport -e ip.dst -e udp.dstport -e frame.time_relative -e echo.data | python FAPacket.py -e -p
# any non-FA packets will crash the parser

# running:
# FAPacket.py [ -p ] [ -e ]
# -p print command stream packets
# -e print encapsulation packets

def hexdump_hash(data):
    res = ''
    for i in range(0, len(data)):
        res += '{0:02x}'.format(ord(data[i]))
    return res

def hexdump(data, indent):
    res = ''
    for i in range(0, len(data), 16):
        if i:
            for k in range(0, indent):
                res += ' '
        for j in range(i, min(i + 16, len(data))):
            res += '{0:02x} '.format(ord(data[j]))
        for k in range(min(i + 16, len(data)), i + 16):
            res += '   '
        for j in range(i, min(i + 16, len(data))):
            if ascii.isprint(data[j]):
                res += data[j]
            else:
                res += '.'
        res += '\n'
    return res

class FAPacket:
    def __init__(self, data):
        self.type = ord(data[0])
        self.len  = ord(data[1]) | ord(data[2]) << 8;
        self.data = data[3:]
        d = {}
        d[0] = 1
        d[0x32] = 1
        d[0x33] = 1
        d[0x34] = 1
        d[1] = 1
        d[3] = 1
        self.decodable = d
        
    def is_advance(self):
        return self.type == 0
    def is_ack(self):
        return self.type == 0x32
    def is_set_cmdsrc(self):
        return self.type == 1
    def cmdsrc(self):
        return ord(self.data[0])


    def ack_cmdsource(self):
        return ord(self.data[0])
    def pp_data(self, indent):
        return hexdump(self.data, indent)
    def can_decode(self):
        return self.type in self.decodable
    def simtick(self):
        if self.type == 0x32:
            return struct.unpack("<bL", self.data)[1]
        if self.type == 0x33 or self.type == 0x34 or self.type == 0:
            return struct.unpack("<L", self.data)[0]
    def decode(self):
        if self.type == 0:
            return "ADV {0}".format(struct.unpack("<L", self.data)[0])
        elif self.type == 0x32:
            return "ACK {0} {1}".format(self.ack_cmdsource(), self.simtick())
        elif self.type == 0x33:
            return "SIM {0}".format(struct.unpack("<L", self.data)[0])
        elif self.type == 0x34:
            return "FIN {0}".format(struct.unpack("<L", self.data)[0])
        elif self.type == 1:
            return "CMDSOURCE {0}".format(ord(self.data[0]))
        elif self.type == 3:
            (h, s) = struct.unpack("<16sL", self.data)
            return "HASH {0} {1}".format(s, hexdump_hash(h))
        else:
            return "(error)"
        
class FAEncap(object):
    def __init__(self, src, srcport, dst, dstport, time, packet):
        self.offset = 0
        self.src = src
        self.dst = dst
        self.srcport = srcport
        self.dstport = dstport
        self.time = time
        if ord(packet[0]) == 8:
            self.type = 8
            self.data = packet[1:]
            self.len = len(packet) - 1
        elif ord(packet[0]) == 0:
            self.type = 0
            self.data = packet[1:]
            self.len = len(packet) - 1
        elif ord(packet[0]) == 255:
            self.type=255
            self.data=''
            self.len = len(packet) - 1
        else:
            (self.type, self.mask, self.seq, self.ack, self.seq2, self.ack2, self.len) = struct.unpack("<bLHHHHH", packet[0:15])
            self.data = packet[15:]

    def src_full(self):
        return src + ":" + srcport
    def dst_full(self):
        return dst + ":" + dstport
    def connection(self):
        return self.src_full() + "->" + self.dst_full()
    def pp_data(self, indent):
        if self.type == 8:
            return self.data
        else:
            return hexdump(self.data, indent)
    def packets(self):
        ret = []
        while True:
            p = self.next_packet()
            if p == None:
                return ret
            ret.append(p)
    def next_packet(self):
        if self.type != 4:
            return None
        if self.offset + 3 > len(self.data):
            return None
        len_ = ord(self.data[self.offset + 1]) | ord(self.data[self.offset + 2]) << 8
        if self.offset + len_ > len(self.data):
            return None
        offset = self.offset;
        self.offset += len_
        if offset == self.offset:
            sys.stdout.write("waarg {0} {1} {2}".format(offset, self.offset, binascii.hexlify(self.data)))
        return FAPacket(self.data[offset: self.offset])
    def prepend_remaining(self, r):
        self.data = str(r) + str(self.data)
    def remaining(self):
        if self.type == 4:
            return self.data[self.offset:]
        return ''

class FAPeerState(object):
    def __init__(self):
        self.addr_to_cmdsrc = {}
        self.cmdsrc_to_addr = []
        self.simtick = []
        self.ack_simtick = []
    def process_egress(self, addr, packet):
        if packet.is_set_cmdsrc():
            self.cmdsource = packet.cmdsrc()
        if packet.is_advance():
            self.simtick[self.addr_to_cmdsrc[addr]] += packet.simtick()
        elif packet.is_ack():
            s1 = self.addr_to_cmdsrc[addr]
            s2 = packet.ack_cmdsource()
            self.ack_simtick[s1][s2] = packet.simtick()
    def process_ingress(self, addr, packet):
        if packet.is_set_cmdsrc():
            s = packet.cmdsrc()
            self.addr_to_cmdsrc[addr] = s
            while len(self.cmdsrc_to_addr) <= s:
                self.cmdsrc_to_addr.append('')
                self.simtick.append(0)
                self.ack_simtick.append(0)
            self.cmdsrc_to_addr[s] = addr

            

argp = argparse.ArgumentParser(prog = "PROG")
argp.add_argument("-e", action="store_true")
argp.add_argument("-t", action="store_true")
argp.add_argument("-p", action="store_true")

args = argp.parse_args()

remain = {}
inflate = {}
inflate_remain = {}

cmdpackets_seen = {}

future = {}

c32 = [0, 0, 0]
c33 = 0
c34 = 0
tick = 0

seq_seen = {}

for line in sys.stdin:
    (src, srcport, dst, dstport, time, data) = line.split();
    #print "*{0}*{1}*{2}*{3}*{4}*{5}".format(src, srcport, dst, dstport, time, data);
    e = FAEncap(src, srcport, dst, dstport, time, binascii.unhexlify(data.translate(None, ':')))

    if not e.connection() in seq_seen:
        seq_seen[e.connection()] = {}
    if not e.connection() in remain:
        remain[e.connection()] = ''
    if not e.connection() in future:
        future[e.connection()] = {}

    s = '{0} {1} type={2} len={3: 4d}'.format(e.time, e.connection(), e.type, e.len)
    if e.type != 4:
        print s
        if e.len:
            print ' ' * 7, hexdump(e.data, 8)
    elif e.type == 4:
        if e.seq2 in seq_seen[e.connection()]:
            continue

        if len(seq_seen[e.connection()]) and not e.seq2 - 1 in seq_seen[e.connection()]:
            print "!! packet received out of sequence !! {0} cseq={1}".format(e.connection(), e.seq2)
            future[e.connection()][e.seq2] = e
            continue


        future[e.connection()][e.seq2] = e

        seq_ix = e.seq2

        while seq_ix in future[e.connection()]:
            e = future[e.connection()][seq_ix]
            seq_seen[e.connection()][e.seq2] = 1
            seq_ix += 1
            s = '{0} {1} type={2} len={3: 4d}'.format(e.time, e.connection(), e.type, e.len)
            s += ' cseq={0} cack={1} mask={2} eseq={3} eack={4}'.format(e.seq2, e.ack2, e.mask, e.seq, e.ack)

            if args.e:
                print s
                if not e.connection() in inflate:
                    print ' ' * 7, e.pp_data(8)
            if args.p:
                if not e.connection() in cmdpackets_seen:
                    if e.data == "\x02\x00\x00\x00\xff\xff":
                        print "        !!deflate detected!! on " + e.connection()
                        inflate[e.connection()] = zlib.decompressobj()

                if e.connection() in inflate:
                    if not e.connection() in cmdpackets_seen:
                        data = "\x78\x9c"
                        data += e.data
                        cmdpackets_seen[e.connection()] = 1
                        inflate_remain[e.connection()] = ''
                    else:
                        data = inflate_remain[e.connection()] + e.data

                    inflated = inflate[e.connection()].decompress(data)
                    print ' ' * 7, hexdump(inflated, 8)
                    e.data = inflated
                    inflate_remain[e.connection()] = inflate[e.connection()].unconsumed_tail

                e.prepend_remaining(remain[e.connection()])
                #print e.pp_data(16);
                for p in e.packets():
                    if p.type == 0x32:
                        c32[p.ack_cmdsource()] = p.simtick()
                    elif p.type == 0x33:
                        c33 = p.simtick()
                    elif p.type == 0x34:
                        c34 = p.simtick()
                    elif p.type == 0:
                        tick += p.simtick()

                    if p.can_decode():
                        print '       ', p.decode()
                    else:
                        s='        {0:02x} {1: 4d}    '.format(p.type, p.len - 3)
                        print s, p.pp_data(len(s) + 1)
                foo = ""
                foo = ''
                if c33 < c34:
                    foo += '<'
                elif c33 > c34:
                    foo += '>'
                else:
                    foo += ' '
                if args.t:
                    print "TICK", ''.join([str(c32[i]) + ' ' for i in range(0, len(c32))]), c33, c34, tick, foo

                remain[e.connection()] = e.remaining()
