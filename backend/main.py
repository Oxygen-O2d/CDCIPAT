from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from lexer import Lexer, LexerError
from parser import Parser, ParseError
from semantic import SemanticAnalyzer
from codegen import CodeGenerator
from executor import Executor, ExecutorError

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompileRequest(BaseModel):
    code: str

class TokenModel(BaseModel):
    type: str
    value: str
    line: int
    column: int

class SemanticErrorModel(BaseModel):
    line: int
    message: str
    type: str

class SymbolModel(BaseModel):
    name: str
    type: str
    line: int

class CompileResponse(BaseModel):
    success: bool
    stage: str
    error: Optional[str] = None
    tokens: Optional[List[TokenModel]] = None
    ast: Optional[Dict[str, Any]] = None
    symbol_table: Optional[List[SymbolModel]] = None
    semantic_issues: Optional[List[SemanticErrorModel]] = None
    tac: Optional[List[str]] = None
    output: Optional[List[str]] = None

EXAMPLES = {
    "All Keywords Test": """
// Tests all keywords: num, dec, check, otherwise, repeat, output
num base = 10;
dec multiplier = 2.5;
dec threshold = 20.0;
dec current = base * multiplier;

check (current > threshold) {
    output(current);
} otherwise {
    output(threshold);
}

num counter = 3;
repeat (counter > 0) {
    output(counter);
    counter = counter - 1;
}
""",
    "Factorial": """
num n = 5;
num result = 1;
repeat (n > 0) {
    result = result * n;
    n = n - 1;
}
output(result);
""",
    "Fibonacci Sequence": """
num a = 0;
num b = 1;
num max = 50;
num next = 0;

output(a);
output(b);

repeat (b < max) {
    next = a + b;
    a = b;
    b = next;
    
    check (b < max) {
        output(b);
    }
}
""",
    "Complex Logic": """
num x = 15;
num y = 30;

check (x < y && x != 0) {
    output(x);
} otherwise {
    output(y);
}
""",
    "Error (Phase 1): Lexical": """
// Lexical Analyzer will fail here because '@' is an invalid character
num score = 100;
score = score @ 10;
""",
    "Error (Phase 2): Syntax": """
// Syntax Analyzer will fail here due to a missing semicolon
num age = 20
num next_year = age + 1;
output(next_year);
""",
    "Error (Phase 3): Undeclared Var": """
// Semantic Analyzer will catch that 'total' was never declared
num subtotal = 50;
total = subtotal + 10; 
""",
    "Error (Phase 3): Redeclaration": """
// Semantic Analyzer will catch the duplicate declaration
num count = 1;
num count = 2; // Error: count already declared
output(count);
""",
    "Warning (Phase 3): Type Mismatch": """
// Semantic Analyzer will issue a warning for precision loss
num integer_val = 10;
dec float_val = 3.14;
integer_val = float_val; // Warning: Assigning dec to num
output(integer_val);
"""
}

@app.get("/api/examples")
def get_examples():
    return EXAMPLES

@app.post("/api/compile", response_model=CompileResponse)
def compile_code(req: CompileRequest):
    res = CompileResponse(success=False, stage="Init")
    
    # 1. Lexical Analysis
    res.stage = "Lexical Analysis"
    try:
        lexer = Lexer(req.code)
        res.tokens = [{"type": t.type, "value": t.value, "line": t.line, "column": t.column} for t in lexer.tokens]
    except LexerError as e:
        res.error = str(e)
        return res

    # 2. Syntax Analysis
    res.stage = "Syntax Analysis"
    try:
        parser = Parser(lexer.tokens)
        ast = parser.parse()
        res.ast = ast.to_dict()
    except ParseError as e:
        res.error = str(e)
        return res
        
    # 3. Semantic Analysis
    res.stage = "Semantic Analysis"
    semantic = SemanticAnalyzer()
    sym_tab, issues = semantic.analyze(ast)
    res.symbol_table = sym_tab
    res.semantic_issues = issues
    
    # If there are semantic errors, stop here
    has_errors = any(i["type"] == "error" for i in issues)
    if has_errors:
        res.error = "Semantic Analysis failed. Check Semantic Checks tab."
        res.success = False
        return res

    # 4. Intermediate Code Generation
    res.stage = "Intermediate Code Gen"
    codegen = CodeGenerator()
    res.tac = codegen.generate(ast)

    # 5. Execution
    res.stage = "Execution"
    try:
        executor = Executor()
        res.output = executor.execute(ast)
    except ExecutorError as e:
        res.error = str(e)
        return res

    res.success = True
    res.stage = "Completed"
    return res
