# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from datetime import datetime
from dateutil.parser import *
import re
from collections import defaultdict

boolTest = False

uid2nt = defaultdict(int)
uid2active = {}

city = "texas"
# with open("../../data/facepp_bios_%s.txt" % (city)) as fi:
with open("./tmp_bios_%s.txt" % (city)) as fi:
    for line_cnt, line in enumerate(fi):
        userid, screen_name, name, location, lang, created_at, statuses_count, followers_count, friends_count, listed_count, favourites_count, profile_image_url, description, recented_tweet_created_at = [term.strip() for term in line.split("\t")]

        uid2nt[screen_name] = int(statuses_count)
        uid2active[screen_name] = recented_tweet_created_at
        
        if boolTest and line_cnt > 10000:
            break

cnt_userswithtweets = 0
with open("./user_num_tweets_%s.txt" % (city)) as fi, open("./tweets_coverage_%s.txt" % (city), "w") as output, open("./tweets_coverage_status_data_prop_%s.txt" % (city), "w") as output_2:
    output.write("proportion"+"\n")
    for line_cnt, line in enumerate(fi):
        screen_name, num_tweets, first_tweet, last_tweet = [term.strip() for term in line.split("\t")]
        if screen_name in uid2nt:
            cnt_userswithtweets += 1

            statuses_count = uid2nt[screen_name]
            recented_tweet_created_at = uid2active[screen_name]
            str_recent_tweet = parse(recented_tweet_created_at).strftime("%Y%m%d%H%M%S")
            # diff = statuses_count - int(num_tweets)
            prop = float(num_tweets)/float(statuses_count)

            if prop > 1.0:
                prop = 1.0

            output_2.write("\t".join([screen_name, str(statuses_count), (num_tweets), str(prop)])+"\n")
            output.write(str(prop)+"\n")

print "Facepp users=", len(uid2nt)
print "userswithtweets=", cnt_userswithtweets