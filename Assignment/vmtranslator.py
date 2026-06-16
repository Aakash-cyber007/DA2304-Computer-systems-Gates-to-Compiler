import os

class VMReader:
    ARITH = "A"
    PUSH = "PUSH"
    POP = "POP"
    LABEL = "LBL"
    GOTO = "GOTO"
    IF = "IF"
    FUNCTION = "FUNC"
    RETURN = "RET"
    CALL = "CALL"

    ops = {"add","sub","neg","eq","gt","lt","and","or","not"}

    def __init__(self, path):
        with open(path) as f:
            raw = f.readlines()

        self.lines = []
        for l in raw:
            clean = l.split("//")[0].strip()
            if clean:
                self.lines.append(clean)

        self.ptr = -1
        self.curr = None

    def hasNext(self):
        return self.ptr < len(self.lines) - 1

    def advance(self):
        if self.hasNext():
            self.ptr += 1
            self.curr = self.lines[self.ptr]

    def type(self):
        c = self.curr.split()[0]
        if c in self.ops: return self.ARITH
        if c == "push": return self.PUSH
        if c == "pop": return self.POP
        if c == "label": return self.LABEL
        if c == "goto": return self.GOTO
        if c == "if-goto": return self.IF
        if c == "function": return self.FUNCTION
        if c == "return": return self.RETURN
        if c == "call": return self.CALL
        raise ValueError("Unknown command")

    def arg1(self):
        parts = self.curr.split()
        if self.type() == self.ARITH:
            return parts[0]
        return parts[1]

    def arg2(self):
        parts = self.curr.split()
        return int(parts[2])


class AssemblyBuilder:

    segMap = {
        "local": "LCL",
        "argument": "ARG",
        "this": "THIS",
        "that": "THAT"
    }

    def __init__(self, outPath):
        self.outPath = outPath
        self.code = []
        self.labelId = 0
        self.callId = 0
        self.currentFunc = ""
        self.fileTag = ""

    def setFile(self, fname):
        self.fileTag = os.path.splitext(os.path.basename(fname))[0]
    def bootstrap(self):
        self.code += ["@256","D=A","@SP","M=D"]
        self.callFunc("Sys.init", 0)

    def pushD(self):
        return ["@SP","A=M","M=D","@SP","M=M+1"]

    def popToD(self):
        return ["@SP","AM=M-1","D=M"]

    # -------- Arithmetic --------
    def writeMath(self, op):
        if op == "add": self.code += self._bin("D+M")
        elif op == "sub": self.code += self._bin("M-D")
        elif op == "and": self.code += self._bin("D&M")
        elif op == "or": self.code += self._bin("D|M")
        elif op == "neg": self.code += ["@SP","A=M-1","M=-M"]
        elif op == "not": self.code += ["@SP","A=M-1","M=!M"]
        else:
            self.code += self._cmp(op)

    def _bin(self, expr):
        return ["@SP","AM=M-1","D=M","A=A-1",f"M={expr}"]

    def _cmp(self, kind):
        lbl = f"CMP{self.labelId}"
        self.labelId += 1
        end = lbl + "_END"

        jump = {"eq":"JEQ","gt":"JGT","lt":"JLT"}[kind]

        return [
            "@SP","AM=M-1","D=M","A=A-1","D=M-D",
            f"@{lbl}",f"D;{jump}",
            "@SP","A=M-1","M=0",
            f"@{end}","0;JMP",
            f"({lbl})","@SP","A=M-1","M=-1",
            f"({end})"
        ]

    def writePushPop(self, cmd, seg, idx):
        if cmd == VMReader.PUSH:
            self._push(seg, idx)
        else:
            self._pop(seg, idx)

    def _push(self, seg, idx):
        if seg == "constant":
            self.code += [f"@{idx}","D=A"]
        elif seg in self.segMap:
            self.code += [f"@{self.segMap[seg]}","D=M",f"@{idx}","A=D+A","D=M"]
        elif seg == "temp":
            self.code += [f"@{5+idx}","D=M"]
        elif seg == "pointer":
            self.code += [f"@{'THIS' if idx==0 else 'THAT'}","D=M"]
        elif seg == "static":
            self.code += [f"@{self.fileTag}.{idx}","D=M"]

        self.code += self.pushD()

    def _pop(self, seg, idx):
        if seg in self.segMap:
            self.code += [f"@{self.segMap[seg]}","D=M",f"@{idx}","D=D+A"]
        elif seg == "temp":
            self.code += [f"@{5+idx}","D=A"]
        elif seg == "pointer":
            self.code += [f"@{3+idx}","D=A"]
        elif seg == "static":
            self.code += [f"@{self.fileTag}.{idx}","D=A"]

        self.code += ["@R13","M=D"]
        self.code += self.popToD()
        self.code += ["@R13","A=M","M=D"]

    # -------- Flow --------
    def label(self, name):
        self.code.append(f"({self._scope(name)})")

    def goTo(self, name):
        self.code += [f"@{self._scope(name)}","0;JMP"]

    def ifGo(self, name):
        self.code += self.popToD() + [f"@{self._scope(name)}","D;JNE"]

    # -------- Functions --------
    def defineFunc(self, name, k):
        self.currentFunc = name
        self.code.append(f"({name})")
        for _ in range(k):
            self.code += ["@SP","M=M+1","A=M-1","M=0"]

    def callFunc(self, name, n):
        ret = f"{name}$ret{self.callId}"
        self.callId += 1

        self.code += [f"@{ret}","D=A"] + self.pushD()

        for seg in ["LCL","ARG","THIS","THAT"]:
            self.code += [f"@{seg}","D=M"] + self.pushD()

        self.code += [
            "@SP","D=M",f"@{n+5}","D=D-A","@ARG","M=D",
            "@SP","D=M","@LCL","M=D",
            f"@{name}","0;JMP",
            f"({ret})"
        ]

    def doReturn(self):
        self.code += ["@LCL","D=M","@R14","M=D"]
        self.code += ["@5","A=D-A","D=M","@R15","M=D"]

        self.code += self.popToD() + ["@ARG","A=M","M=D"]
        self.code += ["@ARG","D=M+1","@SP","M=D"]

        for seg in ["THAT","THIS","ARG","LCL"]:
            self.code += ["@R14","AM=M-1","D=M",f"@{seg}","M=D"]

        self.code += ["@R15","A=M","0;JMP"]
    def _scope(self, label):
        return f"{self.currentFunc}${label}" if self.currentFunc else label

    def save(self):
        with open(self.outPath,"w") as f:
            f.write("\n".join(self.code) + "\n")