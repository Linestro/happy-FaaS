set loadpath './config'
load 'dark2.pal'
set terminal pngcairo size 500, 350
set output "latency-algo.png"
set datafile separator "\t"
set key top left
set title 'Latency CDF: base vs. LRU vs. FIFO'
set xlabel 'Latency (seconds)'
set ylabel 'percentage'
plot "processed/vgg/latency/base.txt" using 1:2 with l title "base" ls 1 lw 2 dt 2, \
     "processed/vgg/latency/lru.txt"  using 1:2 with l title "lru"  ls 3 lw 2 dt 1, \
     "processed/vgg/latency/fifo.txt"  using 1:2 with l title "fifo"  ls 2 lw 2 dt 4