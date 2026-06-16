load And.hdl,
output-file And.out,
compare-to And.cmp,
output-list A B out;

set A 0, set B 0, eval, output;
set A 0, set B 1, eval, output;
set A 1, set B 0, eval, output;
set A 1, set B 1, eval, output;
