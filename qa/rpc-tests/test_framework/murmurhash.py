# murmurhash.py
#
# Distributed under the MIT/X11 software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
#
# This python code was copied from
# https://raw.githubusercontent.com/jgarzik/python-bitcoinlib/417afe9e5868430e620301131f098645c081a90c/bitcoin/hash.py

import struct

def ROTL32(x, r):
    assert x <= 0xFFFFFFFF
    return ((x << r) & 0xFFFFFFFF) | (x >> (32 - r))

def MurmurHash3(nHashSeed, vDataToHash):

    assert nHashSeed <= 0xFFFFFFFF

    h1 = nHashSeed
    c1 = 0xcc9e2d51
    c2 = 0x1b873593

    # body
    i = 0
    while i < len(vDataToHash) - len(vDataToHash) % 4 \
          and len(vDataToHash) - i >= 4:

        k1 = struct.unpack("<L", vDataToHash[i:i+4])[0]

        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = ROTL32(k1, 15)
        k1 = (k1 * c2) & 0xFFFFFFFF

        h1 ^= k1
        h1 = ROTL32(h1, 13)
        h1 = (((h1*5) & 0xFFFFFFFF) + 0xe6546b64) & 0xFFFFFFFF

        i += 4

    # tail
    k1 = 0
    j = (len(vDataToHash) // 4) * 4
    if len(vDataToHash) & 3 >= 3:
        k1 ^= struct.unpack('<B', vDataToHash[j+2])[0] << 16
    if len(vDataToHash) & 3 >= 2:
        k1 ^= struct.unpack('<B', vDataToHash[j+1])[0] << 8
    if len(vDataToHash) & 3 >= 1:
        k1 ^= struct.unpack('<B', vDataToHash[j])[0]

    k1 &= 0xFFFFFFFF
    k1 = (k1 * c1) & 0xFFFFFFFF
    k1 = ROTL32(k1, 15)
    k1 = (k1 * c2) & 0xFFFFFFFF
    h1 ^= k1

    # finalization
    h1 ^= len(vDataToHash) & 0xFFFFFFFF
    h1 ^= (h1 & 0xFFFFFFFF) >> 16
    h1 *= 0x85ebca6b
    h1 ^= (h1 & 0xFFFFFFFF) >> 13
    h1 *= 0xc2b2ae35
    h1 ^= (h1 & 0xFFFFFFFF) >> 16

    return h1 & 0xFFFFFFFF
