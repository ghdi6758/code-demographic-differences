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


    


list_numfollowings=[]
with open("./retry.txt") as fi:
    for line_cnt, line in enumerate(fi):
        keyword, numpage, numfollowing = [term.strip() for term in line.split("\t")]
        numfollowing = int(numfollowing)
        numpage = int(numpage)
        list_numfollowings.append([numfollowing, numpage])


list_numfollowings = sorted(list_numfollowings)

print list_numfollowings

# sys.exit()
# print list_numfollowings
# print list_numfollowings[2]
# print "Total to crawl=", len(list_numfollowings)
# print "Per crawler=", (len(list_numfollowings)/30)+1


keyword="new york"
# keyword="ny|nyc|brooklyn|queens|yonkers|(the bronx)|(nueva york)"

mydir = "./crawled_4/%02d" % (param)
if not os.path.exists(mydir):
    os.mkdir(mydir)

mycursor = read_cursor()
prepagenum = mycursor[0]
prenumfollowing = mycursor[1]

for i in range(0,len(list_numfollowings)):
    offset = ((i%30)-int(i/30)) % 30
    if offset != param:
        continue

    numfollowing = list_numfollowings[i][0]
    pagenum = list_numfollowings[i][1]

    print "offset=", offset, "numfollowing=", numfollowing, "numpage=", pagenum

    if numfollowing < prenumfollowing:
        continue

    result = gethtml(mydir, keyword, numfollowing, pagenum)
    if result == "lastpage":
        break

    print "[Progress] pagenum=", pagenum
    save_cursor(pagenum,numfollowing)
    pagenum+=1

    if boolTest:
        break
    time.sleep(300)
    
    

    
print "--"
print "Total=", pagenum
print "[DONE]"




