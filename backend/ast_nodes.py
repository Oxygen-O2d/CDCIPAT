from typing import Any, Dict, List, Optional

class ASTNode:
    def __init__(self, line: int):
        self.line = line

    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError()

class ProgramNode(ASTNode):
    def __init__(self, statements: List[ASTNode], line: int = 1):
        super().__init__(line)
        self.statements = statements

    def to_dict(self) -> Dict[str, Any]:
        return {
            'line': self.line,
            "type": "Program",
            "statements": [stmt.to_dict() for stmt in self.statements]
        }

class BlockNode(ASTNode):
    def __init__(self, statements: List[ASTNode], line: int):
        super().__init__(line)
        self.statements = statements

    def to_dict(self) -> Dict[str, Any]:
        return {
            'line': self.line,
            "type": "Block",
            "statements": [stmt.to_dict() for stmt in self.statements]
        }

class DeclNode(ASTNode):
    def __init__(self, var_type: str, identifier: str, expr: ASTNode, line: int):
        super().__init__(line)
        self.var_type = var_type
        self.identifier = identifier
        self.expr = expr

    def to_dict(self) -> Dict[str, Any]:
        return {
            'line': self.line,
            "type": "Declaration",
            "var_type": self.var_type,
            "identifier": self.identifier,
            "expr": self.expr.to_dict()
        }

class AssignNode(ASTNode):
    def __init__(self, identifier: str, expr: ASTNode, line: int):
        super().__init__(line)
        self.identifier = identifier
        self.expr = expr

    def to_dict(self) -> Dict[str, Any]:
        return {
            'line': self.line,
            "type": "Assignment",
            "identifier": self.identifier,
            "expr": self.expr.to_dict()
        }

class PrintNode(ASTNode):
    def __init__(self, expr: ASTNode, line: int):
        super().__init__(line)
        self.expr = expr

    def to_dict(self) -> Dict[str, Any]:
        return {
            'line': self.line,
            "type": "Print",
            "expr": self.expr.to_dict()
        }

class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, true_block: BlockNode, false_block: Optional[BlockNode], line: int):
        super().__init__(line)
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def to_dict(self) -> Dict[str, Any]:
        d = {
            'line': self.line,
            "type": "If",
            "condition": self.condition.to_dict(),
            "true_block": self.true_block.to_dict()
        }
        if self.false_block:
            d["false_block"] = self.false_block.to_dict()
        return d

class WhileNode(ASTNode):
    def __init__(self, condition: ASTNode, block: BlockNode, line: int):
        super().__init__(line)
        self.condition = condition
        self.block = block

    def to_dict(self) -> Dict[str, Any]:
        return {
            'line': self.line,
            "type": "While",
            "condition": self.condition.to_dict(),
            "block": self.block.to_dict()
        }

class BinOpNode(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode, line: int):
        super().__init__(line)
        self.left = left
        self.op = op
        self.right = right

    def to_dict(self) -> Dict[str, Any]:
        return {
            'line': self.line,
            "type": "BinOp",
            "op": self.op,
            "left": self.left.to_dict(),
            "right": self.right.to_dict()
        }

class IntNode(ASTNode):
    def __init__(self, value: int, line: int):
        super().__init__(line)
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            'line': self.line,
            "type": "IntConst",
            "value": self.value
        }

class FloatNode(ASTNode):
    def __init__(self, value: float, line: int):
        super().__init__(line)
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            'line': self.line,
            "type": "FloatConst",
            "value": self.value
        }

class IdentNode(ASTNode):
    def __init__(self, name: str, line: int):
        super().__init__(line)
        self.name = name

    def to_dict(self) -> Dict[str, Any]:
        return {
            'line': self.line,
            "type": "Identifier",
            "name": self.name
        }
