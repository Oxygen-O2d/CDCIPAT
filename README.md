# MiniLang Compiler & Visualizer

An academic Compiler Design project demonstrating a complete 5-stage compilation pipeline from scratch (no parser generators). This project includes a custom-built programming language ("MiniLang") and a beautiful, interactive web-based visualizer.

## ✨ Features
- **Custom Language Syntax:** Fully custom keywords for declarations (`num`, `dec`), loops (`repeat`), conditionals (`check`/`otherwise`), and printing (`output`).
- **Full 5-Stage Pipeline:** Lexical Analysis → Syntax Analysis → Semantic Analysis → Intermediate Code Generation → Execution.
- **Interactive AST Visualizer:** Features a two-way binding system. Hover over an AST node to highlight the exact line of code that generated it, or hover over code to see the corresponding AST node glow!
- **In-Editor Error Highlighting:** VS Code-style red squiggly underlines directly in the source code editor when syntax or semantic errors are detected.

---

## 📚 The MiniLang Custom Language

MiniLang is a strictly typed imperative language designed specifically for this compiler.

### Variables & Types
All variables must be declared with a type before use.
- `num` - Integer numbers (e.g., 5, -10)
- `dec` - Decimal/floating-point numbers (e.g., 3.14)

```text
num count = 10;
dec price = 19.99;
```

### Control Flow
Conditional logic uses `check` and `otherwise`.
```text
check (count > 5) {
    count = count - 1;
} otherwise {
    count = count + 1;
}
```

### Loops
Loops are handled via the `repeat` keyword.
```text
repeat (count > 0) {
    output(count);
    count = count - 1;
}
```

### Output
Print results to the execution window using `output(...)`.
```text
output(count);
```

---

## 🏗️ Architecture & Code Explanation

This project is divided into two decoupled systems: a Python backend and a React frontend.

### 1. Backend (Python + FastAPI)
The core compiler engine lives in the `/backend` directory. It exposes a REST API via **FastAPI** (`main.py`). When code is submitted, it flows through the following compiler stages:
1. **Lexical Analysis (`lexer.py`)**: Uses regex to tokenize raw input into a stream of tokens, recognizing our custom keywords like `num` and `check`.
2. **Syntax Analysis (`parser.py`)**: A custom-built **SLR(1) Bottom-Up Parser**. It computes FIRST/FOLLOW sets and builds Action/Goto tables to reduce tokens into an Abstract Syntax Tree (AST) defined in `ast_nodes.py`.
3. **Semantic Analysis (`semantic.py`)**: Traverses the AST to construct a Symbol Table, enforcing strict type checking and scope resolution.
4. **Intermediate Code Generation (`codegen.py`)**: Lowers the validated AST into Three-Address Code (TAC), simulating lower-level machine instructions.
5. **Execution (`executor.py`)**: An interpreter that walks the AST to execute the program statefully and collect standard output.

### 2. Frontend (React + Vite)
The visualizer lives in the `/frontend` directory. It provides an educational lens into the compiler's inner workings.
- **`Editor.jsx`**: A syntax-highlighted code editor using `react-simple-code-editor` and `PrismJS`, equipped with our custom MiniLang grammar rules.
- **`TreeVisualizer.jsx`**: Uses `react-d3-tree` to draw the AST. It communicates with the Editor to enable the two-way hover-binding feature.
- **`PipelineStatus.jsx` & Others**: Cleanly visualizes the outputs from the backend, including the Token Table, Symbol Table, Semantic Checks, and IR Code.

## 🧠 Core Logic & Implementation Details

### 1. Lexical Analysis (Tokenizer)
The lexer (`lexer.py`) reads the source code and uses regular expressions to group characters into `Token` objects. It maps custom `MiniLang` keywords (`num`, `check`, `repeat`) into standard terminal symbols and tracks exact line/column numbers for error reporting.
> **Example:** `num x = 5;` becomes:
> `[Token('INT_TYPE', 'num'), Token('IDENT', 'x'), Token('ASSIGN', '='), Token('INT_CONST', '5'), Token('SEMICOLON', ';')]`

### 2. Syntax Analysis (SLR(1) Parser)
Instead of relying on parser generator tools like YACC or ANTLR, this project features a hand-rolled **Simple LR (SLR)** bottom-up parser (`parser.py`).
- **First & Follow Sets**: Upon initialization, the parser dynamically calculates the `FIRST` and `FOLLOW` sets for the MiniLang grammar.
- **Action/Goto Tables**: It computes closures and goto transitions to build the parsing tables.
- **AST Construction**: As the parser shifts and reduces tokens, it triggers semantic actions (lambda functions) that construct the **Abstract Syntax Tree (AST)** from the bottom up using classes defined in `ast_nodes.py`.
> **Example:** The tokens above are reduced into an AST node: `DeclNode(var_type='int', identifier='x', expr=IntNode(5))`

### 3. Semantic Analysis & Symbol Table
The Semantic Analyzer (`semantic.py`) performs a traversal of the generated AST to enforce type safety and variable scoping.
- **Symbol Table**: Tracks declared variables and their data types.
- **Validation**: Throws semantic errors if variables are used before they are declared, or if they are redeclared.
- **Type Checking**: Ensures that assignments are valid.
> **Example:** If you write `dec y = 3.14; num x = y;`, the semantic analyzer detects the type mismatch (float assigned to int) and generates a type warning/error.

### 4. Intermediate Code Generation (TAC)
The AST is lowered into **Three-Address Code (TAC)** in `codegen.py`. This intermediate representation breaks complex expressions into simple, assembly-like instructions using temporary variables (`t0`, `t1`). Control flow (`check` and `repeat`) is translated into conditional and unconditional `goto` jump instructions.
> **Example:** `num result = a + b * 2;` becomes:
> ```text
> t0 = b * 2
> result = a + t0
> ```

### 5. Execution (Interpreter)
The `Executor` class simulates the runtime environment. It walks the AST, maintaining a dictionary of variables in memory. It computes arithmetic results and captures any `output()` node values to display on the frontend.
> **Example:** When it evaluates `output(result);`, it looks up `result` in the runtime memory dictionary and appends its final computed value to the output trace.

---

## 📂 Backend Codebase Breakdown

Here is a deep dive into the specific Python files driving the compiler backend and their core logic:

### 1. `main.py` (The Orchestrator)
- **Role:** Exposes the compiler as a REST API using FastAPI.
- **Core Logic:** Receives the raw string code and orchestrates the compilation pipeline sequentially. It safely catches `LexerError`, `ParseError`, and `SemanticError`, halting execution early if a phase fails. It packs the AST, Tokens, TAC, and output into a `CompileResponse` JSON object for the frontend.

### 2. `lexer.py` (The Tokenizer)
- **Role:** Converts raw strings into structured tokens.
- **Core Logic:** Defines `TOKEN_SPECIFICATION` using regex patterns. The `tokenize()` method uses `re.finditer()` to step through the code, map matches to our custom `KEYWORDS` dictionary (`num`, `check`, `repeat`), compute the exact line/column numbers, and yield a list of `Token` named tuples.

### 3. `ast_nodes.py` (The Syntax Tree Data Structure)
- **Role:** Defines the blueprint for the Abstract Syntax Tree (AST).
- **Core Logic:** Every grammar rule maps to a class inheriting from `ASTNode` (e.g., `IfNode`, `BinOpNode`, `AssignNode`). Crucially, every node implements a `to_dict()` method to serialize the tree into JSON so the React frontend can dynamically render it using D3.js.

### 4. `parser.py` (The SLR(1) Parsing Engine)
- **Role:** The most complex file. Validates syntax and builds the AST.
- **Core Logic:** 
  - **`build_grammar()`**: Registers grammar rules and semantic actions (lambda functions that instantiate the AST Nodes).
  - **`build_tables()`**: Calculates FIRST/FOLLOW sets, computes `closure()` and `goto()`, and dynamically constructs the SLR Action and Goto state machine tables.
  - **`parse()`**: The main loop that reads tokens, looks up the current state in the Action table, and either `shifts` the token onto the stack or `reduces` the stack by executing the rule's semantic lambda to build the AST from the bottom up.

### 5. `semantic.py` (The Type Checker)
- **Role:** Enforces logical rules and tracks memory scoping.
- **Core Logic:** Uses the Visitor Pattern (`visit()`). It recursively walks the AST, maintaining a `symbol_table` dictionary mapping variable names to their defined types. If a node accesses an undeclared variable or assigns a mismatched type, it appends a `SemanticError` to the issues array.

### 6. `codegen.py` (Three-Address Code Generator)
- **Role:** Lowers the AST into an intermediate representation (TAC).
- **Core Logic:** Also uses the Visitor pattern. It maintains counters for temporary variables (`t0`, `t1`) and jump labels (`L1`, `L2`). For a `BinOpNode` (like `a + b`), it generates strings like `t0 = a + b` and returns `t0` to the parent node. For `WhileNode` and `IfNode`, it emits conditional `if False goto` string instructions.

### 7. `executor.py` (The Interpreter)
- **Role:** Executes the code and generates the final output.
- **Core Logic:** Simulates a virtual machine's runtime environment using a simple Python dictionary (`self.env`). When evaluating an `AssignNode`, it stores the computed value in `env[identifier]`. When evaluating a `PrintNode`, it looks up the value and appends it to an `output` array.

---

## 🚀 Getting Started

Follow these steps to run both the backend compiler engine and the frontend visualizer on your local machine.

### Step 1: Start the Backend (Compiler Engine)
Open a terminal and navigate to the `backend` directory. You will need to create a Python Virtual Environment to keep dependencies isolated.

```bash
cd backend

# 1. Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
# source venv/bin/activate

# 3. Install required Python packages
pip install -r requirements.txt

# 4. Start the FastAPI server
uvicorn main:app --reload
```
The backend API will now be running at `http://127.0.0.1:8000`.

### Step 2: Start the Frontend (Visualizer)
Open a **new** terminal window and navigate to the `frontend` directory.

```bash
cd frontend

# 1. Install Node.js dependencies
npm install

# 2. Start the Vite development server
npm run dev
```

### Step 3: Open the App
Once both servers are running, open your web browser and navigate to the URL provided by Vite (usually `http://localhost:5173`). 

You can select **"All Keywords Test"** from the "Load Example..." dropdown to see the compiler in action!
