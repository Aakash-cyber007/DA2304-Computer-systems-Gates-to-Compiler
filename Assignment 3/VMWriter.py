import os


class VMWriter:
    KIND_TO_SEGMENT = {
        'STATIC': 'static',
        'FIELD':  'this',
        'ARG':    'argument',
        'VAR':    'local',
    }

    def __init__(self, outpath):
        self.outpath = outpath
        self._lines = []

    def write_push(self, segment, index):
        self._lines.append(f'push {segment} {index}')

    def write_pop(self, segment, index):
        self._lines.append(f'pop {segment} {index}')

    def write_arithmetic(self, command):
        self._lines.append(command)

    def write_label(self, label):
        self._lines.append(f'label {label}')

    def write_goto(self, label):
        self._lines.append(f'goto {label}')

    def write_if(self, label):
        self._lines.append(f'if-goto {label}')

    def write_call(self, name, nargs):
        self._lines.append(f'call {name} {nargs}')

    def write_function(self, name, nlocals):
        self._lines.append(f'function {name} {nlocals}')

    def write_return(self):
        self._lines.append('return')

    def close(self):
        with open(self.outpath, 'w') as f:
            f.write('\n'.join(self._lines) + '\n')

    def get_vm(self):
        return '\n'.join(self._lines) + '\n'
