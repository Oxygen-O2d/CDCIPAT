from typing import List, Dict, Any, Tuple
from ast_nodes import *

class SemanticError(Exception):
    def __init__(self, message: str, line: int):
        super().__init__(f"Semantic Error at line {line}: {message}")
        self.message = message
        self.line = line

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table: Dict[str, Dict[str, Any]] = {}
        self.errors: List[Dict[str, Any]] = []

    def analyze(self, node: ASTNode) -> Tuple[Dict[str, Dict[str, Any]], List[Dict[str, Any]]]:
        try:
            self.visit(node)
        except SemanticError as e:
            self.errors.append({"line": e.line, "message": e.message, "type": "error"})
        
        # Build symbol table array for frontend
        sym_list = []
        for name, info in self.symbol_table.items():
            sym_list.append({
                "name": name,
                "type": info["type"],
                "line": info["line"]
            })
        return sym_list, self.errors

    def visit(self, node: ASTNode) -> Optional[str]:
        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                self.visit(stmt)
        elif isinstance(node, BlockNode):
            for stmt in node.statements:
                self.visit(stmt)
        elif isinstance(node, DeclNode):
            if node.identifier in self.symbol_table:
                self.errors.append({"line": node.line, "message": f"Variable '{node.identifier}' is already declared", "type": "error"})
            else:
                self.symbol_table[node.identifier] = {"type": node.var_type, "line": node.line}
            
            expr_type = self.visit(node.expr)
            if expr_type and expr_type != node.var_type:
                # Allow int to float promotion as a warning, otherwise error
                if node.var_type == 'float' and expr_type == 'int':
                    pass # implicit promotion
                elif node.var_type == 'int' and expr_type == 'float':
                    self.errors.append({"line": node.line, "message": f"Possible loss of precision: assigning float to int '{node.identifier}'", "type": "warning"})
                else:
                    self.errors.append({"line": node.line, "message": f"Type mismatch: cannot assign {expr_type} to {node.var_type} '{node.identifier}'", "type": "error"})
        elif isinstance(node, AssignNode):
            if node.identifier not in self.symbol_table:
                self.errors.append({"line": node.line, "message": f"Variable '{node.identifier}' used before declaration", "type": "error"})
                return None
            
            var_type = self.symbol_table[node.identifier]["type"]
            expr_type = self.visit(node.expr)
            
            if expr_type and expr_type != var_type:
                if var_type == 'float' and expr_type == 'int':
                    pass
                elif var_type == 'int' and expr_type == 'float':
                    self.errors.append({"line": node.line, "message": f"Possible loss of precision: assigning float to int '{node.identifier}'", "type": "warning"})
                else:
                    self.errors.append({"line": node.line, "message": f"Type mismatch: cannot assign {expr_type} to {var_type} '{node.identifier}'", "type": "error"})
        
        elif isinstance(node, PrintNode):
            self.visit(node.expr)
            
        elif isinstance(node, IfNode):
            self.visit(node.condition)
            self.visit(node.true_block)
            if node.false_block:
                self.visit(node.false_block)
                
        elif isinstance(node, WhileNode):
            self.visit(node.condition)
            self.visit(node.block)
            
        elif isinstance(node, BinOpNode):
            left_type = self.visit(node.left)
            right_type = self.visit(node.right)
            
            if node.op in ['<', '>', '<=', '>=', '==', '!=']:
                return 'bool'
            elif node.op in ['&&', '||']:
                return 'bool'
            else:
                if left_type == 'float' or right_type == 'float':
                    return 'float'
                return 'int'
                
        elif isinstance(node, IdentNode):
            if node.name not in self.symbol_table:
                self.errors.append({"line": node.line, "message": f"Variable '{node.name}' used before declaration", "type": "error"})
                return 'unknown'
            return self.symbol_table[node.name]["type"]
            
        elif isinstance(node, IntNode):
            return 'int'
            
        elif isinstance(node, FloatNode):
            return 'float'
            
        return None
