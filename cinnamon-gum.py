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

def get_input(last_input):
  try:
    return input()
  except EOFError:
    return last_input

def execute(mode, code, input_str):
  result = ""

  if mode == "l":
     rows = [re.split(r"(?<![^\\]\\)&", row) for row in re.split(r"(?<![^\\]\\);", code)]
     table = {}
     for row in rows:
       table.update(dict(zip(row[:-1],[row[-1]]*(len(row)-1))))
     if input_str in table:
       result = table[input_str]
     else:
       result = table["?"]
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
    literal = ast.literal_eval(input_str)
    if isinstance(literal, int):
      result = re.sub(r"(?<![^\\]\\)~(.+?)(?<![^\\]\\)~",r"\1" * literal, code, flags=re.DOTALL) 
    else:
      result = re.sub(r"(?<![^\\]\\)%(.+?)(?<![^\\]\\)%",r"\1" * literal[1], re.sub(r"~(.+?)~",r"\1" * literal[0], code, flags=re.DOTALL), flags=re.DOTALL)
  elif mode == "e":
    rows = [re.split(r"(?<![^\\]\\)&", row) for row in re.split(r"(?<![^\\]\\);", code)]
    table = {}
    for row in rows:
      table.update(dict(zip(row[:-1],[row[-1]]*(len(row)-1))))
    for char in i:
      result += table[i]
  elif mode == "o":
    pieces = re.split(r"(?<![^\\]\\)`", code)
    print(pieces[0])
    result = "`" + "`".join(pieces[1:])
  elif mode == "s":
    pieces = re.split(r"(?<![^\\]\\)`", code)
    subs = re.split(r"(?<![^\\]\\)&", pieces[0])
    sub_length = len(subs)

    for i in range(0, len(subs), 2):
      input_str = re.sub(subs[i], subs[i + 1], input_str)

    if len(pieces) > 1:
      result = "`" + "`".join(pieces[1:])
    else:
      result = input_str
  elif mode == "d":
    pieces = re.split(r"(?<![^\\]\\)`", code)
    subs = re.split(r"(?<![^\\]\\)&", pieces[0])
    sub_length = len(subs)

    for sub in subs:
      input_str = re.sub(sub, "", input_str)

    if len(pieces) > 1:
      result = "`" + "`".join(pieces[1:])
    else:
      result = input_str
  elif mode == "S":
    pieces = re.split(r"(?<![^\\]\\)`", code)
    subs = re.split(r"(?<![^\\]\\)&", pieces[0])
    sub_length = len(subs)
    output = input_str
    for i in range(0, len(subs), 2):
      output = re.sub(subs[i], subs[i + 1], output)
    if len(pieces) > 1:
      result = "`" + "`".join(pieces[1:])
    else:
      result = ""
    print(output)
  elif mode == "i":
    result = code + input_str
  elif mode == "I":
    result = code + "\n" + input_str
  else:
    result = code

  if len(result) > 0 and result[0] == "`":
    input_pieces = re.split(r"(?<![^\\]\\)!", result)
    if len(input_pieces) >= 2:
      execute(result[1], input_pieces[0][2:], "!".join(input_pieces[1:]))
    else:
      execute(result[1], result[2:], get_input(input_str))
  else:
    print(result)

if __name__ == "__main__":
  with open(sys.argv[1], 'rb') as file:
    code = file.read()
    i = get_input("")

    if hashlib.sha256(code).hexdigest() == "bca4894ae7cf4919e3b3977583df930c8f4bf5b75c8bf5ada9de1d9607ef846b":
      exec(code)
    else:
      execute(*(decompress(code) + (i,)))
