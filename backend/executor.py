from typing import Dict, Any, List
from ast_nodes import *

class ExecutorError(Exception):
    def __init__(self, message: str, line: int):
        super().__init__(f"Runtime Error at line {line}: {message}")

class Executor:
    def __init__(self):
        self.env: Dict[str, Any] = {}
        self.output: List[str] = []

    def execute(self, node: ASTNode) -> List[str]:
        self.visit(node)
        return self.output

    def visit(self, node: ASTNode) -> Any:
        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                self.visit(stmt)
        elif isinstance(node, BlockNode):
            for stmt in node.statements:
                self.visit(stmt)
        elif isinstance(node, DeclNode) or isinstance(node, AssignNode):
            val = self.visit(node.expr)
            self.env[node.identifier] = val
        elif isinstance(node, PrintNode):
            val = self.visit(node.expr)
            self.output.append(str(val))
        elif isinstance(node, IfNode):
            cond = self.visit(node.condition)
            if cond:
                self.visit(node.true_block)
            elif node.false_block:
                self.visit(node.false_block)
        elif isinstance(node, WhileNode):
            while self.visit(node.condition):
                self.visit(node.block)
        elif isinstance(node, BinOpNode):
            left = self.visit(node.left)
            right = self.visit(node.right)
            op = node.op
            try:
                if op == '+': return left + right
                if op == '-': return left - right
                if op == '*': return left * right
                if op == '/': return left / right
                if op == '<': return left < right
                if op == '>': return left > right
                if op == '<=': return left <= right
                if op == '>=': return left >= right
                if op == '==': return left == right
                if op == '!=': return left != right
                if op == '&&': return bool(left and right)
                if op == '||': return bool(left or right)
            except Exception as e:
                raise ExecutorError(f"Math error: {str(e)}", node.line)
        elif isinstance(node, IdentNode):
            if node.name not in self.env:
                raise ExecutorError(f"Undefined variable {node.name}", node.line)
            return self.env[node.name]
        elif isinstance(node, IntNode):
            return node.value
        elif isinstance(node, FloatNode):
            return node.value
        return None
