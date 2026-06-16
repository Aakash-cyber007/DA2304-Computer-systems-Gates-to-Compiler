# Jack Compiler Frontend

## Requirements
- Python 3.8+

## Usage

### Compile a single file
```bash
python JackCompiler.py ../jack/Conv.jack ../out/
```

### Compile an entire directory
```bash
python JackCompiler.py ../jack/ ../out/
```

This produces for each `<ClassName>.jack`:
- `<ClassName>T.xml` — tokeniser output
- `<ClassName>.xml`  — parse-tree XML
- `<ClassName>.vm`   — executable VM code

### Pipeline integration
Feed the `.vm` files into your Assignment 2 VM Translator:
```bash
python VMTranslator.py ../out/   # produces .asm files
```
Then load the `.asm` into the Hack CPU Emulator.

## Files
| File | Role |
|---|---|
| `JackTokenizer.py` | Lexical analyser — strips comments (state machine), classifies tokens |
| `SymbolTable.py` | Two-scope symbol table (class + subroutine) |
| `VMWriter.py` | Emits VM commands |
| `CompilationEngine.py` | Recursive-descent parser; produces XML parse tree + VM code |
| `JackCompiler.py` | Master pipeline script |
