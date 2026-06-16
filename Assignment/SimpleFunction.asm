(SimpleFunction.test)

@0
D = A
@SP
A = M
M = D
@SP
M = M+1

@0
D = A
@SP
A = M
M = D
@SP
M = M+1

@0
D = A
@LCL
A = M+D
D = M
@SP
A = M
M = D
@SP
M = M+1

@1
D = A
@LCL
A = M+D
D = M
@SP
A = M
M = D
@SP
M = M+1

@SP
M = M-1
A = M
D = M
A = A-1
M = M+D

@SP
M = M-1
A = M
M = !M
@SP
M = M+1

@0
D = A
@ARG
A = M+D
D = M
@SP
A = M
M = D
@SP
M = M+1

@SP
M = M-1
A = M
D = M
A = A-1
M = M+D

@1
D = A
@ARG
A = M+D
D = M
@SP
A = M
M = D
@SP
M = M+1

@SP
M = M-1
A = M
D = M
A = A-1
M = M-D

@LCL
D = M
@R13
M = D
@5
A = D-A
D = M
@R14
M = D
@SP
M = M-1
A = M
D = M
@ARG
A = M
M = D
@ARG
D = M+1
@SP
M = D

@R13
M = M-1
A = M
D = M
@THAT
M = D


@R13
M = M-1
A = M
D = M
@THIS
M = D


@R13
M = M-1
A = M
D = M
@ARG
M = D


@R13
M = M-1
A = M
D = M
@LCL
M = D

@R14
A = M
0;JMP

(END_PROGRAM)
@END_PROGRAM
0;JMP
