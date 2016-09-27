#!/usr/bin/python3

import ast, exrex, hashlib, lzma, pcre, sys, zlib

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

def handle_pieces(pieces, input):  
  if len(pieces) > 1:
    return "`" + "`".join(pieces[1:])
  else:
    return input

def handle_table(rows):
  table = {}
  
  for row in rows:
    table.update(dict(zip(row[:-1],[row[-1]] * (len(row) - 1))))
    
  return table
  
def execute(mode, code, input_str):
  result = ""

  if mode == "l":
     rows = (pcre.split(r"(?<![^\\]\\)&", row) for row in pcre.split(r"(?<![^\\]\\);", code))
     table = handle_table(rows)
    
     if input_str in table:
       result = table[input_str]
     else:
       result = table["?"]
  elif mode == "f":
     result = code % ast.literal_eval(input_str)
  elif mode == "F":
     literal = ast.literal_eval(input_str)
     if isinstance(literal, tuple):
       result = code % literal
       input_str = str(sum((len(str(x)) for x in literal)))
     else:
       result = code % literal
       input_str = str(len(str(literal)))
  elif mode == "g":
    for string in exrex.generate(code):
      print(string.encode("utf-8").decode("unicode-escape"))
    return # Generate is always terminal
  elif mode == "h":
    if type(input_str) is str:
      input_str = pcre.escape(input_str)
    for string in exrex.generate(code % input_str):
      print(string.encode("utf-8").decode("unicode-escape"))
    return
  elif mode == "p":
    literal = ast.literal_eval(input_str)
    if isinstance(literal, int):
      result = pcre.sub(r"(?<![^\\]\\)~(.+?)(?<![^\\]\\)~",r"\1" * literal, code, flags=pcre.DOTALL) 
    else:
      result = pcre.sub(r"(?<![^\\]\\)%(.+?)(?<![^\\]\\)%",r"\1" * literal[1], pcre.sub(r"~(.+?)~",r"\1" * literal[0], code, flags=pcre.DOTALL), flags=pcre.DOTALL)
  elif mode == "P":
    result = pcre.sub(r"(.)(?<![^\\]\\)~",r"\1" * ast.literal_eval(input_str), code, flags=pcre.DOTALL)
  elif mode == "e":
    rows = (pcre.split(r"(?<![^\\]\\)&", row) for row in pcre.split(r"(?<![^\\]\\);", code))
    table = handle_table(rows)
    
    for char in i:
      result += table[i]
      
  elif mode == "o":
    pieces = pcre.split(r"(?<![^\\]\\)`", code)
    print(pieces[0].encode("utf-8").decode("unicode-escape"))
    result = handle_pieces(pieces[1:])
  elif mode == "s":
    pieces = pcre.split(r"(?<![^\\]\\)`", code)
    subs = pcre.split(r"(?<![^\\]\\)&", pieces[0])
    sub_length = len(subs)

    for i in range(0, len(subs), 2):
      input_str = pcre.sub(subs[i], subs[i + 1], input_str)

    result = handle_pieces(pieces[1:])
  elif mode == "d":
    pieces = pcre.split(r"(?<![^\\]\\)`", code)
    subs = pcre.split(r"(?<![^\\]\\)&", pieces[0])
    
    for sub in subs:
      input_str = pcre.sub(sub, "", input_str)

    result = handle_pieces(pieces[1:])
  elif mode == "S":
    pieces = pcre.split(r"(?<![^\\]\\)`", code)
    subs = pcre.split(r"(?<![^\\]\\)&", pieces[0])
    sub_length = len(subs)
    output = input_str
    for i in range(0, len(subs), 2):
      output = pcre.sub(subs[i], subs[i + 1], output)
    
    result = handle_pieces(pieces[1:])
    print(output.encode("utf-8").decode("unicode-escape"))
  elif mode == "i":
    result = code + input_str
  elif mode == "I":
    result = code + "\n" + input_str
  else:
    result = code

  if len(result) > 0 and result[0] == "`":
    input_pieces = pcre.split(r"(?<![^\\]\\)!", result)
    if len(input_pieces) >= 2:
      execute(result[1], input_pieces[0][2:], "!".join(input_pieces[1:]))
    else:
      execute(result[1], result[2:], get_input(input_str))
  else:
    print(result.encode("utf-8").decode("unicode-escape"))

if __name__ == "__main__":
  pcre.enable_re_template_mode()
  with open(sys.argv[1], 'rb') as file:
    string = file.read()
    if hashlib.sha256(string).hexdigest() == "bca4894ae7cf4919e3b3977583df930c8f4bf5b75c8bf5ada9de1d9607ef846b":
      i = input()
      exec(string)
    else:
      mode, code = decompress(string)
      input_pieces = pcre.split(r"(?<![^\\]\\)!", code)
  
      if len(input_pieces) >= 2:
        i = get_input("!".join(input_pieces[1:]))
      else:
        i = get_input("")

      execute(mode, input_pieces[0], i)
