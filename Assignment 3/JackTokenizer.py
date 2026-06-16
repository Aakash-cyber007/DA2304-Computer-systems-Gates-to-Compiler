import re
import os

KEYWORDS = {
    'class', 'constructor', 'function', 'method', 'field', 'static',
    'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
    'this', 'let', 'do', 'if', 'else', 'while', 'return'
}

SYMBOLS = set('{}()[].,;+-*/&|<>=~')

XML_ESCAPE = {
    '<': '&lt;',
    '>': '&gt;',
    '&': '&amp;',
    '"': '&quot;',
}


class JackTokenizer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.classname = os.path.splitext(os.path.basename(filepath))[0]
        with open(filepath, 'r') as f:
            self.source = f.read()
        self.tokens = []

    def _strip_comments(self, src):
        result = []
        i = 0
        n = len(src)
        IN_CODE, IN_LINE_COMMENT, IN_BLOCK_COMMENT, IN_STRING = 0, 1, 2, 3
        state = IN_CODE

        while i < n:
            if state == IN_CODE:
                if src[i] == '"':
                    state = IN_STRING
                    result.append(src[i])
                    i += 1
                elif i + 1 < n and src[i:i+2] == '//':
                    state = IN_LINE_COMMENT
                    i += 2
                elif i + 1 < n and src[i:i+2] == '/*':
                    state = IN_BLOCK_COMMENT
                    i += 2
                else:
                    result.append(src[i])
                    i += 1
            elif state == IN_LINE_COMMENT:
                if src[i] == '\n':
                    state = IN_CODE
                    result.append('\n')
                i += 1
            elif state == IN_BLOCK_COMMENT:
                if i + 1 < n and src[i:i+2] == '*/':
                    state = IN_CODE
                    i += 2
                else:
                    if src[i] == '\n':
                        result.append('\n')
                    i += 1
            elif state == IN_STRING:
                result.append(src[i])
                if src[i] == '"':
                    state = IN_CODE
                i += 1

        return ''.join(result)

    TOKEN_RE = re.compile(
        r'(\d+)'              # integerConstant
        r'|(".*?")'           # stringConstant (non-greedy, no newlines expected)
        r'|([a-zA-Z_]\w*)'   # keyword or identifier
        r'|([{}()\[\].,;+\-*/&|<>=~])'  # symbol
    )

    def tokenize(self):
        clean = self._strip_comments(self.source)
        for m in self.TOKEN_RE.finditer(clean):
            integer, string, word, symbol = m.groups()
            if integer is not None:
                self.tokens.append(('integerConstant', integer))
            elif string is not None:
                self.tokens.append(('stringConstant', string[1:-1]))
            elif word is not None:
                if word in KEYWORDS:
                    self.tokens.append(('keyword', word))
                else:
                    self.tokens.append(('identifier', word))
            elif symbol is not None:
                self.tokens.append(('symbol', symbol))
        return self.tokens

    def write_xml(self, outdir='.'):
        lines = ['<tokens>']
        for ttype, tval in self.tokens:
            escaped = ''.join(XML_ESCAPE.get(c, c) or c for c in tval)
            lines.append(f'<{ttype}> {escaped} </{ttype}>')
        lines.append('</tokens>')
        path = os.path.join(outdir, f'{self.classname}T.xml')
        with open(path, 'w') as f:
            f.write('\n'.join(lines) + '\n')
        return path


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python JackTokenizer.py <file.jack>")
        sys.exit(1)
    t = JackTokenizer(sys.argv[1])
    t.tokenize()
    out = t.write_xml()
    print(f"Wrote {out}")
