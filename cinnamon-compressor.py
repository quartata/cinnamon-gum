import fileinput, subprocess, sys, tempfile

def bb96decode(bbytes, a = 0, s = []):
    bbytes = list(bbytes)
    for byte in bbytes:
      if byte == 10:
        byte = 127
      a = 96 * a + byte - 31
    while a:
      r = a % 256
      s = [r] + s
      a //= 256
    return bytes(s)

input = ""

for line in fileinput.input():
  input += line

mode = input[0]
code = input[1:]

with tempfile.NamedTemporaryFile() as temp:
  temp.write(code.encode("utf-8"))
  temp.flush()
  zopfli_result = subprocess.check_output(["zopfli", "-c", "--deflate", "--i100000", temp.name])
  lzma_result = subprocess.check_output(["lzma", "-9", "--format=raw", "--stdout", temp.name])
  bb96_result = bb96decode(code.encode("utf-8"))

  sys.stdout.buffer.write(mode.encode("utf-8") + min([zopfli_result, lzma_result, bb96_result], key=len))
