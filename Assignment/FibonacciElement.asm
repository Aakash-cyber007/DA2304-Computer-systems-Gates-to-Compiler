
@256
D=A
@SP
M=D

@Sys.init_ret.0
D = A
@SP
A = M
M = D
@SP
M = M+1

@LCL
D = M
@SP
A = M
M = D
@SP
M = M+1


@ARG
D = M
@SP
A = M
M = D
@SP
M = M+1


@THIS
D = M
@SP
A = M
M = D
@SP
M = M+1


@THAT
D = M
@SP
A = M
M = D
@SP
M = M+1

@SP
D = M
@0
D = D-A
@5
D = D-A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Sys.init
0;JMP
(Sys.init_ret.0)
(Main.fibonacci)

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

@2
D = A
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
D = M-D
@COMP_0
D;JLT
@SP
A = M-1
M = 0
@COMP_END_0
0;JMP
(COMP_0)
@SP
A = M-1
M=-1
(COMP_END_0)

@SP
M = M-1
A = M
D = M
@Main.fibonacci_N_LT_2
D;JNE

@Main.fibonacci_N_GE_2
0;JMP
(Main.fibonacci_N_LT_2)

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
(Main.fibonacci_N_GE_2)

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

@2
D = A
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

@Main.fibonacci_ret.1
D = A
@SP
A = M
M = D
@SP
M = M+1

@LCL
D = M
@SP
A = M
M = D
@SP
M = M+1


@ARG
D = M
@SP
A = M
M = D
@SP
M = M+1


@THIS
D = M
@SP
A = M
M = D
@SP
M = M+1


@THAT
D = M
@SP
A = M
M = D
@SP
M = M+1

@SP
D = M
@1
D = D-A
@5
D = D-A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Main.fibonacci
0;JMP
(Main.fibonacci_ret.1)

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

@1
D = A
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

@Main.fibonacci_ret.2
D = A
@SP
A = M
M = D
@SP
M = M+1

@LCL
D = M
@SP
A = M
M = D
@SP
M = M+1


@ARG
D = M
@SP
A = M
M = D
@SP
M = M+1


@THIS
D = M
@SP
A = M
M = D
@SP
M = M+1


@THAT
D = M
@SP
A = M
M = D
@SP
M = M+1

@SP
D = M
@1
D = D-A
@5
D = D-A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Main.fibonacci
0;JMP
(Main.fibonacci_ret.2)

@SP
M = M-1
A = M
D = M
A = A-1
M = M+D

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
(Sys.init)

@4
D = A
@SP
A = M
M = D
@SP
M = M+1

@Main.fibonacci_ret.3
D = A
@SP
A = M
M = D
@SP
M = M+1

@LCL
D = M
@SP
A = M
M = D
@SP
M = M+1


@ARG
D = M
@SP
A = M
M = D
@SP
M = M+1


@THIS
D = M
@SP
A = M
M = D
@SP
M = M+1


@THAT
D = M
@SP
A = M
M = D
@SP
M = M+1

@SP
D = M
@1
D = D-A
@5
D = D-A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Main.fibonacci
0;JMP
(Main.fibonacci_ret.3)
(Sys.init_END)

@Sys.init_END
0;JMP

(END_PROGRAM)
@END_PROGRAM
0;JMP
