set term postscript eps enhanced color 27
# set term fig
set key bottom right
#unset key
set size 1,1
set border 3
set xtics nomirror
set ytics nomirror

###This style is for boxes###

set style line 1 pt 4 lt 1 lw 3 lc rgb "red" ps 2.0
set style line 2 pt 6 lt 3 lw 3 lc rgb "black" ps 2.0
set style line 3 pt 3 lt 7 lw 3 lc rgb "blue" ps 2.0

#set style line 1 pt 3 lt 1 lw 9 lc rgb "black" ps 2.0
#set style line 2 pt 5 lt 7 lw 9 lc rgb "brown" ps 2.0
#set style line 3 pt 6 lt 1 lw 5 lc rgb "orange" ps 2.0
#set style line 4 pt 5 lt 1 lc rgb "white" ps 1.0

set output 'tweets_status_count_cdf.eps'
set xlabel 'ntweets in bio'
set ylabel 'CDF'
#set yrange[0.3:1]
#set xrange[0:1]



set log x
#set log y
#set xrange [1:1001]


set xtics font "Roman-Times,22"
set ytics font "Roman-Times,22"

#set format x "10^{%L}"
#set format y "10^{%L}"

#set style fill solid 1.00 border 1
#set boxwidth 0.5 absolute
#set style histogram clustered gap 1
#set key bmargin center horizontal Left
#set logscale x
#set xtics (1, 10, 20, 30, 40, 50, 60, 70, 80)
#set style data histograms


plot "./tweets_status_count_newyork.cdf" using ($1):($2) t 'New York' w l ls 1, \
"../05_tweets_texas/tweets_status_count_texas.cdf" using ($1):($2) t 'Texas' w l ls 3,
