import os
import sys
import glob
import getopt
import subprocess

def split(n, ifile, outputdir):
    line_count = int(subprocess.Popen("wc -l %s" % ifile,
                                      shell=True, stdout=subprocess.PIPE).stdout.read().split()[0].strip())
    lines_per_file = line_count / n
    subprocess.Popen("gsplit -d --lines=%d %s %s/part." % (lines_per_file+1, ifile, outputdir), shell=True)


n = 22
# inputfile = "../../../data/human_bios_newyork.txt"
inputfile = "../../../data/human_bios_texas.txt"
keyfile = "./faceplusplus_api_keys.txt"

# directory
KEYDIR = "keys"
OUTDIR = "crawled"
RETRYDIR = "retry"
CURSORDIR = "cursors"
LOGDIR = "logs"
DATADIR = "./data"

for target_dir in [OUTDIR, RETRYDIR, CURSORDIR, LOGDIR, DATADIR, KEYDIR]:
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

split(n, inputfile, DATADIR)
split(n, keyfile, KEYDIR)

with open("run.sh", "w") as fo:
    for i in range(0, n):
        fo.write("python profile-image-detection.py %d > logs/%.2d.log &\n" % (i, i))
        # fo.write("python retry-profile-image-detection.py %d > logs/%.2d.log &\n" % (i, i))
        fo.write("PID=$!\n")
        fo.write("echo \"kill -9 ${PID}\" >> kill.sh\n")
    fo.write("echo \"rm kill.sh\" >> kill.sh\n")
