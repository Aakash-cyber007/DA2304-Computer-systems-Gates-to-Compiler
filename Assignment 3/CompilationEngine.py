import os
from SymbolTable import SymbolTable
from VMWriter import VMWriter

XML_ESCAPE = {'<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;'}

OP_MAP = {
    '+': 'add', '-': 'sub', '&': 'and', '|': 'or',
    '<': 'lt',  '>': 'gt',  '=': 'eq',
}
UNARY_OP_MAP = {'-': 'neg', '~': 'not'}

KEYWORD_CONSTANTS = {'true', 'false', 'null', 'this'}


class CompilationEngine:
    def __init__(self, tokens, classname, outdir='.'):
        self.tokens = tokens
        self.pos = 0
        self.classname = classname
        self.outdir = outdir

        # XML output
        self._xml = []
        self._indent = 0

        # Symbol table & VM writer
        self.symtab = SymbolTable()
        self.vm = VMWriter(os.path.join(outdir, f'{classname}.vm'))
        self._label_counter = 0

        # State tracked during compilation
        self._current_subroutine_kind = None  # 'constructor'|'function'|'method'
        self._current_subroutine_name = None

    def _cur(self):
        return self.tokens[self.pos]

    def _peek_val(self):
        return self.tokens[self.pos][1]

    def _peek_type(self):
        return self.tokens[self.pos][0]

    def _advance(self):
        ttype, tval = self.tokens[self.pos]
        self.pos += 1
        return ttype, tval

    def _eat(self, expected_val=None, expected_type=None):
        ttype, tval = self._advance()
        if expected_val is not None and tval != expected_val:
            raise SyntaxError(
                f"Expected '{expected_val}', got '{tval}' at token {self.pos-1}")
        if expected_type is not None and ttype != expected_type:
            raise SyntaxError(
                f"Expected type '{expected_type}', got '{ttype}' at token {self.pos-1}")
        return ttype, tval

    def _xml_open(self, tag):
        self._xml.append('  ' * self._indent + f'<{tag}>')
        self._indent += 1

    def _xml_close(self, tag):
        self._indent -= 1
        self._xml.append('  ' * self._indent + f'</{tag}>')

    def _xml_terminal(self, ttype, tval):
        escaped = ''.join(XML_ESCAPE.get(c) or c for c in tval)
        self._xml.append('  ' * self._indent + f'<{ttype}> {escaped} </{ttype}>')

    def _eat_and_xml(self, expected_val=None, expected_type=None):
        ttype, tval = self._eat(expected_val, expected_type)
        self._xml_terminal(ttype, tval)
        return ttype, tval

    def _new_label(self):
        label = f'L{self._label_counter}'
        self._label_counter += 1
        return label

    def _segment_of(self, kind):
        return VMWriter.KIND_TO_SEGMENT[kind]

    def compile_class(self):
        self.symtab.reset()
        self._xml_open('class')

        self._eat_and_xml('class')
        _, cname = self._eat_and_xml(expected_type='identifier')
        self.classname = cname
        self._eat_and_xml('{')

        while self._peek_val() in ('static', 'field'):
            self._compile_class_var_dec()

        while self._peek_val() in ('constructor', 'function', 'method'):
            self._compile_subroutine_dec()

        self._eat_and_xml('}')
        self._xml_close('class')

        # Write outputs
        xml_path = os.path.join(self.outdir, f'{self.classname}.xml')
        with open(xml_path, 'w') as f:
            f.write('\n'.join(self._xml) + '\n')

        self.vm.close()

    def _compile_class_var_dec(self):
        self._xml_open('classVarDec')

        _, kind_str = self._eat_and_xml()
        kind = kind_str.upper()
        _, type_ = self._eat_and_xml()
        _, name = self._eat_and_xml()
        self.symtab.define(name, type_, kind)

        while self._peek_val() == ',':
            self._eat_and_xml(',')
            _, name = self._eat_and_xml()
            self.symtab.define(name, type_, kind)

        self._eat_and_xml(';')
        self._xml_close('classVarDec')

    def _compile_subroutine_dec(self):
        self._xml_open('subroutineDec')
        self.symtab.start_subroutine()

        _, sub_kind = self._eat_and_xml()
        self._current_subroutine_kind = sub_kind
        self._eat_and_xml()
        _, sub_name = self._eat_and_xml()
        self._current_subroutine_name = f'{self.classname}.{sub_name}'

        if sub_kind == 'method':
            self.symtab.define('this', self.classname, 'ARG')

        self._eat_and_xml('(')
        self._compile_parameter_list()
        self._eat_and_xml(')')

        self._compile_subroutine_body(sub_kind)
        self._xml_close('subroutineDec')

    def _compile_parameter_list(self):
        self._xml_open('parameterList')
        if self._peek_val() != ')':
            _, type_ = self._eat_and_xml()
            _, name = self._eat_and_xml()
            self.symtab.define(name, type_, 'ARG')
            while self._peek_val() == ',':
                self._eat_and_xml(',')
                _, type_ = self._eat_and_xml()
                _, name = self._eat_and_xml()
                self.symtab.define(name, type_, 'ARG')
        self._xml_close('parameterList')

    def _compile_subroutine_body(self, sub_kind):
        self._xml_open('subroutineBody')
        self._eat_and_xml('{')

        while self._peek_val() == 'var':
            self._compile_var_dec()

        n_locals = self.symtab.var_count('VAR')
        self.vm.write_function(self._current_subroutine_name, n_locals)

        if sub_kind == 'constructor':
            n_fields = self.symtab.var_count('FIELD')
            self.vm.write_push('constant', n_fields)
            self.vm.write_call('Memory.alloc', 1)
            self.vm.write_pop('pointer', 0)
        elif sub_kind == 'method':
            self.vm.write_push('argument', 0)
            self.vm.write_pop('pointer', 0)

        self._compile_statements()
        self._eat_and_xml('}')
        self._xml_close('subroutineBody')

    def _compile_var_dec(self):
        self._xml_open('varDec')
        self._eat_and_xml('var')
        _, type_ = self._eat_and_xml()
        _, name = self._eat_and_xml()
        self.symtab.define(name, type_, 'VAR')

        while self._peek_val() == ',':
            self._eat_and_xml(',')
            _, name = self._eat_and_xml()
            self.symtab.define(name, type_, 'VAR')

        self._eat_and_xml(';')
        self._xml_close('varDec')

    def _compile_statements(self):
        self._xml_open('statements')
        while self._peek_val() in ('let', 'if', 'while', 'do', 'return'):
            v = self._peek_val()
            if v == 'let':
                self._compile_let()
            elif v == 'if':
                self._compile_if()
            elif v == 'while':
                self._compile_while()
            elif v == 'do':
                self._compile_do()
            elif v == 'return':
                self._compile_return()
        self._xml_close('statements')

    def _compile_let(self):
        self._xml_open('letStatement')
        self._eat_and_xml('let')
        _, name = self._eat_and_xml()

        is_array = False
        if self._peek_val() == '[':
            is_array = True
            self._eat_and_xml('[')

            entry = self.symtab.lookup(name)
            if entry:
                self.vm.write_push(self._segment_of(entry[1]), entry[2])

            self._compile_expression()
            self.vm.write_arithmetic('add')

            self._eat_and_xml(']')

        self._eat_and_xml('=')
        self._compile_expression()
        self._eat_and_xml(';')

        if is_array:
            self.vm.write_pop('temp', 0)
            self.vm.write_pop('pointer', 1)
            self.vm.write_push('temp', 0)
            self.vm.write_pop('that', 0)
        else:
            entry = self.symtab.lookup(name)
            if entry is None:
                raise NameError(f"Undefined identifier '{name}'")
            self.vm.write_pop(self._segment_of(entry[1]), entry[2])

        self._xml_close('letStatement')

    def _compile_if(self):
        self._xml_open('ifStatement')
        lbl_else = self._new_label()
        lbl_end = self._new_label()

        self._eat_and_xml('if')
        self._eat_and_xml('(')
        self._compile_expression()
        self._eat_and_xml(')')

        self.vm.write_arithmetic('not')
        self.vm.write_if(lbl_else)

        self._eat_and_xml('{')
        self._compile_statements()
        self._eat_and_xml('}')

        self.vm.write_goto(lbl_end)
        self.vm.write_label(lbl_else)

        if self._peek_val() == 'else':
            self._eat_and_xml('else')
            self._eat_and_xml('{')
            self._compile_statements()
            self._eat_and_xml('}')

        self.vm.write_label(lbl_end)
        self._xml_close('ifStatement')

    def _compile_while(self):
        self._xml_open('whileStatement')
        lbl_loop = self._new_label()
        lbl_end = self._new_label()

        self._eat_and_xml('while')
        self.vm.write_label(lbl_loop)

        self._eat_and_xml('(')
        self._compile_expression()
        self._eat_and_xml(')')

        self.vm.write_arithmetic('not')
        self.vm.write_if(lbl_end)

        self._eat_and_xml('{')
        self._compile_statements()
        self._eat_and_xml('}')

        self.vm.write_goto(lbl_loop)
        self.vm.write_label(lbl_end)
        self._xml_close('whileStatement')

    def _compile_do(self):
        self._xml_open('doStatement')
        self._eat_and_xml('do')
        _, name = self._eat_and_xml()
        self._compile_subroutine_call(name)
        self.vm.write_pop('temp', 0)
        self._eat_and_xml(';')
        self._xml_close('doStatement')

    def _compile_return(self):
        self._xml_open('returnStatement')
        self._eat_and_xml('return')
        if self._peek_val() != ';':
            self._compile_expression()
        else:
            self.vm.write_push('constant', 0)
        self._eat_and_xml(';')
        self.vm.write_return()
        self._xml_close('returnStatement')

    def _compile_subroutine_call(self, first_name):
        if self._peek_val() == '(':
            self.vm.write_push('pointer', 0)
            self._eat_and_xml('(')
            nargs = self._compile_expression_list()
            self._eat_and_xml(')')
            self.vm.write_call(f'{self.classname}.{first_name}', nargs + 1)

        elif self._peek_val() == '.':
            self._eat_and_xml('.')
            _, method_name = self._eat_and_xml()

            entry = self.symtab.lookup(first_name)
            if entry is not None:
                obj_type = entry[0]
                self.vm.write_push(self._segment_of(entry[1]), entry[2])
                self._eat_and_xml('(')
                nargs = self._compile_expression_list()
                self._eat_and_xml(')')
                self.vm.write_call(f'{obj_type}.{method_name}', nargs + 1)
            else:
                self._eat_and_xml('(')
                nargs = self._compile_expression_list()
                self._eat_and_xml(')')
                self.vm.write_call(f'{first_name}.{method_name}', nargs)

    def _compile_expression(self):
        self._xml_open('expression')
        self._compile_term()

        while self._peek_val() in ('+', '-', '*', '/', '&', '|', '<', '>', '='):
            _, op = self._eat_and_xml()
            self._compile_term()
            if op == '*':
                self.vm.write_call('Math.multiply', 2)
            elif op == '/':
                self.vm.write_call('Math.divide', 2)
            else:
                self.vm.write_arithmetic(OP_MAP[op])

        self._xml_close('expression')

    def _compile_term(self):
        self._xml_open('term')
        ttype, tval = self._cur()

        if ttype == 'integerConstant':
            self._eat_and_xml()
            self.vm.write_push('constant', int(tval))

        elif ttype == 'stringConstant':
            self._eat_and_xml()
            self.vm.write_push('constant', len(tval))
            self.vm.write_call('String.new', 1)
            for ch in tval:
                self.vm.write_push('constant', ord(ch))
                self.vm.write_call('String.appendChar', 2)

        elif ttype == 'keyword' and tval in KEYWORD_CONSTANTS:
            self._eat_and_xml()
            if tval == 'true':
                self.vm.write_push('constant', 0)
                self.vm.write_arithmetic('not')
            elif tval in ('false', 'null'):
                self.vm.write_push('constant', 0)
            elif tval == 'this':
                self.vm.write_push('pointer', 0)

        elif tval == '(':
            self._eat_and_xml('(')
            self._compile_expression()
            self._eat_and_xml(')')

        elif tval in ('-', '~'):
            _, op = self._eat_and_xml()
            self._compile_term()
            self.vm.write_arithmetic(UNARY_OP_MAP[op])

        elif ttype == 'identifier':
            _, name = self._eat_and_xml()
            if self._peek_val() == '[':
                self._eat_and_xml('[')
                entry = self.symtab.lookup(name)
                if entry is None:
                    raise NameError(f"Undefined identifier '{name}'")
                self.vm.write_push(self._segment_of(entry[1]), entry[2])
                self._compile_expression()
                self.vm.write_arithmetic('add')
                self.vm.write_pop('pointer', 1)
                self.vm.write_push('that', 0)
                self._eat_and_xml(']')
            elif self._peek_val() in ('(', '.'):
                self._compile_subroutine_call(name)
            else:
                entry = self.symtab.lookup(name)
                if entry is None:
                    raise NameError(f"Undefined identifier '{name}'")
                self.vm.write_push(self._segment_of(entry[1]), entry[2])

        self._xml_close('term')

    def _compile_expression_list(self):
        self._xml_open('expressionList')
        nargs = 0
        if self._peek_val() != ')':
            self._compile_expression()
            nargs = 1
            while self._peek_val() == ',':
                self._eat_and_xml(',')
                self._compile_expression()
                nargs += 1
        self._xml_close('expressionList')
        return nargs