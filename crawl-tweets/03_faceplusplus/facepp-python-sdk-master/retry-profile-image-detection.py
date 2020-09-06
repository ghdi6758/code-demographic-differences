# -*- coding: utf-8 -*- 
import sys
import os
import json
import time
from facepp import API
import datetime as dt
reload(sys)
sys.setdefaultencoding("utf-8")

today = dt.datetime.today().strftime("%Y%m%d%H%M")

boolTest = False

try: 
    param = int(sys.argv[1])
except:
    print "[usage] profile-image-detection.py [param]"
    print "param=0, 1, 2, ... n"


def save_cursor(numline):
    cursor_output = open("./cursors/cursor.%02d" % (param), 'w')
    cursor_output.write("\t".join([str(numline)])+"\n")

def read_cursor():
    try: 
        fi = open("./cursors/cursor.%02d" % (param))
        for line in fi:
            prenumline = line.strip()
            prenumline = int(prenumline)

        return prenumline
    except:
        return -1

def read_apikeys():
    fi = open("./keys/part.%02d" % (param))
    for line_cnt, line in enumerate(fi):
        userid, api_key, api_secret = [term.strip() for term in line.split("\t")]
    return [api_key, api_secret]

myproxy = ''
with open("./list_of_proxies.tsv") as fi:
    for line_cnt, line in enumerate(fi):
        result = [term.strip() for term in line.split("\t")]
        # print result
        ip = result[0]
        port = result[1]
        login = result[2]
        pwd = result[3]
        proxy_url = 'http://%s:%s@%s:%s' % (login, pwd, ip, port)
        if line_cnt == param:
            myproxy = proxy_url
proxies = {'http_proxy': myproxy}

# proxies = {'http_proxy': 'http://ghdi6758:1234@1.1.1.1:2222'}

result = read_apikeys()
API_KEY = result[0]
API_SECRET = result[1]
api = API(API_KEY, API_SECRET, proxies)
# print api.myproxy

mycursor = read_cursor()

retry_output = open("./retry/retry.%02d" % (param), 'a')
output = open("./crawled/crawled.%02d.%s" % (param, today), 'w')

cnt_error = 0
with open("./data/part.%02d" % (param)) as fi:
    for line_cnt, line in enumerate(fi):
        if line_cnt <= mycursor:
            continue
        terms = line.split("\t")
        screen_name = terms[0].strip()
        image_link = terms[1].strip()

        print "[%d] %s image_link = %s" % (line_cnt, screen_name, image_link)

        try:
            result_json = api.detection.detect(url=image_link)
            if len(result_json['face']) > 0:
                str_result = json.dumps(result_json)
                output.write('\t'.join([screen_name, str_result]) + "\n")
            else:
                cnt_error += 1
                print "\t error (no face recognized) ", screen_name
                output.write('\t'.join([screen_name, "error"]) + "\n")

        except Exception, e:
            print "\t [ERROR]: Faceplusplus call error"
            if "IMAGE_ERROR_FAILED_TO_DOWNLOAD" not in str(e):
                retry_output.write("\t".join([screen_name, image_link])+"\n")
            print "\t", str(e)

        save_cursor(line_cnt)

        if boolTest and line_cnt > 3:
            break

        time.sleep(1)

print "IMAGE_ERROR_FAILED_TO_DOWNLOAD/DECTECT", cnt_error
