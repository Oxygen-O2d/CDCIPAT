# MiniLang Compiler

An academic Compiler Design project demonstrating a complete 5-stage compilation pipeline from scratch (no parser generators).

## Compilation Pipeline

1. **Lexical Analysis:** Tokenizes input into a stream of tokens.
2. **Syntax Analysis:** Builds an Abstract Syntax Tree (AST) using a hand-written LL(1) recursive-descent parser.
3. **Semantic Analysis:** Constructs a Symbol Table and enforces type checking and scope rules.
4. **Intermediate Code Generation:** Lowers the AST into Three-Address Code (TAC).
5. **Execution:** Interprets the AST to produce live output.

## MiniLang Grammar (EBNF)

```ebnf
Program -> StmtList
StmtList -> Stmt StmtList | ε
Stmt -> DeclStmt | AssignStmt | IfStmt | WhileStmt | PrintStmt | Block

DeclStmt -> Type IDENT ASSIGN Expr SEMICOLON
Type -> "int" | "float"

AssignStmt -> IDENT ASSIGN Expr SEMICOLON
PrintStmt -> "print" LPAREN Expr RPAREN SEMICOLON

IfStmt -> "if" LPAREN Expr RPAREN Block ( "else" Block )?
WhileStmt -> "while" LPAREN Expr RPAREN Block
Block -> LBRACE StmtList RBRACE

Expr -> LogicalOrExpr
LogicalOrExpr -> LogicalAndExpr ( "||" LogicalAndExpr )*
LogicalAndExpr -> RelExpr ( "&&" RelExpr )*
RelExpr -> AddExpr ( RelOp AddExpr )?
RelOp -> "<" | ">" | "<=" | ">=" | "==" | "!="

AddExpr -> MulExpr ( AddOp MulExpr )*
AddOp -> "+" | "-"

MulExpr -> Factor ( MulOp Factor )*
MulOp -> "*" | "/"

Factor -> IDENT | INT_CONST | FLOAT_CONST | LPAREN Expr RPAREN
```

## Setup Instructions

### Backend (FastAPI)
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend (React/Vite)
```bash
cd frontend
npm install
npm run dev
```
