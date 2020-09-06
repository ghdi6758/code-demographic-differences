#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import getopt
import subprocess
from sys import platform as _platform
import json
import math

def split(n, input_file, output_dir):
    """split key/input files for distributed crawlers"""
    p1 = subprocess.Popen(["wc", "-l", "%s" % input_file], stdout=subprocess.PIPE)
    line_count = int(p1.communicate()[0].split()[0].strip())
    lines_per_file = math.floor(line_count/float(n))

    if _platform == "darwin":
        # osx
        # if you don't have gsplit (core-utils), please read https://www.topbug.net/blog/2013/04/14/install-and-use-gnu-command-line-tools-in-mac-os-x/
        subprocess.Popen(["gsplit", "-d", "--lines=%d" % lines_per_file, input_file, "%s/%s." % (output_dir, os.path.basename(input_file))])
    elif  _platform == "linux" or _platform == "linux2":
        # linux
        subprocess.Popen(["split", "-d", "--lines=%d" % lines_per_file, input_file, "%s/%s." % (output_dir, os.path.basename(input_file))])
    else:
        # windows
        print "Please install http://gnuwin32.sourceforge.net/packages/coreutils.htm"
        subprocess.Popen(["split.exe", "-d", "--lines=%d" % lines_per_file+1, input_file, "%s/%s." % (output_dir, os.path.basename(input_file))])

if __name__ == "__main__":
    with open("config.json") as fi:
        config = json.loads(fi.read())

    if config['crawling'] != "SocialGraph":
        print "incorrect config file.  Please check."
        exit()

    for target in config:
        if "_dir" in target:
            if not os.path.exists(config[target]):
                os.mkdir(config[target])
                
    split(config["number_of_crawlers"], config["key_file"], config["key_dir"])
    split(config["number_of_crawlers"], config["input_file"], config["input_dir"])
    split(config["number_of_crawlers"], config["proxy_file"], config["proxy_dir"])

    with open("run.sh", "w") as fo:
        for i in range(0, config["number_of_crawlers"]):
            # python HTweetCrawler.py -n 1 -k testkey -i remaining.txt -o temp.txt -e error.txt -t status.conf -m 3200 -s True
            fo.write("python HSocialGraphCrawler.py %d &\n" % i)
            fo.write("PID=$!\n")
            fo.write("echo \"kill -9 ${PID}\" >> kill.sh\n")
        fo.write("echo \"rm kill.sh\" >> kill.sh\n")
