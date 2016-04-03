#!/usr/bin/python3

import hashlib, lzma, sys, zlib

def bb96encode(code, a = 0, s = []):
  code = list(code)
  for byte in code:
    a = 256 * a + byte
  while a:
    a -= 1
    r = a % 96
    s = [[10, r + 32][r < 95]] + s
    a //= 96
  return bytes(s)

with open(sys.argv[1], 'rb') as file:
  code = file.read()

if bb96encode(hashlib.sha256(code).digest()) == b"3'A~2dM'O6xiv9fzcp_ZoaI@eikCL*)%mR])NoB":
  i = input()
  exec(code)
else:
  try:
    o = zlib.decompress(code, -zlib.MAX_WBITS)
  except:
    try:
      o = lzma.decompress(code, format=lzma.FORMAT_RAW, filters=[{'id': lzma.FILTER_LZMA2, 'preset': 9 | lzma.PRESET_EXTREME}])
    except:
      o = bb96encode(code)

try:
  sys.stdout.buffer.write(o)
except:
  print(o, end="")
