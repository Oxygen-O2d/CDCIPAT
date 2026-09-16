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
    "Factorial": """
num n = 5;
num result = 1;
repeat (n > 0) {
    result = result * n;
    n = n - 1;
}
output(result);
""",
    "Type Checking": """
num x = 10;
dec y = 3.14;
x = y; // Semantic Warning: Float to Int
output(x);
""",
    "Undeclared Var": """
num a = 5;
b = a + 2; // Semantic Error: b undeclared
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
