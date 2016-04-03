#!/usr/bin/python3

import ast, hashlib, lzma, sys, zlib

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

mode = chr(code[0])
code = code[1:]
i = input()

if bb96encode(hashlib.sha256(code).digest()) == b"3'A~2dM'O6xiv9fzcp_ZoaI@eikCL*)%mR])NoB":
  exec(code)
else:
  try:
    o = zlib.decompress(code, -zlib.MAX_WBITS)
  except:
    try:
      o = lzma.decompress(code, format=lzma.FORMAT_RAW, filters=[{'id': lzma.FILTER_LZMA2, 'preset': 9 | lzma.PRESET_EXTREME}])
    except:
      o = bb96encode(code)

  o = "".join(map(chr,o))

  if mode == "l":
    rows = [row.split("&") for row in o.split(";")]
    table = {}
    for row in rows:
      table.update(dict(zip(row[:-1],[row[-1]]*(len(row)-1))))
    print(table[i], end="")
  elif mode == "f":
    print(o % ast.literal_eval(i), end="")
  else:
    print(o, end="")
