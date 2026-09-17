import json
from collections import defaultdict

class ParseError(Exception):
    def __init__(self, message, token=None):
        loc = f" at line {token.line}" if token else ""
        super().__init__(f"Syntax Error{loc}: {message}")
        self.token = token

# --- AST Node definitions to match what we need ---
from ast_nodes import (
    ProgramNode, BlockNode, DeclNode, AssignNode,
    IfNode, WhileNode, PrintNode, BinOpNode,
    IdentNode, IntNode, FloatNode
)

class Rule:
    def __init__(self, lhs, rhs, action=None):
        self.lhs = lhs
        self.rhs = rhs if rhs != ['EPSILON'] else []
        self.action = action

    def __repr__(self):
        return f"{self.lhs} -> {' '.join(self.rhs) if self.rhs else 'EPSILON'}"

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs

    def __hash__(self):
        return hash((self.lhs, tuple(self.rhs)))

class Item:
    def __init__(self, rule, dot):
        self.rule = rule
        self.dot = dot

    def __eq__(self, other):
        return self.rule == other.rule and self.dot == other.dot

    def __hash__(self):
        return hash((self.rule, self.dot))

    def next_symbol(self):
        if self.dot < len(self.rule.rhs):
            return self.rule.rhs[self.dot]
        return None

    def __repr__(self):
        rhs = list(self.rule.rhs)
        rhs.insert(self.dot, '.')
        return f"{self.rule.lhs} -> {' '.join(rhs)}"

class SLRParser:
    def __init__(self):
        self.rules = []
        self.terminals = set()
        self.nonterminals = set()
        self.start_symbol = "Program"
        
        self.action_table = {}
        self.goto_table = {}
        
        self.build_grammar()
        self.build_tables()

    def build_grammar(self):
        # Helper to add rules easily
        def add(lhs, rhs_str, action=None):
            rhs = rhs_str.split()
            self.rules.append(Rule(lhs, rhs, action))
            self.nonterminals.add(lhs)
            for sym in rhs:
                if sym == 'EPSILON': continue
                if sym.isupper() or sym in ['<','>','<=','>=','==','!=','+','-','*','/','&&','||']:
                    self.terminals.add(sym)
                else:
                    self.nonterminals.add(sym)

        self.rules.append(Rule("Start_Prime", [self.start_symbol]))
        self.nonterminals.add("Start_Prime")

        add("Program", "StmtList", lambda p: ProgramNode(p[0]))
        
        add("StmtList", "StmtList Stmt", lambda p: p[0] + [p[1]])
        add("StmtList", "EPSILON", lambda p: [])
        
        add("Stmt", "DeclStmt", lambda p: p[0])
        add("Stmt", "AssignStmt", lambda p: p[0])
        add("Stmt", "IfStmt", lambda p: p[0])
        add("Stmt", "WhileStmt", lambda p: p[0])
        add("Stmt", "PrintStmt", lambda p: p[0])
        add("Stmt", "Block", lambda p: p[0])
        
        add("DeclStmt", "Type IDENT ASSIGN Expr SEMICOLON", lambda p: DeclNode(p[0], p[1].value, p[3], p[1].line))
        add("Type", "INT_TYPE", lambda p: 'int')
        add("Type", "FLOAT_TYPE", lambda p: 'float')
        
        add("AssignStmt", "IDENT ASSIGN Expr SEMICOLON", lambda p: AssignNode(p[0].value, p[2], p[0].line))
        add("PrintStmt", "PRINT LPAREN Expr RPAREN SEMICOLON", lambda p: PrintNode(p[2], p[0].line))
        
        add("IfStmt", "IF LPAREN Expr RPAREN Block ELSE Block", lambda p: IfNode(p[2], p[4], p[6], p[0].line))
        add("IfStmt", "IF LPAREN Expr RPAREN Block", lambda p: IfNode(p[2], p[4], None, p[0].line))
        
        add("WhileStmt", "WHILE LPAREN Expr RPAREN Block", lambda p: WhileNode(p[2], p[4], p[0].line))
        
        add("Block", "LBRACE StmtList RBRACE", lambda p: BlockNode(p[1], p[0].line))
        
        add("Expr", "LogicalOrExpr", lambda p: p[0])
        
        add("LogicalOrExpr", "LogicalOrExpr OR LogicalAndExpr", lambda p: BinOpNode(p[0], '||', p[2], getattr(p[0], 'line', 0)))
        add("LogicalOrExpr", "LogicalAndExpr", lambda p: p[0])
        
        add("LogicalAndExpr", "LogicalAndExpr AND RelExpr", lambda p: BinOpNode(p[0], '&&', p[2], getattr(p[0], 'line', 0)))
        add("LogicalAndExpr", "RelExpr", lambda p: p[0])
        
        add("RelExpr", "AddExpr RelOp AddExpr", lambda p: BinOpNode(p[0], p[1], p[2], getattr(p[0], 'line', 0)))
        add("RelExpr", "AddExpr", lambda p: p[0])
        
        add("RelOp", "LT", lambda p: '<')
        add("RelOp", "GT", lambda p: '>')
        add("RelOp", "LE", lambda p: '<=')
        add("RelOp", "GE", lambda p: '>=')
        add("RelOp", "EQ", lambda p: '==')
        add("RelOp", "NEQ", lambda p: '!=')
        
        add("AddExpr", "AddExpr PLUS MulExpr", lambda p: BinOpNode(p[0], '+', p[2], getattr(p[0], 'line', 0)))
        add("AddExpr", "AddExpr MINUS MulExpr", lambda p: BinOpNode(p[0], '-', p[2], getattr(p[0], 'line', 0)))
        add("AddExpr", "MulExpr", lambda p: p[0])
        
        add("MulExpr", "MulExpr MUL Factor", lambda p: BinOpNode(p[0], '*', p[2], getattr(p[0], 'line', 0)))
        add("MulExpr", "MulExpr DIV Factor", lambda p: BinOpNode(p[0], '/', p[2], getattr(p[0], 'line', 0)))
        add("MulExpr", "Factor", lambda p: p[0])
        
        add("Factor", "IDENT", lambda p: IdentNode(p[0].value, p[0].line))
        add("Factor", "INT_CONST", lambda p: IntNode(int(p[0].value), p[0].line))
        add("Factor", "FLOAT_CONST", lambda p: FloatNode(float(p[0].value), p[0].line))
        add("Factor", "LPAREN Expr RPAREN", lambda p: p[1])
        
        self.terminals.add('$')

    def compute_first_sets(self):
        first = {nt: set() for nt in self.nonterminals}
        for t in self.terminals:
            first[t] = {t}
        first['EPSILON'] = {'EPSILON'}
        
        changed = True
        while changed:
            changed = False
            for rule in self.rules:
                if not rule.rhs:
                    if 'EPSILON' not in first[rule.lhs]:
                        first[rule.lhs].add('EPSILON')
                        changed = True
                else:
                    for sym in rule.rhs:
                        f = first.get(sym, {sym})
                        before = len(first[rule.lhs])
                        first[rule.lhs].update(f - {'EPSILON'})
                        if 'EPSILON' not in f:
                            break
                    else:
                        before = len(first[rule.lhs])
                        first[rule.lhs].add('EPSILON')
                        
                    if len(first[rule.lhs]) > before:
                        changed = True
        return first

    def follow_sets(self, first_sets):
        follow = {nt: set() for nt in self.nonterminals}
        follow["Start_Prime"].add('$')
        
        changed = True
        while changed:
            changed = False
            for rule in self.rules:
                for i, sym in enumerate(rule.rhs):
                    if sym in self.nonterminals:
                        next_first = set()
                        for nsym in rule.rhs[i+1:]:
                            f = first_sets.get(nsym, {nsym})
                            next_first.update(f - {'EPSILON'})
                            if 'EPSILON' not in f:
                                break
                        else:
                            next_first.add('EPSILON')
                        
                        before = len(follow[sym])
                        follow[sym].update(next_first - {'EPSILON'})
                        if 'EPSILON' in next_first or i == len(rule.rhs) - 1:
                            follow[sym].update(follow[rule.lhs])
                        if len(follow[sym]) > before:
                            changed = True
        return follow

    def closure(self, items):
        C = set(items)
        changed = True
        while changed:
            changed = False
            new_items = set()
            for item in C:
                sym = item.next_symbol()
                if sym in self.nonterminals:
                    for rule in self.rules:
                        if rule.lhs == sym:
                            new_item = Item(rule, 0)
                            if new_item not in C:
                                new_items.add(new_item)
            if new_items:
                C.update(new_items)
                changed = True
        return C

    def goto(self, items, symbol):
        moved = set()
        for item in items:
            if item.next_symbol() == symbol:
                moved.add(Item(item.rule, item.dot + 1))
        return self.closure(moved)

    def build_tables(self):
        first_sets = self.compute_first_sets()
        follow = self.follow_sets(first_sets)
        
        start_item = Item(self.rules[0], 0)
        start_state = frozenset(self.closure({start_item}))
        
        states = [start_state]
        state_idx = {start_state: 0}
        
        queue = [0]
        
        while queue:
            idx = queue.pop(0)
            state = states[idx]
            
            self.action_table[idx] = {}
            self.goto_table[idx] = {}
            
            # Reduce actions
            for item in state:
                if item.dot == len(item.rule.rhs):
                    if item.rule.lhs == "Start_Prime":
                        self.action_table[idx]['$'] = ('accept', None)
                    else:
                        for f in follow[item.rule.lhs]:
                            if f in self.action_table[idx] and self.action_table[idx][f][0] != 'reduce':
                                # Prefer shift on conflict (resolves dangling else & precedence)
                                continue
                            self.action_table[idx][f] = ('reduce', item.rule)
            
            # Shift & Goto actions
            symbols = set(item.next_symbol() for item in state if item.next_symbol())
            for sym in symbols:
                next_state_set = frozenset(self.goto(state, sym))
                if not next_state_set: continue
                
                if next_state_set not in state_idx:
                    state_idx[next_state_set] = len(states)
                    states.append(next_state_set)
                    queue.append(state_idx[next_state_set])
                
                nidx = state_idx[next_state_set]
                if sym in self.terminals:
                    self.action_table[idx][sym] = ('shift', nidx)
                else:
                    self.goto_table[idx][sym] = nidx

class Parser:
    _slr = None
    
    def __init__(self, tokens):
        self.tokens = tokens
        # We only generate the SLR tables once when the server starts
        if Parser._slr is None:
            Parser._slr = SLRParser()
        self.slr = Parser._slr

    def parse(self):
        tokens = list(self.tokens)
        stack = [0]
        sym_stack = []
        
        idx = 0
        while True:
            state = stack[-1]
            tok = tokens[idx] if idx < len(tokens) else None
            sym = '$' if (not tok or tok.type == 'EOF') else tok.type
            
            action = self.slr.action_table[state].get(sym)
            
            if not action:
                expected = [k for k, v in self.slr.action_table[state].items() if k != '$']
                raise ParseError(f"Unexpected token '{tok.value if tok else 'EOF'}'. Expected one of: {', '.join(expected)}", tok)
                
            atype, aparam = action
            
            if atype == 'shift':
                stack.append(aparam)
                sym_stack.append(tok)
                idx += 1
            elif atype == 'reduce':
                rule = aparam
                rhs_len = len(rule.rhs)
                
                popped_syms = []
                for _ in range(rhs_len):
                    stack.pop()
                    popped_syms.insert(0, sym_stack.pop())
                
                if rule.action:
                    new_sym = rule.action(popped_syms)
                else:
                    new_sym = None
                    
                sym_stack.append(new_sym)
                
                new_state = self.slr.goto_table[stack[-1]][rule.lhs]
                stack.append(new_state)
            elif atype == 'accept':
                return sym_stack[0]
