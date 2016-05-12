#!/usr/bin/python3

import subprocess, tempfile

tests = [
  ["p\x01\xe42\xe3\xb0", "3", r"\\\o///"]
]

interpreter_path = "python3"

failures = []

for test in enumerate(tests):
  try:
    temp = tempfile.NamedTemporaryFile()
    temp.write(test[1][0])
    if subprocess.check_output("python3 cinnamon-gum.py %s < '%s'" % [temp.name, test[1][1]], shell=True) == test[1][2]:
      pass
    else:
      print("Test " + str(test[0] + 1) + " " + test[1][0]+" failed (incorrect output)\n")
  except Exception as e:
    print("Test " + str(test[0] + 1) + " " + test[1][0]+" failed (exception %s)\n" % e)

if not failures:
  sys.exit(1)
