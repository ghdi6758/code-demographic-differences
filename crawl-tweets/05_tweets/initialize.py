import os
import sys
import glob
import getopt
import subprocess


def parse_argv(argv):
    try:
        opts, args = getopt.getopt(argv, "hn:k:i:")
    except getopt.GetoptError:
        print "usage: python initialize.py -n <number_of_crawlers> -k <keyfile> -i <inputfile>"
        sys.exit()

    for opt, arg in opts:
        if opt == "-h":
            print "usage: python initialize.py -n <number_of_crawlers> -k <keyfile> -i <inputfile>"
            sys.exit()
        elif opt == "-n":
            n = int(arg)
        elif opt == "-k":
            keyfile = arg
        elif opt == "-i":
            inputfile = arg

    return n, keyfile, inputfile


# def split(n, ifile, outputdir):
#     line_count = int(subprocess.Popen("wc -l %s" % ifile,
#                                       shell=True, stdout=subprocess.PIPE).stdout.read().split()[0].strip())
#     lines_per_file = line_count / n
#     subprocess.Popen("gsplit -d --lines=%d %s %s/part." % (lines_per_file+1, ifile, outputdir), shell=True)

def split(n, input_file, output_dir):
    """split key/input files for distributed crawlers"""
    p1 = subprocess.Popen(["wc", "-l", "%s" % input_file], stdout=subprocess.PIPE)
    line_count = int(p1.communicate()[0].split()[0].strip())
    lines_per_file = math.ceil(line_count/float(n))

    if _platform == "darwin":
        # osx
        # if you don't have gsplit (core-utils), please read https://www.topbug.net/blog/2013/04/14/install-and-use-gnu-command-line-tools-in-mac-os-x/
        subprocess.Popen(["gsplit", "-d", "—lines=%d" % lines_per_file, input_file, "%s/%s." % (output_dir, os.path.basename(input_file))])
    elif  _platform == "linux" or _platform == "linux2":
        # linux
        subprocess.Popen(["split", "-d", "—lines=%d" % lines_per_file, input_file, "%s/%s." % (output_dir, os.path.basename(input_file))])
    else:
        # windows
        print "Please install http://gnuwin32.sourceforge.net/packages/coreutils.htm"
        subprocess.Popen(["split.exe", "-d", "—lines=%d" % lines_per_file+1, input_file, "%s/%s." % (output_dir, os.path.basename(input_file))])
        
if __name__ == "__main__":
    try:
        n, keyfile, inputfile = parse_argv(sys.argv[1:])
    except:
        print "usage: python initialize.py -n <number_of_crawlers> -k <keyfile> -i <inputfile>"
        sys.exit()

    # directory
    KEYDIR = "keys"
    INDIR = "data"
    OUTDIR = "tweets"
    RAWJSONDRI = "rawjson"
    LOGDIR = "logs"
    ERRORDIR = "errors"
    CURSORDIR = "cursors"
    for target_dir in [KEYDIR, INDIR, OUTDIR, LOGDIR, ERRORDIR, CURSORDIR, RAWJSONDRI]:
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)

    split(n, keyfile, KEYDIR)
    split(n, inputfile, INDIR)

    IS_SCREEN_NAME = "True"  # or False
    TEMPLATE_FILE_NAME = "status.conf"
    MAX_TWEETS = 3200

    with open("run.sh", "w") as fo:
        for i in range(0, n):
            fo.write("python HTweetCrawler.py -n %d -k %s/part.%.2d -i %s/part.%.2d -o %s/tweets.`date +%%Y%%m%%d%%H%%M%%S`.%.2d.txt -e %s/error.%.2d.txt -l %s/%.2d.log -t %s -c %s/cursor.%.2d.txt -m %d -s %s -r %s/rawjson.`date +%%Y%%m%%d%%H%%M%%S`.%.2d.txt > %s/%.2d.log &\n" %
                     (i, KEYDIR, i, INDIR, i, OUTDIR, i, ERRORDIR, i, LOGDIR, i, TEMPLATE_FILE_NAME, CURSORDIR, i, MAX_TWEETS, IS_SCREEN_NAME, RAWJSONDRI, i, LOGDIR, i))
            fo.write("PID=$!\n")
            fo.write("echo \"kill -9 ${PID}\" >> kill.sh\n")
        fo.write("echo \"rm kill.sh\" >> kill.sh\n")
