#!/usr/bin/python

##Last modified: 2009/04/08

##This nk.py groups and counts tuples of the same value of the pivot column.
##The index of the pivot column begins at 0.
##That is, the column index of the leftmost column of the file is 0.

## example:

## input_file: [cyworld_node.deg]
## 1    37
## 2    34
## 3    37
## 4    8
## 5    21

## haewoon@an $ nk.py cyworld_node.deg 1

## output_file: [cyworld_node.deg.nk]
## 8 1
## 21 1
## 34 1
## 37 2

import sys
import glob
from collections import defaultdict

city = "newyork"
choice = 1
afile = "./tweets_coverage_status_data_prop_%s.txt" % (city)
# screen_name, str(statuses_count), (num_tweets), str(prop)
# op = open('tweets_coverage_%s.cdf' % (city), 'w')
op = open('tweets_status_count_%s.cdf' % (city), 'w')

pk = defaultdict(int)

with open (afile) as fi:
    next(fi)
    for line in fi:
        degree = float(line.split("\t")[choice].strip())
        pk[degree] += 1
    fi.close()

tot=0
for degree in sorted(pk):
    tot += float(pk[degree])

prop = defaultdict(float)
for degree in sorted(pk):
    prop[degree] = (float(pk[degree])/tot)


pkc = []
idx = 1
for degree in sorted(prop):
    pkc.append([float(degree), float(prop[degree])])

j = len(pkc)
for i in range(j):
    if i == 0:
        pkc[i][1] = pkc[i][1]
    else:
        pkc[i][1] = pkc[i-1][1] + pkc[i][1]


for i in range(len(pkc)):
    op.write(str(pkc[i][0]) + ' ' + str(pkc[i][1]) + '\n')
op.close()