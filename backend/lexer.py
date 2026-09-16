import re
from typing import List, NamedTuple

class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Lexical Error at line {line}, col {column}: {message}")
        self.line = line
        self.column = column

TOKEN_SPECIFICATION = [
    ('FLOAT_CONST', r'\d+\.\d+'),
    ('INT_CONST',   r'\d+'),
    ('IDENT',       r'[A-Za-z_][A-Za-z0-9_]*'),
    ('EQ',          r'=='),
    ('NEQ',         r'!='),
    ('LE',          r'<='),
    ('GE',          r'>='),
    ('AND',         r'&&'),
    ('OR',          r'\|\|'),
    ('ASSIGN',      r'='),
    ('LT',          r'<'),
    ('GT',          r'>'),
    ('PLUS',        r'\+'),
    ('MINUS',       r'-'),
    ('STAR',        r'\*'),
    ('SLASH',       r'/'),
    ('LPAREN',      r'\('),
    ('RPAREN',      r'\)'),
    ('LBRACE',      r'\{'),
    ('RBRACE',      r'\}'),
    ('SEMICOLON',   r';'),
    ('COMMENT',     r'//.*'),
    ('WHITESPACE',  r'[ \t]+'),
    ('NEWLINE',     r'\n'),
    ('MISMATCH',    r'.'),
]

KEYWORDS = {
    'check': 'IF', 'otherwise': 'ELSE', 'repeat': 'WHILE', 'output': 'PRINT',
    'num': 'INT_TYPE', 'dec': 'FLOAT_TYPE'
}

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.tokens: List[Token] = []
        self.tokenize()

    def tokenize(self):
        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)
        line_num = 1
        line_start = 0
        for mo in re.finditer(tok_regex, self.text):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start + 1
            
            if kind == 'COMMENT':
                pass
            elif kind == 'WHITESPACE':
                pass
            elif kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
            elif kind == 'IDENT':
                kind = KEYWORDS.get(value, 'IDENT')
                self.tokens.append(Token(kind, value, line_num, column))
            elif kind == 'MISMATCH':
                raise LexerError(f"Unexpected character {value!r}", line_num, column)
            else:
                self.tokens.append(Token(kind, value, line_num, column))
        self.tokens.append(Token('EOF', '', line_num, len(self.text) - line_start + 1))
