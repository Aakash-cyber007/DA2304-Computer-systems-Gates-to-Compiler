load Multiplier.hdl,
output-file Multiplier.out,
compare-to Multiplier.cmp,
output-list a%B1.16.1 b%B1.16.1 lo%B1.16.1 hi%B1.16.1;

set a 0, set b 0, eval, output;
set a 1, set b 1, eval, output;
set a 2, set b 3, eval, output;
set a 10, set b 10, eval, output;
set a 255, set b 255, eval, output;
set a 1000, set b 5, eval, output;
set a 32767, set b 2, eval, output;
set a 1234, set b 5678, eval, output;
set a 65535, set b 1, eval, output;
set a 65535, set b 65535, eval, output;