set terminal png size 600, 400
set output filename.".png"
set datafile separator "\t"
set key top left
plot filename using 1:2 with l title filename lt 6 lw 2