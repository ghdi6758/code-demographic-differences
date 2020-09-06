import os
import sys
import glob
import getopt
import subprocess

n=30

# directory
OUTDIR = "crawled"
RETRYDIR = "retry"
CURSORDIR = "cursors"
LOGDIR = "logs"
for target_dir in [OUTDIR, RETRYDIR, CURSORDIR, LOGDIR]:
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

with open("run.sh", "w") as fo:
    for i in range(0, n):
        fo.write("python 01_followermonk_new.py %d > logs/%.2d.log &\n" % (i, i))
        fo.write("PID=$!\n")
        fo.write("echo \"kill -9 ${PID}\" >> kill.sh\n")
    fo.write("echo \"rm kill.sh\" >> kill.sh\n")

