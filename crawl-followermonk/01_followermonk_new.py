# -*- coding: utf-8 -*- 
# code by Jisun An #
import sys
import logging 
import os
import time
import urllib2
import requests
import codecs
import datetime as dt
import cookielib
today = dt.datetime.today().strftime("%Y%m%d%H%M")

reload(sys)
sys.setdefaultencoding("utf-8")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

headers = {
    'cookie': 'tz=Asia%2FBaghdad; visid_incap_133232=s3LZEYroTSKue/qHGbPv4nOGwVYAAAAAQUIPAAAAAADsTRTItg+JjCd/4BWmCEm7; incap_ses_406_133232=4Ik5HEyPzCGTaXWVE2eiBXOGwVYAAAAAXvOsaW4zMI+293k2qVi8wA==; optimizelyEndUserId=oeu1455523448584r0.390710917301476; __qca=P0-2134903382-1455523450368; __utmt=1; _sdsat_WONK_ACCT_ID=669211; _sdsat_TWITTER_ID=54740139; _sdsat_FOLLOWER_COUNT=591; _sdsat_TWITTER_ID_COUNT_FOR_FW_ID=1; intercom-session-ze4rr0vi=b2FLVFhvek9Ec3ZNVHIwWms1OGg4K0N5TzluNzdoeTU2bWh4cTdoNnczUlBGcy9Nc2NJRFYwZU92dE9xakRoNy0tbnBMbFNHNHRodDIzZnFlY1Eydy9Jdz09--5c487965fbded32b61e543851cde051ae4a834b9; sess=e4e2a2b38af35ca6294eec60a253a552; _sdsat_MOZ_SEARCH_LEVEL=basic; optimizelySegments=%7B%22571842640%22%3A%22gc%22%2C%22572040976%22%3A%22false%22%2C%22572831570%22%3A%22direct%22%7D; optimizelyBuckets=%7B%7D; s_cc=true; s_vi=[CS]v1|2B60C33D053136CC-6000010E800080E9[CE]; __ar_v4=FPNOYSQHFJDIVOL7TZPD7S%3A20160216%3A2%7CDDIJILMLEVDBTOHX5IGU32%3A20160216%3A2%7CNU76H3LTEBGOPCLFI4WH6E%3A20160216%3A2%7CU327KV3XV5CVBHVRBCPF5G%3A20160216%3A3%7CRF73OFRSGBBADATWXMC6KT%3A20160216%3A3%7CTFG2QAXZSZBFRF6XBPNCG3%3A20160216%3A3; s_fid=338AC32F663D0C51-2DCBD22AD85181F3; __utma=181959355.1160577169.1455523451.1455523451.1455523451.1; __utmb=181959355.8.9.1455524317837; __utmc=181959355; __utmz=181959355.1455523451.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); mozauth=I9a1u1TsVeXwpOpJfUXBclDUDAcfDJdhaocdL8gk8'
}

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


list_numfollowings=[]

for i in range(2,2000):
    list_numfollowings.append(i)

list_numfollowings = sorted(list_numfollowings)

# keyword="new york"
# keyword="ny|nyc|brooklyn|queens|yonkers|(the bronx)|(nueva york)"
keyword="dallas|houston|(fort worth)|fortworth"


mydir = "./crawled/%02d" % (param)
if not os.path.exists(mydir):
    os.mkdir(mydir)

mycursor = read_cursor()
prepagenum = mycursor[0]
prenumfollowing = mycursor[1]

with requests.Session() as s:
    s.headers.update(headers)
    # p = s.post('https://moz.com/login', data=payload)
    # print p.headers

    # s.cookies = cookies

    for i in range(0, len(list_numfollowings)):
        # offset = ((i % 30)-int(i/30)) % 30
        # if offset != param:
        #     continue

        numfollowing = list_numfollowings[i]

        # logger.debug("offset=%d, numfollowing=%d" % (offset, numfollowing))

        if numfollowing < prenumfollowing:
            continue

        pagenum = 1
        while(True):

            if pagenum <= prepagenum:
                pagenum += 1
                continue

            logger.debug("[CALL] gethtml, Pagenum=%d, Numfollowing=%d" % (pagenum, numfollowing))

            urlkeyword=urllib2.quote(keyword)
            url = 'https://moz.com/followerwonk/bio/?q_type=all&l=%s&frmin=%d&frmax=%d&s=fl&p=%d' % (urlkeyword, numfollowing, numfollowing, pagenum)
            logger.debug(url)

            try:
                html_result = s.get(url)

                # with open("temp.html", "w") as output:
                #     output.write(html_result.text)

                # if "No results found" not in html_result:
                if "Invalid Offset" not in html_result.text:
                    with codecs.open("%s/follower_monk_%s_frmin%d_%d.html" % (mydir,keyword.replace(" ", ""), numfollowing, pagenum), 'w', encoding="utf-8") as output:
                        output.write(html_result.text)
                        logger.debug("ok")
                    valid = "ok"
                else:
                    logger.debug("no result found")
                    valid = "lastpage"
                
            except Exception, e:
                logger.debug("[ERROR]: Follower monk call error")
                retry_output.write("\t".join([keyword, str(numfollowing), str(pagenum)])+"\n")        
                logger.debug(str(e))
                # raise

            if valid == "lastpage":
                prepagenum = 0
                break

            logger.debug("[Progress] pagenum=%d" %  (pagenum))
            save_cursor(pagenum, numfollowing)
            pagenum += 1

            if boolTest and pagenum > 5:
                break

            time.sleep(3)
        
        if boolTest:
            break

    
logger.debug("--")
logger.debug("Total=%d" % (pagenum))
logger.debug("[DONE]")




