def findVMID(what, c, f, l):
    if what == "this":
        return "pointer 0"
    if what in c.statVars:
        return "static " + str(c.statVars[what][0])
    if what in c.fieldVars:
        return "this " + str(c.fieldVars[what][0])
    if what in f.arguments:
        return "argument " + str(f.arguments[what][0])
    if what in l.locals:
        return "local " + str(l.locals[what][0])
    raise ValueError
def findType(what, c, f, l):
    if what == "this":
        return c.name
    if what in c.statVars:
        return c.statVars[what][1]
    if what in c.fieldVars:
        return c.fieldVars[what][1]
    if what in f.arguments:
        return f.arguments[what][1]
    if what in l.locals:
        return l.locals[what][1]
    return what
def isKnown(what, c, f, l):
    return what == "this" or what in c.statVars or what in c.fieldVars or what in f.arguments or what in l.locals
to_s = { }
to_s["="] = "eq"
to_s["<"] = "lt"
to_s[">"] = "gt"
to_s["+"] = "add"
to_s["-"] = "sub"
to_s["&"] = "and"
to_s["|"] = "or"
def to_string(what):
    return to_s[what]+"\r\n"
class RecursiveDeclaration():
    def __init__(self, d = None, other = None):
        self.decs = []
        if other != None:
            self.decs += other.decs
        if d != None:
            self.decs.append(d)

class Class():
    def __init__(self, name, varDecs, subroutineDecs):
        self.name = name.value
        self.varDecs = varDecs
        self.subroutineDecs = subroutineDecs
        self.statVars = {}
        self.fieldVars = {}
        self.markCount = 0
        statCount = 0
        fieldCount = 0
        for d in varDecs.decs:
            for n in d.commaedIdentifiers.decs:
                if d.stat.value == "field":
                    self.fieldVars[n.value] = [fieldCount, d.typ.value]
                    fieldCount += 1
                else:
                    self.statVars[n.value] = [statCount, d.typ.value]
                    statCount += 1
    def eval(self):
        self.markCount = 0
        return self.subroutineDecs.eval(self)

class ClassVarDecs(RecursiveDeclaration):
    def eval(self):
        return "Not implemented"
class ClassVarDec():
    def __init__(self, stat, typ, commaedIdentifiers):
        self.stat = stat
        self.typ = typ
        self.commaedIdentifiers = commaedIdentifiers
class Type():
    def __init__(self, name):
        self.name = name
        self.value = name
class SubRoutineDecs(RecursiveDeclaration):
    def eval(self, c):
        return "\r\n".join(i.eval(c) for i in self.decs)
class SubRoutineDec():
    def __init__(self, stat, typ, name, parameters, body):
        self.stat = stat
        self.typ = typ
        self.name = name.value
        self.parameters = parameters
        self.body = body
        self.arguments = {}
        argCount = 1 if self.stat == "method" else 0
        for p in parameters.decs:
            self.arguments[p.name] = [argCount, p.typ]
            argCount += 1
    def eval(self, c):
        plusThis = 1 if self.stat == "method" else 0
        return "function " + c.name + "." + self.name + " " + str(plusThis + len([n for v in self.body.varDecs.decs for n in v.commaedIdentifiers.decs])) + "\r\n" + self.body.eval(c, self)
class ParemeterList(RecursiveDeclaration):
    def eval(self):
        return "Not implemented"
class Paremeter():
    def __init__(self, typ, name):
        self.typ = typ
        self.name = name
class SubRoutineBody():
    def __init__(self, varDecs, statements):
        self.varDecs = varDecs
        self.statements = statements
        self.locals = {}
        localCount = 0
        for v in varDecs.decs:
            for name in v.commaedIdentifiers.decs:
                self.locals[name.value] = [localCount, v.typ]
                localCount += 1
    def eval(self, c, f):
        ret = ""
        if f.stat == "method":
            ret += "push argument 0\r\n"
            ret += "pop pointer 0\r\n"
        elif f.stat == "constructor":
            ret += "push constant " + str(len(c.fieldVars)) + "\r\n"
            ret += "call Memory.alloc 1\r\n"
            ret += "pop pointer 0\r\n"
        ret += self.statements.eval(c, f, self)
        return ret
class VarDecs(RecursiveDeclaration):
    def eval(self):
        return "Not implemented"
class VarDec():
    def __init__(self, typ, commaedIdentifiers):
        self.typ = typ.value
        self.commaedIdentifiers = commaedIdentifiers
class Statements(RecursiveDeclaration):
    def eval(self, c, f, l):
        return "\r\n".join(i.eval(c, f, l) for i in self.decs)
class Let():
    def __init__(self, left, rightExp):
        self.left = left
        self.right = rightExp
    def eval(self, c, f, l):
        return self.right.eval(c, f, l) + "pop " + findVMID(self.left, c, f, l) + "\r\n"
class IndexLet():
    def __init__(self, left, indexExp, rightExp):
        self.left = left
        self.index = indexExp
        self.right = rightExp
    def eval(self, c, f, l):
        return self.index.eval(c, f, l) + "push " + findVMID(self.left, c, f, l) + "\r\nadd\r\n" + self.right.eval(c, f, l) + "pop temp 0\r\npop pointer 1\r\npush temp 0\r\npop that 0\r\n"
class IfElse():
    def __init__(self, conditionExp, ifStatements, elseStatements):
        self.condition = conditionExp
        self.ifs = ifStatements
        self.els = elseStatements
    def eval(self, c, f, l):
        ret = self.condition.eval(c, f, l)
        mc = c.markCount
        c.markCount += 2
        ret += "not\r\n"
        ret += "if-goto IF_" + str(mc) + "\r\n"
        ret += self.ifs.eval(c, f, l)
        ret += "goto IF_" + str(mc + 1) + "\r\n"
        ret += "label IF_" + str(mc) + "\r\n"
        if self.els != None:
            ret += self.els.eval(c, f, l)
        ret += "label IF_" + str(mc + 1) + "\r\n"
        return ret
class While():
    def __init__(self, conditionExp, statements):
        self.condition = conditionExp
        self.statements = statements
    def eval(self, c, f, l):
        mc = c.markCount
        c.markCount += 2
        ret = "label WHILE_" + str(mc) + "\r\n"
        ret += self.condition.eval(c, f, l)
        ret += "not\r\n"
        ret += "if-goto WHILE_" + str(mc + 1) + "\r\n"
        ret += self.statements.eval(c, f, l)
        ret += "goto WHILE_" + str(mc) + "\r\n"
        ret += "label WHILE_"+str(mc+1) + "\r\n"
        return ret
class Do():
    def __init__(self, subroutineCall):
        self.call = subroutineCall
    def eval(self, c, f, l):
        ret = self.call.eval(c, f, l)
        ret += "pop temp 0\r\n"
        return ret
class Return():
    def __init__(self, exp):
        self.exp = exp
    def eval(self, c, f, l):
        ret = ""
        if self.exp != None:
            ret += self.exp.eval(c, f, l)
        else:
            ret += "push constant 0\r\n"
        ret += "return\r\n"
        return ret
class Expression():
    def __init__(self, termList):
        self.tl = termList
    def eval(self, c, f, l):
        return self.tl.eval(c, f, l)
class TermList():
    def __init__(self, right, op, tl):
        self.right = right
        self.op = op
        self.tl = tl
    def eval(self, c, f, l):
        if self.op != None:
            ret = self.tl.eval(c, f, l) + self.right.eval(c, f, l)
            if self.op.value == "/":
                ret += "call Math.divide 2\r\n"
            elif self.op.value == "*":
                ret += "call Math.multiply 2\r\n"
            else:
                ret += to_string(self.op.value)
            return ret
        else:
            return self.right.eval(c, f, l)
class Number():
    def __init__(self, value):
        self.value = value
    def eval(self, c, f, l):
        return "push constant " + self.value + "\r\n"
class String():
    def __init__(self, value):
        self.value = value[1:-1]
    def eval(self, c, f, l):
        ret = "push constant " + str(len(self.value)) + "\r\n"
        ret += "call String.new 1\r\n"
        for i in self.value:
            ret += "push constant " + str(ord(i)) + "\r\n"
            ret += "call String.appendChar 2\r\n"
        return ret
class Keyword():
    def __init__(self, value):
        self.value = value
    def eval(self, c, f, l):
        if self.value == "this":
            return "push pointer 0\r\n"
        elif self.value == "true":
            return "push constant 0\r\nnot\r\n"
        elif self.value == "false":
            return "push constant 0\r\n"
        elif self.value == "null":
            return "push constant 0\r\n"
        else:
            return "Not implemented"
class IdTerm():
    def __init__(self, identifier, indexExp):
        self.identifier = identifier
        self.indexExp = indexExp
    def eval(self, c, f, l):
        if self.indexExp != None:
            ret = self.indexExp.eval(c, f, l)
            ret += "push " + findVMID(self.identifier, c, f, l) + "\r\n"
            ret += "add\r\n"
            ret += "pop pointer 1\r\n"
            ret += "push that 0\r\n"
            return ret
        else:
            return "push " + findVMID(self.identifier, c, f, l) + "\r\n"
class SCTerm():
    def __init__(self, subroutineCall):
        self.call = subroutineCall
    def eval(self, c, f, l):
        return self.call.eval(c, f, l)
class ParenTerm():
    def __init__(self, exp):
        self.exp = exp
    def eval(self, c, f, l):
        return self.exp.eval(c, f, l)
class UnaryTerm():
    def __init__(self, op, term):
        self.op = op
        self.term = term
    def eval(self, c, f, l):
        return self.term.eval(c, f, l) + ("not" if self.op == "~" else "neg") + "\r\n"
class SRCall():
    def __init__(self, left, right, args):
        self.left = left
        self.right = right
        self.args = args
    def eval(self, c, f, l):
        ret = ""
        argCount = len(self.args.decs)
        if isKnown(self.left, c, f, l):
            ret += "push " + findVMID(self.left, c, f, l) + "\r\n"
            argCount += 1
        ret += "\r\n".join(e.eval(c, f, l) for e in self.args.decs)
        ret += "call " + findType(self.left, c, f, l) + "." + self.right + " " + str(argCount) + "\r\n"
        return ret
class ExpressionList(RecursiveDeclaration):
    def eval(self):
        return "Not implemented"
class CommaedIdentifiers(RecursiveDeclaration):
    def eval(self):
        return "Not implemented"






