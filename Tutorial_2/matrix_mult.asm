// Matrix A (RAM 16 to 24) [Row-Major]
// Values: 1, 2, 3, 4, 5, 6, 7, 8, 9
@1
D=A
@16
M=D
@2
D=A
@17
M=D
@3
D=A
@18
M=D
@4
D=A
@19
M=D
@5
D=A
@20
M=D
@6
D=A
@21
M=D
@7
D=A
@22
M=D
@8
D=A
@23
M=D
@9
D=A
@24
M=D

// Matrix B (RAM 25 to 33) [Column-Major]
// Column 0 (indices 0,1,2)
@1
D=A
@25
M=D      // B[0][0] = 1
@0
D=A
@26
M=D      // B[1][0] = 0
@0
D=A
@27
M=D      // B[2][0] = 0

// Column 1
@0
D=A
@28
M=D      // B[0][1] = 0
@1
D=A
@29
M=D      // B[1][1] = 1
@0
D=A
@30
M=D      // B[2][1] = 0

// Column 2
@0
D=A
@31
M=D      // B[0][2] = 0
@0
D=A
@32
M=D      // B[1][2] = 0
@1
D=A
@33
M=D      // B[2][2] = 1

// MAIN MULTIPLICATION LOGIC
// R0 = i (row counter 0-2)
// R1 = j (col counter 0-2)
// R2 = k (dot product counter 0-2)
// R3 = sum
// R4 = A pointer
// R5 = B pointer
// R6 = C pointer (starts at 34)
// R7 = A row base
// R8 = B column base
// R12 = Temp variable for swapping

// Initialize C_PTR = 34
@34
D=A
@R6
M=D

// Initialize i = 0
@0
D=A
@R0
M=D

(LOOP_I)
// if i == 3, end
@R0
D=M
@3
D=D-A
@END
D;JEQ

// Initialize A_ROW_BASE = 16 + (i * 3)
@R0
D=M      // D = i (A is 0)
D=D+M    // D = i * 2 
D=D+M    // D = i * 3 
@16
D=D+A    // D = 16 + (i * 3)
@R7
M=D      // Store result in R7

// Initialize j = 0
@0
D=A
@R1
M=D

(LOOP_J)
// if j == 3, go to next row
@R1
D=M
@3
D=D-A
@LOOP_I_END
D;JEQ

// Initialize sum = 0
@0
D=A
@R3
M=D

// Initialize B_COL_BASE = 25 + (j * 3)
@R1
D=M      // D = j (A is 1)
D=D+M    // D = j * 2 
D=D+M    // D = j * 3
@25
D=D+A    // D = 25 + (j * 3)
@R8
M=D      // Store result in R8

// Initialize k = 0
@0
D=A
@R2
M=D

// Set A_PTR to start of current row
@R7
D=M
@R4
M=D

(LOOP_K)
// if k == 3, done with dot product
@R2
D=M
@3
D=D-A
@STORE_RESULT
D;JEQ

// Load A[k] - A_PTR points to A[i][k]
@R4
A=M
D=M
@R9
M=D

// Load B[k] - B_PTR points to B[k][j]
@R8
D=M
@R2
D=D+M      // B_COL_BASE + k
A=D
D=M
@R10
M=D

//NEW OPTIMIZATION: SWAP IF R9 < R10
@R9
D=M
@R10
D=D-M
@NO_SWAP
D;JGE      // If R9 >= R10, proceed without swapping

// Swap R9 and R10 using R12 as a temporary register
@R9
D=M
@R12
M=D        // R12 = R9
@R10
D=M
@R9
M=D        // R9 = R10
@R12
D=M
@R10
M=D        // R10 = R12

(NO_SWAP)
// ------------------------------------------

// Multiply R9 * R10 and add to sum
// Using repeated addition
@R9
D=M
@R11
M=D      // Store multiplicand
@R10
D=M
@MULT_END
D;JLE    // If multiplier <= 0, skip

(MULT_LOOP)
@R11
D=M
@R3
M=D+M    // ADDITION FIX: Standard syntax D+M
@R10
M=M-1    // decrement multiplier
D=M
@MULT_LOOP
D;JGT

(MULT_END)
// Advance A pointer to next column
@R4
M=M+1

// Increment k
@R2
M=M+1
@LOOP_K
0;JMP

(STORE_RESULT)
// Store sum in C[i][j]
@R3
D=M
@R6
A=M
M=D

// Advance C pointer
@R6
M=M+1

// Increment j
@R1
M=M+1
@LOOP_J
0;JMP

(LOOP_I_END)
// Increment i
@R0
M=M+1
@LOOP_I
0;JMP

(END)
@END
0;JMP
