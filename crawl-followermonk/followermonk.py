# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
import time
import urllib2
import requests
from lxml import etree
# from bs4 import BeautifulSoup
import codecs
import datetime as dt
today=dt.datetime.today().strftime("%Y%m%d%H%M")

boolTest = False

try: 
    param = int(sys.argv[1])
except:
    print "[usage] followermonk.py [param]"
    print "param=0, 1, 2, ... n"


retry_output = open("./retry/retry.%02d" % (param), 'a')

def save_cursor(pagenum, numfollowing):
    cursor_output = open("./cursors/cursor.%02d" % (param), 'w')
    cursor_output.write("\t".join([str(pagenum),str(numfollowing)])+"\n")

def read_cursor():
    try: 
        fi = open("./cursors/cursor.%02d" % (param))
        for line in fi:
            prepagenum, prenumfollowing = [term.strip() for term in line.split("\t")]

        prepagenum = int(prepagenum)
        prenumfollowing = int(prenumfollowing)

        return [prepagenum, prenumfollowing]
    except:
        return [-1, -1]


myproxy = ''
with open("./list_of_proxies.tsv") as fi:
    for line_cnt, line in enumerate(fi):
        result = [term.strip() for term in line.split("\t")]
        # print result
        ip = result[0]
        port = result[1]
        login = result[2]
        pwd = result[3]
        proxy_url = 'http://%s:%s@%s:%s' % (login,pwd,ip,port)
        if line_cnt == param:
            myproxy = proxy_url
proxies = {'http_proxy': myproxy}

# proxies = {'http_proxy': 'http://iweber:F0GjwpxT@209.0.51.123:29842'}
# print proxies

def gethtml(mydir, keyword, numfollowing, pagenum):


    print "[CALL] gethtml", "Pagenum=", pagenum, "Numfollowing=", numfollowing


    urlkeyword=urllib2.quote(keyword)
    url = 'https://moz.com/followerwonk/bio/?q_type=all&l=%s&frmin=%d&frmax=%d&s=fl&p=%d' % (urlkeyword, numfollowing, numfollowing, pagenum)
    # url = 'https://moz.com/followerwonk/bio/?q_type=all&l=%s&frmax=%d&s=fl&p=%d' % (urlkeyword, numfollowing, pagenum)
    print url

    try:
        proxy = urllib2.ProxyHandler(proxies)
        auth = urllib2.HTTPBasicAuthHandler()
        opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        html_result = urllib2.urlopen(url, timeout = 60).read()

        if "No results found" not in html_result:
            with codecs.open("%s/follower_monk_%s_frmin%d_%d.html" % (mydir,keyword.replace(" ", ""), numfollowing, pagenum), 'w', encoding="utf-8") as output:
                output.write(html_result)
                print "ok"
            return "ok"
        else:
            print "no result found"
            return "lastpage"

        
    except Exception, e:
        print "[ERROR]: Follower monk call error"
        retry_output.write("\t".join([keyword, str(numfollowing), str(pagenum)])+"\n")        
        print str(e)
        # raise


    




# new york  1,236,504 results, 24731 pages
# NY 1,005,920 results, 20119 pages
# nyc 296,575 results, 5932 pages
totalpages=24731
maxfollowing = 1999
keyword="new york"

assignment= int(float(maxfollowing)/28.0) + 1
mystart= assignment*param
myend=assignment*param+assignment

if mystart == 0:
    mystart = 2

mydir = "./crawled/%s_%02d" % (keyword.replace(" ", ""), param)
if not os.path.exists(mydir):
    os.mkdir(mydir)

mycursor = read_cursor()
prepagenum = mycursor[0]
prenumfollowing = mycursor[1]

# if boolTest:
#     prepagenum=157
#     mydir="crawled/test"
#     numfollowing=2

for numfollowing in range(mystart, myend): 

    if numfollowing < prenumfollowing:
        continue

    # if boolTest:
    #     numfollowing=2

    pagenum=1
    while(True):

        if pagenum <= prepagenum:
            pagenum+=1
            continue

        result = gethtml(mydir, keyword, numfollowing, pagenum)
        if result == "lastpage":
            break
        print "[Progress] pagenum=", pagenum
        save_cursor(pagenum,numfollowing)
        pagenum+=1

        if boolTest and pagenum > 4:
            break
        time.sleep(300)
    
    if boolTest:
        break
    # if boolTest and pagenum > 3:
    #     break



print "--"
print "Total=", pagenum
print "[DONE]"




