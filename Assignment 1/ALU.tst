load ALU.hdl,
output-file ALU_MUL.out,
compare-to ALU_MUL.cmp,
output-list x%B1.16.1 y%B1.16.1 zx%B1.1.1 nx%B1.1.1 zy%B1.1.1 ny%B1.1.1 f%B1.1.1 no%B1.1.1 out%B1.16.1;

// Test standard operations with x=6, y=7
set x 6, set y 7,

// 0
set zx 1, set nx 0, set zy 1, set ny 0, set f 1, set no 0, eval, output;
// 1
set zx 1, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;
// -1
set zx 1, set nx 1, set zy 1, set ny 0, set f 1, set no 0, eval, output;
// x
set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 0, eval, output;
// y
set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 0, eval, output;
// !x
set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 1, eval, output;
// !y
set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 1, eval, output;
// -x
set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 1, eval, output;
// -y
set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;
// x+1
set zx 0, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;
// y+1
set zx 1, set nx 1, set zy 0, set ny 1, set f 1, set no 1, eval, output;
// x-1
set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 0, eval, output;
// y-1
set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 0, eval, output;
// x+y
set zx 0, set nx 0, set zy 0, set ny 0, set f 1, set no 0, eval, output;
// x-y
set zx 0, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;
// y-x
set zx 0, set nx 0, set zy 0, set ny 1, set f 1, set no 1, eval, output;
// x&y
set zx 0, set nx 0, set zy 0, set ny 0, set f 0, set no 0, eval, output;
// x|y
set zx 0, set nx 1, set zy 0, set ny 1, set f 0, set no 1, eval, output;

// ---- MULTIPLIER TESTS (Signature: zx=0, nx=1, zy=0, ny=1, f=1) ----
// Note: no=0 returns LO, no=1 returns HI (based on our ALU.hdl integration)

// 3 * 4 = 12
set x 3, set y 4, set zx 0, set nx 1, set zy 0, set ny 1, set f 1, set no 0, eval, output;
// 10 * 10 = 100
set x 10, set y 10, set zx 0, set nx 1, set zy 0, set ny 1, set f 1, set no 0, eval, output;
// 255 * 255 = 65025 (lo: 1111111000000001, hi: 0)
set x 255, set y 255, set zx 0, set nx 1, set zy 0, set ny 1, set f 1, set no 0, eval, output;
set no 1, eval, output;