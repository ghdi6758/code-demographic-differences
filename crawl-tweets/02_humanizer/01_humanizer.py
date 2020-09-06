# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from datetime import datetime
from dateutil.parser import *



boolTest=False
today=datetime.today().date()
cnt_none=0
# with open("../../data/bios_newyork_users.txt") as fi, open("../../data/human_bios_newyork.txt", "w") as output:
with open("../../data/bios_texas_users.txt") as fi, open("../../data/human_bios_texas.txt", "w") as output:
    for line_cnt, line in enumerate(fi):
        userid, screen_name, name, location, lang, created_at, statuses_count, followers_count, friends_count, listed_count, favourites_count, profile_image_url, description, recented_tweet_created_at = [term.strip() for term in line.split("\t")]

        statuses_count = int(statuses_count)
        followers_count = int(followers_count)
        friends_count = int(friends_count)

        created_at = parse(created_at).date()
        days_since_join = (today - created_at).days

        # print recented_tweet_created_at
        if recented_tweet_created_at != "none":
            recented_tweet_created_at = parse(recented_tweet_created_at).date()
            days_since_active = (today - recented_tweet_created_at).days
        else:
            cnt_none+=1
            continue

        # print statuses_count, friends_count, days_since_join
        # if statuses_count < 10 or followers_count > 10000 or days_since_join < 90: 
        #     continue
        if statuses_count < 10 or days_since_join < 90 or days_since_active > 90: 
            continue

        output.write("\t".join([userid, screen_name, name, location, lang, str(days_since_join), str(statuses_count), str(followers_count), str(friends_count), listed_count, favourites_count, profile_image_url, description, str(days_since_active)])+"\n")


        # print screen_name, today, created_at, days_since_join

        

        if boolTest:
            break
print "cnt_none=", cnt_none