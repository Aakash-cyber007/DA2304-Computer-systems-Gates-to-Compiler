class SymbolTable:

    def __init__(self):
        self.class_scope = {}      # name -> (type, kind, index)
        self.sub_scope = {}        # name -> (type, kind, index)
        self._counts = {'STATIC': 0, 'FIELD': 0, 'ARG': 0, 'VAR': 0}

    def start_subroutine(self):
        self.sub_scope = {}
        self._counts['ARG'] = 0
        self._counts['VAR'] = 0

    def reset(self):
        self.class_scope = {}
        self.sub_scope = {}
        self._counts = {'STATIC': 0, 'FIELD': 0, 'ARG': 0, 'VAR': 0}

    def define(self, name, type_, kind):
        idx = self._counts[kind]
        entry = (type_, kind, idx)
        if kind in ('STATIC', 'FIELD'):
            self.class_scope[name] = entry
        else:
            self.sub_scope[name] = entry
        self._counts[kind] += 1

    def lookup(self, name):
        if name in self.sub_scope:
            return self.sub_scope[name]
        if name in self.class_scope:
            return self.class_scope[name]
        return None

    def var_count(self, kind):
        return self._counts.get(kind, 0)

    def kind_of(self, name):
        entry = self.lookup(name)
        return entry[1] if entry else None

    def type_of(self, name):
        entry = self.lookup(name)
        return entry[0] if entry else None

    def index_of(self, name):
        entry = self.lookup(name)
        return entry[2] if entry else None

    def dump(self):
        lines = ["=== Class scope ==="]
        for n, (t, k, i) in sorted(self.class_scope.items()):
            lines.append(f"  {n:20s}  type={t:12s}  kind={k:8s}  index={i}")
        lines.append("=== Subroutine scope ===")
        for n, (t, k, i) in sorted(self.sub_scope.items()):
            lines.append(f"  {n:20s}  type={t:12s}  kind={k:8s}  index={i}")
        return '\n'.join(lines)
