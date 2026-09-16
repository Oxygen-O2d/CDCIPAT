from typing import List, Optional
from lexer import Token
from ast_nodes import *

class ParseError(Exception):
    def __init__(self, message: str, token: Token):
        super().__init__(f"Syntax Error at line {token.line}, col {token.column}: {message}")
        self.token = token

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def consume(self, expected_type: str) -> Token:
        token = self.peek()
        if token.type == expected_type:
            self.pos += 1
            return token
        raise ParseError(f"expected '{expected_type}' but found '{token.type}' ({token.value})", token)

    def match(self, expected_type: str) -> bool:
        if self.peek().type == expected_type:
            self.consume(expected_type)
            return True
        return False

    def parse(self) -> ProgramNode:
        stmts = self.parse_stmt_list()
        self.consume('EOF')
        return ProgramNode(stmts)

    def parse_stmt_list(self) -> List[ASTNode]:
        stmts = []
        while self.peek().type in ['INT_TYPE', 'FLOAT_TYPE', 'IDENT', 'IF', 'WHILE', 'PRINT', 'LBRACE']:
            stmts.append(self.parse_stmt())
        return stmts

    def parse_stmt(self) -> ASTNode:
        token = self.peek()
        if token.type in ['INT_TYPE', 'FLOAT_TYPE']:
            return self.parse_decl_stmt()
        elif token.type == 'IDENT':
            return self.parse_assign_stmt()
        elif token.type == 'IF':
            return self.parse_if_stmt()
        elif token.type == 'WHILE':
            return self.parse_while_stmt()
        elif token.type == 'PRINT':
            return self.parse_print_stmt()
        elif token.type == 'LBRACE':
            return self.parse_block()
        else:
            raise ParseError("expected statement", token)

    def parse_decl_stmt(self) -> DeclNode:
        type_token = self.peek()
        if type_token.type == 'INT_TYPE':
            self.consume('INT_TYPE')
            var_type = 'int'
        elif type_token.type == 'FLOAT_TYPE':
            self.consume('FLOAT_TYPE')
            var_type = 'float'
        else:
            raise ParseError("expected 'num' or 'dec'", type_token)
        
        ident = self.consume('IDENT')
        self.consume('ASSIGN')
        expr = self.parse_expr()
        self.consume('SEMICOLON')
        return DeclNode(var_type, ident.value, expr, type_token.line)

    def parse_assign_stmt(self) -> AssignNode:
        ident = self.consume('IDENT')
        self.consume('ASSIGN')
        expr = self.parse_expr()
        self.consume('SEMICOLON')
        return AssignNode(ident.value, expr, ident.line)

    def parse_print_stmt(self) -> PrintNode:
        start_tok = self.consume('PRINT')
        self.consume('LPAREN')
        expr = self.parse_expr()
        self.consume('RPAREN')
        self.consume('SEMICOLON')
        return PrintNode(expr, start_tok.line)

    def parse_if_stmt(self) -> IfNode:
        start_tok = self.consume('IF')
        self.consume('LPAREN')
        cond = self.parse_expr()
        self.consume('RPAREN')
        true_block = self.parse_block()
        false_block = None
        if self.match('ELSE'):
            false_block = self.parse_block()
        return IfNode(cond, true_block, false_block, start_tok.line)

    def parse_while_stmt(self) -> WhileNode:
        start_tok = self.consume('WHILE')
        self.consume('LPAREN')
        cond = self.parse_expr()
        self.consume('RPAREN')
        block = self.parse_block()
        return WhileNode(cond, block, start_tok.line)

    def parse_block(self) -> BlockNode:
        start_tok = self.consume('LBRACE')
        stmts = self.parse_stmt_list()
        self.consume('RBRACE')
        return BlockNode(stmts, start_tok.line)

    def parse_expr(self) -> ASTNode:
        return self.parse_logical_or()

    def parse_logical_or(self) -> ASTNode:
        left = self.parse_logical_and()
        while self.peek().type == 'OR':
            op = self.consume('OR')
            right = self.parse_logical_and()
            left = BinOpNode(left, op.value, right, op.line)
        return left

    def parse_logical_and(self) -> ASTNode:
        left = self.parse_rel_expr()
        while self.peek().type == 'AND':
            op = self.consume('AND')
            right = self.parse_rel_expr()
            left = BinOpNode(left, op.value, right, op.line)
        return left

    def parse_rel_expr(self) -> ASTNode:
        left = self.parse_add_expr()
        if self.peek().type in ['LT', 'GT', 'LE', 'GE', 'EQ', 'NEQ']:
            op = self.consume(self.peek().type)
            right = self.parse_add_expr()
            left = BinOpNode(left, op.value, right, op.line)
        return left

    def parse_add_expr(self) -> ASTNode:
        left = self.parse_mul_expr()
        while self.peek().type in ['PLUS', 'MINUS']:
            op = self.consume(self.peek().type)
            right = self.parse_mul_expr()
            left = BinOpNode(left, op.value, right, op.line)
        return left

    def parse_mul_expr(self) -> ASTNode:
        left = self.parse_factor()
        while self.peek().type in ['STAR', 'SLASH']:
            op = self.consume(self.peek().type)
            right = self.parse_factor()
            left = BinOpNode(left, op.value, right, op.line)
        return left

    def parse_factor(self) -> ASTNode:
        token = self.peek()
        if token.type == 'IDENT':
            self.consume('IDENT')
            return IdentNode(token.value, token.line)
        elif token.type == 'INT_CONST':
            self.consume('INT_CONST')
            return IntNode(int(token.value), token.line)
        elif token.type == 'FLOAT_CONST':
            self.consume('FLOAT_CONST')
            return FloatNode(float(token.value), token.line)
        elif token.type == 'LPAREN':
            self.consume('LPAREN')
            expr = self.parse_expr()
            self.consume('RPAREN')
            return expr
        else:
            raise ParseError(f"expected IDENT, INT, FLOAT, or LPAREN, found '{token.type}'", token)
