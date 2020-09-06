# -*- coding: utf-8 -*- 
import json
import glob
import sys
import re
from dateutil.parser import *
reload(sys)
sys.setdefaultencoding("utf-8")

boolTest = False

all_files = glob.glob("./tweets/*.txt")
# if boolTest:
#     all_files = ["test"]
print len(all_files)


file_index = 1
output = open("./user_num_tweets_texas.txt", "w")


for each_file in all_files:

    print "[%d out of %d]" % (file_index, len(all_files)), each_file
    
    # if boolTest:
    #     each_file = "./tweets/tweets.20151124154826.29.txt"

    with open(each_file) as fi:
        pre_screen_name = ""
        pre_created_at = ""
        first_tweet = ""
        last_tweet = ""
        num_tweets = 0

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

            if line_cnt != 0 and screen_name != pre_screen_name:

                first_tweet = parse(pre_created_at).strftime("%Y%m%d%H%M%S")

                output.write("\t".join([pre_screen_name, str(num_tweets), first_tweet, last_tweet])+"\n")

                pre_screen_name = screen_name
                pre_created_at = created_at
                first_tweet = ""
                last_tweet = parse(created_at).strftime("%Y%m%d%H%M%S")
                num_tweets = 0

               
            if num_tweets == 0:
                last_tweet = parse(created_at).strftime("%Y%m%d%H%M%S")
            
            num_tweets += 1
            pre_screen_name = screen_name
            pre_created_at = created_at

            if boolTest and line_cnt > 10000:
                break

    if boolTest and file_index > 5:
        break
    file_index += 1

print "DONE!"
