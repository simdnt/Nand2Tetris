import sys

f = open(sys.argv[1], "r")
rawlines = f.read().split("\n")
output = []
lines = []
markCounter = 16
marks = { "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4, "SCREEN": 16384, "KBD": 24576 }
for line in rawlines:
  line = line.split("//")[0].strip().replace(" ","")
  if len(line) > 0:
    if line[0] == '(':
      mark = line[1:-1]
      marks[mark] = len(lines)
    else:
      lines.append(line)

for line in lines:
  if line[0] == '@':
    what = line[1:]
    num = -1
    if what.isdigit():
      num = int(what)
    elif what[0] == 'R' and what[1:].isdigit():
      num = int(what[1:])
    else:
      if not what in marks:
        marks[what] = markCounter
        markCounter += 1
      num = marks[what]
    output.append("0" + "{0:015b}".format(num)[:15])
  else:
    dest = ""
    computation = line
    jmp = ""
    if "=" in line:
      parts = line.split("=")
      dest = parts[0].upper()
      computation = parts[1]
    if ";" in computation:
      parts = computation.split(";")
      computation = parts[0]
      jmp = parts[1].upper()
    
    oline = "111"
    cs = computation.lower().replace("m","a")
    oline += "1" if "M" in computation.upper() else "0"
    oline += "0" if "d" in cs else "1"
    oline += "0" if "&" in cs or "a-d" == cs or ("d" in cs and "+" in cs and "a" in cs) or "d-1" == cs or "0" == cs or (("d" in cs and "a" not in cs) and "d+1" != cs) else "1"
    oline += "0" if "a" in cs else "1"
    oline += "0" if "&" in cs or "d-a" == cs or ("d" in cs and "+" in cs and "a" in cs) or "a-1" == cs or "-1" == cs or "0" == cs or (("a" in cs and "d" not in cs) and "a+1" != cs) else "1"
    oline += "1" if "+" in cs or "-" in cs or cs == "1" or cs == "0" else "0"
    oline += "1" if "!" in cs or "|" in cs or "+1" in cs or "-d" in cs or "-a" in cs or cs == "1" else "0"
    oline += "1" if "A" in dest else "0"
    oline += "1" if "D" in dest else "0"
    oline += "1" if "M" in dest else "0"
    oline += "1" if "L" in jmp or jmp == "JNE" or jmp == "JMP" else "0"
    oline += "1" if ("E" in jmp and "N" not in jmp) or jmp == "JMP" else "0"
    oline += "1" if "G" in jmp or jmp == "JNE" or jmp == "JMP" else "0"
    output.append(oline)

f = open(sys.argv[1] + ".hack", "w")
for x in output:
  f.write(x + "\r\n")
f.close()
