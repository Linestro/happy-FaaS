set loadpath '../plot/config'
load 'dark2.pal'
set terminal pngcairo size 520, 360
set output fname."-thruput.png"
set datafile separator "\t"
set key left top
if (fname eq 'inception') {
    set key bottom right
}
set title plot_title
set ylabel y_title
set xlabel 'Progress %'
set xtics 0,0.25,1

if (fname eq 'inception') {
    plot "thruput/".fname.".txt.0" using 1:2 with l title "1s" ls 1 lw 2 dt 1, \
         "thruput/".fname.".txt.1" using 1:2 with l title "2s" ls 2 lw 2 dt 2, \
         "thruput/".fname.".txt.2" using 1:2 with l title "4s" ls 4 lw 2 dt 4
} else {
    plot "thruput/".fname.".txt.0" using 1:2 with l title "0.5s" ls 1 lw 2 dt 1, \
         "thruput/".fname.".txt.1" using 1:2 with l title "1s"   ls 2 lw 2 dt 2, \
         "thruput/".fname.".txt.2" using 1:2 with l title "2s"   ls 4 lw 2 dt 4, \
         "thruput/".fname.".txt.3" using 1:2 with l title "4s"   ls 8 lw 2 dt 5
}
