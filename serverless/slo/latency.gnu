set loadpath '../plot/config'
load 'dark2.pal'
set terminal pngcairo size 520, 360
set output fname."-latency.png"
set datafile separator "\t"
set key left top
set title plot_title
set ylabel y_title
set xlabel 'Batch size'

plot "latency/".fname.".txt" using 1 with point title '' ls 1