load approachB.asm,
output-file MatmulTest.out,
compare-to MatmulTest.cmp,

set RAM[2000] 1,
set RAM[2001] 2,
set RAM[2002] 3,
set RAM[2003] 4,

set RAM[2010] 5,
set RAM[2011] 6,
set RAM[2012] 7,
set RAM[2013] 8,

set RAM[2020] 10,
set RAM[2021] 20,
set RAM[2022] 30,
set RAM[2023] 40,

set RAM[2030] 0,
set RAM[2031] 0,
set RAM[2032] 0,
set RAM[2033] 0,

repeat 50000 {
	ticktock;
}

output-list RAM[2030]%D1.9.1 RAM[2031]%D1.9.1 RAM[2032]%D1.9.1 RAM[2033]%D1.9.1;
output;