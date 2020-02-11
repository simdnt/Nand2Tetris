from lexer import Lexer
from parser import Parser
import sys
import glob
pg = Parser()
pg.parse()
parser = pg.get_parser()
lexer = Lexer().get_lexer()
for path in glob.glob(sys.argv[1] + "/*.jack"):
  outputFile = sys.argv[1] + "/" + path.split("/")[-1] + ".vm"
  with open(path, "r") as f:
    print path
    text_input = f.read()
    #print text_input
    tokens = lexer.lex(text_input)
    oc = parser.parse(tokens).eval()
    oc = "\r\n".join(line for line in oc.split("\r\n") if len(line) > 0)
    #print(oc)
    with open(outputFile, 'w') as output_file:
        output_file.write(oc)
