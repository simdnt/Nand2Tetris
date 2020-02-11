import sys
import glob
outputFile = sys.argv[1] + "/" + sys.argv[1].split("/")[-1] + ".asm"
rawlines = []
for path in glob.glob(sys.argv[1] + "/*.vm"):
  f = open(path, "r")
  rawlines += [[path.split("/")[-1][:-3], i] for i in f.read().split("\n")]
o = [
  "@261",
  "D=A",
  "@SP",
  "M=D",
  "@Sys.init",
  "0;JMP"
]
lines = []
fcallCount = 0
jmpCount = 0
currentFunctionName = ""

def binaryAssociativeOperation(operation):
  o.append("@SP")
  o.append("AM=M-1")
  o.append("D=M")
  o.append("A=A-1")
  o.append("M=D" + operation + "M")

def compOperation(jmpString):
    global jmpCount
    o.append("@SP")
    o.append("AM=M-1")
    o.append("A=A-1")
    o.append("D=M")
    o.append("A=A+1")
    o.append("D=D-M")
    o.append("A=A-1")
    o.append("@jumpMark." + str(jmpCount) + ".0")
    o.append("D;" + jmpString)
    o.append("@SP")
    o.append("A=M-1")
    o.append("M=0")
    o.append("@jumpMark." + str(jmpCount) + ".1")
    o.append("0;JMP")
    o.append("(jumpMark." + str(jmpCount) + ".0)")
    o.append("@SP")
    o.append("A=M-1")
    o.append("M=-1")
    o.append("(jumpMark." + str(jmpCount) + ".1)")
    jmpCount += 1

def unaryOperation(operation):
    o.append("@SP")
    o.append("A=M-1")
    o.append("M=" + operation + "M")

def findSegmentIndexInA(line, parts):
    c2 = parts[1]
    o.append("@"+parts[2])
    o.append("D=A")
    if c2 != "constant":
      if c2 == "temp" or c2 == "static":
        if c2 == "temp":
          o.append("@5")
          o.append("A=D+A")
        if c2 == "static":
          o.append("@" + line[0] + ".static." + str(parts[2]))
      elif c2 == "pointer":
        o.append("@THIS")
        o.append("A=D+A")
      else:
        if c2 == "argument":
          o.append("@ARG")
        if c2 == "local":
          o.append("@LCL")
        if c2 == "this":
          o.append("@THIS")
        if c2 == "that":
          o.append("@THAT")
        o.append("A=D+M")

for line in rawlines:
  line[1] = line[1].split("//")[0].strip()
  if len(line[1]) > 0:
    lines.append(line)

for line in lines:
  parts = line[1].split()
  c = parts[0]
  if c == "add":
    binaryAssociativeOperation("+")
  elif c == "sub":
    o.append("@SP")
    o.append("AM=M-1")
    o.append("A=A-1")
    o.append("D=M")
    o.append("A=A+1")
    o.append("D=D-M")
    o.append("A=A-1")
    o.append("M=D")
  elif c == "neg":
    unaryOperation("-")
  elif c == "eq":
    compOperation("JEQ")
  elif c == "gt":
    compOperation("JGT")
  elif c == "lt":
    compOperation("JLT")
  elif c == "and":
    binaryAssociativeOperation("&")
  elif c == "or":
    binaryAssociativeOperation("|")
  elif c == "not":
    unaryOperation("!")
  elif c == "push":
    findSegmentIndexInA(line, parts)
    if parts[1] != "constant":
        o.append("D=M")
    o.append("@SP")
    o.append("M=M+1")
    o.append("A=M-1")
    o.append("M=D")
  elif c == "pop":
    findSegmentIndexInA(line, parts)
    o.append("D=A")
    o.append("@15")
    o.append("M=D")
    o.append("@SP")
    o.append("AM=M-1")
    o.append("D=M")
    o.append("@15")
    o.append("A=M")
    o.append("M=D")
  elif c == "label":
    o.append("(" + currentFunctionName + "." + parts[1] + ")")
  elif c == "goto":
    o.append("@" + currentFunctionName + "." + parts[1])
    o.append("0;JMP")
  elif c == "if-goto":
    o.append("@SP")
    o.append("AM=M-1")
    o.append("D=M")
    o.append("@" + currentFunctionName + "." + parts[1])
    o.append("D;JNE")
  elif c == "function":
    currentFunctionName = parts[1]
    o.append("(" + currentFunctionName + ")")
    for k in range(0,int(parts[2])):
      o.append("@SP")
      o.append("M=M+1")
      o.append("A=M-1")
      o.append("M=0")
  elif c == "call":
    o.append("@fcall." + str(fcallCount))
    o.append("D=A")
    o.append("@SP")
    o.append("A=M")
    o.append("M=D")#return address
    o.append("@LCL")
    o.append("D=M")
    o.append("@SP")
    o.append("AM=M+1")
    o.append("M=D")#local
    o.append("@ARG")
    o.append("D=M")
    o.append("@SP")
    o.append("AM=M+1")
    o.append("M=D")#argument
    o.append("@THIS")
    o.append("D=M")
    o.append("@SP")
    o.append("AM=M+1")
    o.append("M=D")#this
    o.append("@THAT")
    o.append("D=M")
    o.append("@SP")
    o.append("AM=M+1")
    o.append("M=D")#that

    o.append("@SP")
    o.append("MD=M+1")
    o.append("@LCL")
    o.append("M=D")
    o.append("@"+parts[2])
    o.append("A=A+1")
    o.append("A=A+1")
    o.append("A=A+1")
    o.append("A=A+1")
    o.append("A=A+1")
    o.append("D=D-A")
    o.append("@ARG")
    o.append("M=D")
    
    o.append("@" + parts[1])
    o.append("0;JMP")
    o.append("(fcall." + str(fcallCount) + ")")
    fcallCount += 1
  elif c == "return":
    o.append("@LCL")
    o.append("D=M")
    o.append("@13")
    o.append("M=D")#save fix address
    o.append("@5")
    o.append("A=D-A")
    o.append("D=M")
    o.append("@12")
    o.append("M=D")#save return address to prevent overriding if 0 arguments

    o.append("@SP")
    o.append("A=M-1")
    o.append("D=M")
    o.append("@ARG")
    o.append("A=M")
    o.append("M=D")
    o.append("D=A+1")
    o.append("@SP")
    o.append("M=D")#return value

    o.append("@13")
    o.append("AM=M-1")
    o.append("D=M")
    o.append("@THAT")
    o.append("M=D")
    o.append("@13")
    o.append("AM=M-1")
    o.append("D=M")
    o.append("@THIS")
    o.append("M=D")
    o.append("@13")
    o.append("AM=M-1")
    o.append("D=M")
    o.append("@ARG")
    o.append("M=D")
    o.append("@13")
    o.append("AM=M-1")
    o.append("D=M")
    o.append("@LCL")
    o.append("M=D")

    o.append("@12")
    o.append("A=M")
    o.append("0;JMP")#jump to saved return address

o.append("@endendend")
o.append("(endendend)")
o.append("0;JMP")
f = open(outputFile, "w")
for x in o:
  f.write(x + "\r\n")
f.close()
