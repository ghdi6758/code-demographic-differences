# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import json, glob

boolTest = False

json_files = glob.glob("./rawjson/*.txt")
print len(json_files)

file_index=1
# output=open("./bios_newyork_users.txt", "w")
output=open("./bios_texas_users.txt", "w")

total_bios=0
users_with_location=0
for json_file in json_files:

    print "[%d out of %d]" % (file_index, len(json_files)), json_file

    with open(json_file) as fi:
        for line_cnt, line in enumerate(fi):
            line = line.strip()
            result_json = json.loads(line.strip())
            for each_bio in result_json:
                
                userid = str(each_bio["id"])
                screen_name = each_bio["screen_name"]
                name = each_bio["name"]
                name = " ".join(name.split())
                location = each_bio["location"]
                location = " ".join(location.split())
                lang = each_bio["lang"]
                created_at = each_bio["created_at"]

                if boolTest:
                    print userid, screen_name, name, location, lang, created_at
                
                statuses_count = str(each_bio["statuses_count"])
                followers_count = str(each_bio["followers_count"])
                friends_count = str(each_bio["friends_count"])
                listed_count = str(each_bio["listed_count"])
                favourites_count = str(each_bio["favourites_count"])

                if boolTest:
                    print statuses_count, followers_count, friends_count, listed_count, favourites_count

                profile_image_url = each_bio["profile_image_url"]
                profile_image_url = profile_image_url.replace("_normal", "")

                if boolTest:
                    print profile_image_url

                description = each_bio["description"]
                description = " ".join(description.split())

                if boolTest:
                    print description                

                recent_tweet_created_at="none"

                if "status" in each_bio.keys():
                    status = each_bio["status"]
                    recent_tweet_created_at = status["created_at"]

                    if boolTest:
                        print recent_tweet_created_at

                output.write("\t".join([userid, screen_name, name, location, lang, created_at, statuses_count, followers_count, friends_count, listed_count, favourites_count, profile_image_url, description, recent_tweet_created_at])+"\n")
                    
            if boolTest:
                break
    if boolTest:
        break
    file_index+=1

