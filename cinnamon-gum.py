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

def decompress(code):
  mode = chr(code[0])
  code = code[1:]
  try:
    decompressed_code = zlib.decompress(code, -zlib.MAX_WBITS)
  except:
    try:
      decompressed_code = lzma.decompress(code, format=lzma.FORMAT_RAW, filters=[{'id': lzma.FILTER_LZMA2, 'preset': 9 | lzma.PRESET_EXTREME}])
    except:
      decompressed_code = bb96encode(code)

  return mode, "".join(map(chr, decompressed_code)) 

def get_input():
  try:
    return input()
  except EOFError:
    return ""

def execute(mode, code, input_str):
  result = ""

  if mode == "l":
     rows = [re.split(r"(?<![^\\]\\)&", row) for row in re.split(r"(?<![^\\]\\);", code)]
     table = {}
     for row in rows:
       table.update(dict(zip(row[:-1],[row[-1]]*(len(row)-1))))
     result = table[i]
  elif mode == "f":
     result = code % ast.literal_eval(input_str)
  elif mode == "g":
    for string in exrex.generate(code):
      print(string)
    return # Generate is always terminal
  elif mode == "h":
    if type(input_str) is str:
      input_str = re.escape(input_str)
    for string in exrex.generate(code % input_str):
      print(string)
    return
  elif mode == "p":
    result = re.sub(r"~(.)",r"\1" * ast.literal_eval(input_str), code) 
  elif mode == "e":
    rows = [re.split(r"(?<![^\\]\\)&", row) for row in re.split(r"(?<![^\\]\\);", code)]
    table = {}
    for row in rows:
      table.update(dict(zip(row[:-1],[row[-1]]*(len(row)-1))))
    for char in i:
      result += table[i]
  elif mode == "s":
    subs = re.split(r"(?<![^\\]\\)&", code)
    result = re.sub(subs[0],subs[1],i)
  elif mode == "i":
    result = code + input_str
  else:
    result = code

  if result[0] == "`":
    input_pieces = re.split(r"(?<![^\\]\\)!", result)
    if len(input_pieces) >= 2:
      execute(result[1], input_pieces[0][2:], "!".join(input_pieces[1:]))
    else:
      execute(result[1], result[2:], get_input())
  else:
    print(result)

if __name__ == "__main__":
  with open(sys.argv[1], 'rb') as file:
    code = file.read()
    i = get_input()

    if hashlib.sha256(code).hexdigest() == "bca4894ae7cf4919e3b3977583df930c8f4bf5b75c8bf5ada9de1d9607ef846b":
      exec(code)
    else:
      execute(*(decompress(code) + (i,)))
