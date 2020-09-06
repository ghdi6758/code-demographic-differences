import sys
from datetime import datetime, timedelta
from dateutil.parser import *

boolTest = False

startdate = parse("2014-11-01")

with open("../../data/sorted_user_time_tweetid_hashtag_lower.txt") as fi, open("../../data/new_sorted_user_time_tweetid_hashtag_lower.txt", "w") as output:
    
    for line_cnt, line in enumerate(fi):
        screenname, createdate, tweetid, hashtag = [term.strip() for term in line.split("\t")]
        # print screenname, createdate, tweetid, hashtag
        createdate = parse(createdate)

        if boolTest and line_cnt > 10:
            break

        if createdate < startdate:
            continue

        output.write(line)


start_date = "1 Nov 00:00:00 +0000 2014"
start_date = parse(start_date)

with open("../../data/tweets_NY.txt") as fi, open("../../data/new_tweets_NY.txt", "w") as output:
    for line_cnt, line in enumerate(fi):
        
        try:
            terms = [term.strip() for term in line.split("\t")]
            screen_name = terms[0]
            user_id = terms[1]
            created_at = terms[2]
            tweet_id = terms[3]
            text = terms[4:-1]
            text = " ".join(text)
            coordinates = terms[-1]
        except:
            print "ERROR", line
            continue

        created_at = parse(created_at)

        if boolTest and line_cnt > 10:
            break

        if created_at < start_date:
            continue

        output.write(line)


        