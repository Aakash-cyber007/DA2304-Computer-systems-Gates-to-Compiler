import sys
import os
import glob
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


def compile_file(jack_path, outdir):
    classname = os.path.splitext(os.path.basename(jack_path))[0]
    print(f"[JackCompiler] Compiling {jack_path}  -->  {classname}T.xml, {classname}.xml, {classname}.vm")

    tokenizer = JackTokenizer(jack_path)
    tokens = tokenizer.tokenize()
    tokenizer.write_xml(outdir)

    engine = CompilationEngine(tokens, classname, outdir)
    engine.compile_class()

    print(f"[JackCompiler] Done: {classname}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python JackCompiler.py <file.jack | directory>")
        sys.exit(1)

    target = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else 'out'

    os.makedirs(outdir, exist_ok=True)

    if os.path.isdir(target):
        jack_files = sorted(glob.glob(os.path.join(target, '*.jack')))
        if not jack_files:
            print(f"No .jack files found in {target}")
            sys.exit(1)
        for jf in jack_files:
            compile_file(jf, outdir)
    elif os.path.isfile(target) and target.endswith('.jack'):
        compile_file(target, outdir)
    else:
        print(f"Error: '{target}' is not a .jack file or directory")
        sys.exit(1)


if __name__ == '__main__':
    main()
