# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from datetime import datetime
from dateutil.parser import *
from collections import defaultdict

boolTest=False

uid2nt = defaultdict(int)

city = "texas"
with open("../../data/facepp_bios_%s.txt" % (city)) as fi:
    for line_cnt, line in enumerate(fi):
        userid, screen_name, name, location, lang, days_since_join, statuses_count, followers_count, friends_count, listed_count, favourites_count, profile_image_url, description, days_since_active = [term.strip() for term in line.split("\t")]
        
        uid2nt[screen_name] = int(statuses_count)
        
        if boolTest and line_cnt > 10000:
            break


with open("../../data/bios_%s_users.txt" % (city)) as fi, open("./tmp_bios_%s.txt" % (city), "w") as output:
    for line_cnt, line in enumerate(fi):
        userid, screen_name, name, location, lang, created_at, statuses_count, followers_count, friends_count, listed_count, favourites_count, profile_image_url, description, recented_tweet_created_at = [term.strip() for term in line.split("\t")]
        if screen_name in uid2nt:
            output.write(line)
            

