from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        self.lexer.ignore('/\*((.|[\\r\\n])*?)\*/')
        self.lexer.ignore('//.*\\n')
        self.lexer.ignore('\s+') # Ignore spaces

        self.lexer.add('NUMBER', r'\d+')
        self.lexer.add('STRING_CONST', r'"(.*)"')

        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')
        self.lexer.add('OPEN_CURLY_PAREN', r'\{')
        self.lexer.add('CLOSE_CURLY_PAREN', r'\}')
        self.lexer.add('OPEN_INDEX_PAREN', r'\[')
        self.lexer.add('CLOSE_INDEX_PAREN', r'\]')
        self.lexer.add('DOT', r'\.')
        self.lexer.add('COMMA', r'\,')
        self.lexer.add('SEMI_COLON', r'\;')
        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'/')
        self.lexer.add('AND', r'&')
        self.lexer.add('OR', r'\|')
        self.lexer.add('LT', r'<')
        self.lexer.add('GT', r'>')
        self.lexer.add('EQUAL', r'=')
        self.lexer.add('NOT', '~')

        self.lexer.add('CLASS', r'class')
        self.lexer.add('CONSTRUCTOR', r'constructor')
        self.lexer.add('FUNCTION', r'function')
        self.lexer.add('METHOD', r'method')
        self.lexer.add('FIELD', r'field')
        self.lexer.add('STATIC', r'static')
        self.lexer.add('VAR', r'var')
        self.lexer.add('INT', r'int')
        self.lexer.add('CHAR', r'char')
        self.lexer.add('BOOLEAN', r'boolean')
        self.lexer.add('VOID', r'void')
        self.lexer.add('TRUE', r'true')
        self.lexer.add('FALSE', r'false')
        self.lexer.add('NULL', r'null')
        self.lexer.add('THIS', r'this')
        self.lexer.add('LET', r'let')
        self.lexer.add('DO', r'do ')
        self.lexer.add('IF', r'if')
        self.lexer.add('ELSE', r'else')
        self.lexer.add('WHILE', r'while')
        self.lexer.add('RETURN', r'return')
        self.lexer.add('IDENTIFIER', r'[A-Za-z_](\w*)')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()

