from typing import List
from ast_nodes import *

class CodeGenerator:
    def __init__(self):
        self.code: List[str] = []
        self.temp_count = 1
        self.label_count = 1

    def new_temp(self) -> str:
        t = f"t{self.temp_count}"
        self.temp_count += 1
        return t

    def new_label(self) -> str:
        l = f"L{self.label_count}"
        self.label_count += 1
        return l

    def generate(self, node: ASTNode) -> List[str]:
        self.visit(node)
        return self.code

    def visit(self, node: ASTNode) -> Optional[str]:
        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                self.visit(stmt)
        elif isinstance(node, BlockNode):
            for stmt in node.statements:
                self.visit(stmt)
        elif isinstance(node, DeclNode) or isinstance(node, AssignNode):
            res = self.visit(node.expr)
            self.code.append(f"{node.identifier} = {res}")
        elif isinstance(node, PrintNode):
            res = self.visit(node.expr)
            self.code.append(f"PRINT {res}")
        elif isinstance(node, IfNode):
            cond_res = self.visit(node.condition)
            false_label = self.new_label()
            end_label = self.new_label()
            
            self.code.append(f"IF_FALSE {cond_res} GOTO {false_label}")
            self.visit(node.true_block)
            self.code.append(f"GOTO {end_label}")
            self.code.append(f"{false_label}:")
            if node.false_block:
                self.visit(node.false_block)
            self.code.append(f"{end_label}:")
            
        elif isinstance(node, WhileNode):
            start_label = self.new_label()
            end_label = self.new_label()
            
            self.code.append(f"{start_label}:")
            cond_res = self.visit(node.condition)
            self.code.append(f"IF_FALSE {cond_res} GOTO {end_label}")
            self.visit(node.block)
            self.code.append(f"GOTO {start_label}")
            self.code.append(f"{end_label}:")
            
        elif isinstance(node, BinOpNode):
            left_res = self.visit(node.left)
            right_res = self.visit(node.right)
            t = self.new_temp()
            self.code.append(f"{t} = {left_res} {node.op} {right_res}")
            return t
            
        elif isinstance(node, IdentNode):
            return node.name
        elif isinstance(node, IntNode):
            return str(node.value)
        elif isinstance(node, FloatNode):
            return str(node.value)
            
        return None
