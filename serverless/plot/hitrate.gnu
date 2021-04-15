set loadpath './config'
load 'dark2.pal'
set terminal pngcairo size 560, 450
set output "latency-rate.png"
set datafile separator "\t"
set key top left
set title 'Latency CDF under diff. hit rates'
set xlabel 'Latency (seconds)'
set ylabel 'percentage'
plot "processed/vgg/latency/0.txt"    using 1:2 with l title "hit = 0.00" ls 1 lw 2.5 dt 4, \
     "processed/vgg/latency/0.25.txt" using 1:2 with l title "hit = 0.25" ls 2 lw 2.5 dt 5, \
     "processed/vgg/latency/0.5.txt"  using 1:2 with l title "hit = 0.50" ls 3 lw 2.5 dt 2, \
     "processed/vgg/latency/0.75.txt" using 1:2 with l title "hit = 0.75" ls 7 lw 2.5 dt 1