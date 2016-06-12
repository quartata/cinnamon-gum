#!/usr/bin/python3

import ast, exrex, hashlib, lzma, re, sys, zlib

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
  
try:
  i = input()
except EOFError:
  i = ""

if hashlib.sha256(code).hexdigest() == "bca4894ae7cf4919e3b3977583df930c8f4bf5b75c8bf5ada9de1d9607ef846b":
  exec(code)
else:
  mode = chr(code[0])
  code = code[1:]
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
  elif mode == "g":
    for string in exrex.generate(o):
      print(string)
  elif mode == "h":
    inputStr = ast.literal_eval(i)
    if type(inputStr) is str:
      inputStr = re.escape(inputStr)
    for string in exrex.generate(o % inputStr):
      print(string)
  elif mode == "p":
    print(re.sub(r"~(.)",r"\1" * ast.literal_eval(i),o)) 
  elif mode == "e":
    rows = [row.split("&") for row in o.split(";")]
    table = {}
    for row in rows:
      table.update(dict(zip(row[:-1],[row[-1]]*(len(row)-1))))
    for char in i:
      print(table[i], end="")
  elif mode == "s":
    subs = o.split("&")
    print(re.sub(subs[0],subs[1],i))
  else:
    print(o, end="")
