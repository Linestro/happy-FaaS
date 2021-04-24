set loadpath './config'
load 'dark2.pal'
set terminal png size 520, 300
set output "thruput.png"
set datafile separator "\t"
set boxwidth 0.5
set style fill solid
set yrange [0:2.2]
set title 'Normalized throughput: LRU vs. FIFO vs. base'
set ylabel '#images/s (normalized)'
plot "processed/vgg/thruput/thruput.txt" using 2:xtic(1) with boxes ls 3 title '', \
     "processed/vgg/thruput/thruput.txt" using 0:2:(strcol(2).'x') w labels offset 0, 0.5 notitle
