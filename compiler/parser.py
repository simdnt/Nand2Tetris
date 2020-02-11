from rply import ParserGenerator
from ast import  Class, ClassVarDecs, ClassVarDec, Type, SubRoutineDecs, SubRoutineDec, ParemeterList, Paremeter, SubRoutineBody, VarDecs, VarDec, Statements, Let, IndexLet, IfElse, While, Do, Return, Expression, TermList, Number, String, Keyword, IdTerm, SCTerm, ParenTerm, UnaryTerm, SRCall, ExpressionList, CommaedIdentifiers

class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['NUMBER', 'STRING_CONST', 'OPEN_PAREN', 'CLOSE_PAREN', 'OPEN_CURLY_PAREN', 'CLOSE_CURLY_PAREN', 'OPEN_INDEX_PAREN', 'CLOSE_INDEX_PAREN', 'DOT', 'COMMA', 'SEMI_COLON', 'SUM', 'SUB', 'MUL', 'DIV', 'AND', 'OR', 'LT', 'GT', 'EQUAL', 'NOT', 'CLASS', 'CONSTRUCTOR', 'FUNCTION', 'METHOD','FIELD', 'STATIC', 'VAR', 'INT', 'CHAR', 'BOOLEAN', 'VOID', 'TRUE', 'FALSE', 'NULL', 'THIS', 'LET', 'DO', 'IF','ELSE','WHILE', 'RETURN', 'IDENTIFIER' ])

    def parse(self):
        @self.pg.production('class : CLASS className OPEN_CURLY_PAREN classVarDecs subroutineDecs CLOSE_CURLY_PAREN')
        def handleClass(p):
            return Class(p[1], p[3], p[4])
        @self.pg.production('classVarDecs : ')
        @self.pg.production('classVarDecs : classVarDec')
        @self.pg.production('classVarDecs : classVarDecs classVarDec')
        def handleRecursiveClassVarDecs(p):
            return ClassVarDecs(p[1] if len(p) > 1 else p[0] if len(p) > 0 else None, p[0] if len(p) > 1 else None)
        @self.pg.production('classVarDec : STATIC type commaedIdentifiers SEMI_COLON')
        @self.pg.production('classVarDec : FIELD type commaedIdentifiers SEMI_COLON')
        def handleClassVarDec(p):
            return ClassVarDec(p[0], p[1], p[2])
        @self.pg.production('type : INT')
        @self.pg.production('type : CHAR')
        @self.pg.production('type : BOOLEAN')
        @self.pg.production('type : className')
        def handleType(p):
            return Type(p[0].value)
        @self.pg.production('subroutineDecs : ')
        @self.pg.production('subroutineDecs : subroutineDec')
        @self.pg.production('subroutineDecs : subroutineDecs subroutineDec')
        def handleRecursiveSRDecs(p):
            return SubRoutineDecs(p[1] if len(p) > 1 else p[0] if len(p) > 0 else None, p[0] if len(p) > 1 else None)
        @self.pg.production('subroutineDec : CONSTRUCTOR VOID subroutineName OPEN_PAREN parameterList CLOSE_PAREN subroutineBody')
        @self.pg.production('subroutineDec : CONSTRUCTOR type subroutineName OPEN_PAREN parameterList CLOSE_PAREN subroutineBody')
        @self.pg.production('subroutineDec : FUNCTION VOID subroutineName OPEN_PAREN parameterList CLOSE_PAREN subroutineBody')
        @self.pg.production('subroutineDec : FUNCTION type subroutineName OPEN_PAREN parameterList CLOSE_PAREN subroutineBody')
        @self.pg.production('subroutineDec : METHOD VOID subroutineName OPEN_PAREN parameterList CLOSE_PAREN subroutineBody')
        @self.pg.production('subroutineDec : METHOD type subroutineName OPEN_PAREN parameterList CLOSE_PAREN subroutineBody')
        def handleSRDec(p):
            return SubRoutineDec(p[0].value, p[1].value, p[2], p[4], p[6])
        @self.pg.production('parameterList : ')
        @self.pg.production('parameterList : parameter')
        @self.pg.production('parameterList : parameterList COMMA parameter')
        def handleRecursiveParamsList(p):
            return ParemeterList(p[2] if len(p) > 2 else p[0] if len(p) > 0 else None, p[0] if len(p) > 1 else None)
        @self.pg.production('parameter : type IDENTIFIER')
        def handleParameter(p):
            return Paremeter(p[0].value, p[1].value)
        @self.pg.production('subroutineBody : OPEN_CURLY_PAREN varDecs statements CLOSE_CURLY_PAREN')
        def handleSRBody(p):
            return SubRoutineBody(p[1], p[2])
        @self.pg.production('varDecs : ')
        @self.pg.production('varDecs : varDec')
        @self.pg.production('varDecs : varDecs varDec')
        def handleRecursiveVarDecs(p):
            return VarDecs(p[1] if len(p) > 1 else p[0] if len(p) > 0 else None, p[0] if len(p) > 1 else None)
        @self.pg.production('varDec : VAR type commaedIdentifiers SEMI_COLON')
        def handleVarDec(p):
            return VarDec(p[1], p[2])
        @self.pg.production('statements : ')
        @self.pg.production('statements : statement')
        @self.pg.production('statements : statements statement')
        def handleRecursiveStatements(p):
            return Statements(p[1] if len(p) > 1 else p[0] if len(p) > 0 else None, p[0] if len(p) > 1 else None)
        @self.pg.production('statement : LET IDENTIFIER EQUAL expression SEMI_COLON')
        def handleLet(p):
            return Let(p[1].value, p[3])
        @self.pg.production('statement : LET IDENTIFIER OPEN_INDEX_PAREN expression CLOSE_INDEX_PAREN EQUAL expression SEMI_COLON')
        def handleIndexLet(p):
            return IndexLet(p[1].value, p[3], p[6])
        @self.pg.production('statement : IF OPEN_PAREN expression CLOSE_PAREN OPEN_CURLY_PAREN statements CLOSE_CURLY_PAREN')
        def handleIf(p):
            return IfElse(p[2], p[5], None)
        @self.pg.production('statement : IF OPEN_PAREN expression CLOSE_PAREN OPEN_CURLY_PAREN statements CLOSE_CURLY_PAREN ELSE OPEN_CURLY_PAREN statements CLOSE_CURLY_PAREN') 
        def handleIfElse(p):
            return IfElse(p[2], p[5], p[9])
        @self.pg.production('statement : WHILE OPEN_PAREN expression CLOSE_PAREN OPEN_CURLY_PAREN statements CLOSE_CURLY_PAREN')
        def handleWhile(p):
            return While(p[2], p[5])
        @self.pg.production('statement : DO subroutineCall SEMI_COLON')
        def handleDo(p):
            return Do(p[1])
        @self.pg.production('statement : RETURN SEMI_COLON')
        def handleReturnVoid(p):
            return Return(None)
        @self.pg.production('statement : RETURN expression SEMI_COLON')
        def handleReturn(p):
            return Return(p[1])
        @self.pg.production('expression : termList')
        def handleExpression(p):
            return Expression(p[0])
        @self.pg.production('termList : term')
        def handleSingleTermList(p):
            return TermList(p[0], None, None)
        @self.pg.production('termList : termList op term')
        def handleRecursiveTermList(p):
            return TermList(p[2], p[1], p[0])
        @self.pg.production('term : NUMBER')
        def handleNumber(p):
            return Number(p[0].value)
        @self.pg.production('term : STRING_CONST')
        def handleString(p):
            return String(p[0].value)
        @self.pg.production('term : keywordConstant')
        def handleKeyword(p):
            return Keyword(p[0].value)
        @self.pg.production('term : IDENTIFIER')
        def handleIdentifierTerm(p):
            return IdTerm(p[0].value, None)
        @self.pg.production('term : IDENTIFIER OPEN_INDEX_PAREN expression CLOSE_INDEX_PAREN')
        def handleRecursiveIdentifierTerm(p):
            return IdTerm(p[0].value, p[2])
        @self.pg.production('term : subroutineCall')
        def handleSCTerm(p):
            return SCTerm(p[0])
        @self.pg.production('term : OPEN_PAREN expression CLOSE_PAREN')
        def handleParenTerm(p):
            return ParenTerm(p[1])
        @self.pg.production('term : unaryOp term')
        def handleUnaryTerm(p):
            return UnaryTerm(p[0].value, p[1])
        @self.pg.production('subroutineCall : subroutineName OPEN_PAREN expressionList CLOSE_PAREN')
        def handleThisSRCall(p):
            return SRCall("this", p[0].value, p[2])
        @self.pg.production('subroutineCall : IDENTIFIER DOT subroutineName OPEN_PAREN expressionList CLOSE_PAREN')
        def handleSRCall(p):
            return SRCall(p[0].value, p[2].value, p[4])
        @self.pg.production('expressionList : ')
        @self.pg.production('expressionList : expression')
        @self.pg.production('expressionList : expressionList COMMA expression')
        def handleRecursivExpressionListe(p):
            return ExpressionList(p[2] if len(p) > 2 else p[0] if len(p) > 0 else None, p[0] if len(p) > 1 else None)
        @self.pg.production('op : SUM')
        @self.pg.production('op : SUB')
        @self.pg.production('op : MUL')
        @self.pg.production('op : DIV')
        @self.pg.production('op : AND')
        @self.pg.production('op : OR')
        @self.pg.production('op : LT')
        @self.pg.production('op : GT')
        @self.pg.production('op : EQUAL')
        @self.pg.production('unaryOp : SUB')
        @self.pg.production('unaryOp : NOT')
        @self.pg.production('keywordConstant : TRUE')
        @self.pg.production('keywordConstant : FALSE')
        @self.pg.production('keywordConstant : NULL')
        @self.pg.production('keywordConstant : THIS')
        @self.pg.production('className : IDENTIFIER')
        @self.pg.production('subroutineName : IDENTIFIER')
        def KW(p):
            return p[0]
        @self.pg.production('commaedIdentifiers : IDENTIFIER')
        @self.pg.production('commaedIdentifiers : commaedIdentifiers COMMA IDENTIFIER')
        def handleCommaedIdentifiers(p):
            return CommaedIdentifiers(p[2]if len(p) > 2 else p[0], p[0] if len(p) > 2 else None)
 
        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
