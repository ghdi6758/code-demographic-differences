# -*- coding: utf-8 -*- 
import json
import glob
import sys
import re
from dateutil.parser import *
reload(sys)
sys.setdefaultencoding("utf-8")

# test_created_at = parse(formated_created_at)
# print test_created_at.strftime("%a %b %Y %H:%M:%S")

boolTest = True

# all_files = glob.glob("./tweets/tweets_1/*.txt")
all_files = glob.glob("./tweets/*.txt")
print len(all_files)

start_date = "1 Nov 00:00:00 +0000 2014"
end_date = "30 Oct 00:00:00 +0000 2015"
start_date = parse(start_date)
end_date = parse(end_date)


file_index = 1
# output = open("./user_time_tweetid_hashtag.txt", "w")
# output_tweets = open("./tweets_NY.txt", "w")
output = open("./user_time_tweetid_hashtag_lower_Texas.txt", "w")
output_tweets = open("./tweets_Texas.txt", "w")

for each_file in all_files:

    print "[%d out of %d]" % (file_index, len(all_files)), each_file

    with open(each_file) as fi:
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
            # naive = dt.replace(tzinfo=None)

            if created_at < start_date or created_at > end_date:
                continue
            output_tweets.write(line)
            formated_created_at = created_at.strftime("%Y%m%d%H%M%S")
            
            for hashtag in re.findall(r"#(\w+)", text):

                hashtag = hashtag.lower()
                if boolTest:
                    print screen_name, formated_created_at, tweet_id, text, hashtag    

                output.write("\t".join([screen_name, formated_created_at, tweet_id, hashtag])+"\n")
            
            if boolTest and line_cnt > 500:
                break

    if boolTest and file_index > 5:
        break
    file_index += 1

print "DONE!"
