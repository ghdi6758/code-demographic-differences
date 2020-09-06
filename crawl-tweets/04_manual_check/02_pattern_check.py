# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from datetime import datetime
from dateutil.parser import *
import re

boolTest = True

with open("../../data/facepp_bios_newyork.txt") as fi, open("./pattern_matched_users_2.txt", "w") as output:

    for line_cnt, line in enumerate(fi):
        userid, screen_name, name, location, lang, days_since_join, statuses_count, followers_count, friends_count, listed_count, favourites_count, profile_image_url, description, days_since_active = [term.strip() for term in line.split("\t")]
        
        if len(re.findall(r"^(girl|wife|mother|mom)", description.lower())) > 0:
            # print "gender", "female", screen_name
            output.write("\t".join(["gender", "Female", screen_name])+"\n")


        if len(re.findall(r"^(boy|guy|husband|father|dad|dude)", description.lower())) > 0:
            # print "gender", "male", screen_name
            output.write("\t".join(["gender", "Male", screen_name])+"\n")

        # if len(re.findall(r"([1-9][0-9]) *(yr|yrs|year|years) old", description.lower())) > 0:
        if len(re.findall(r"([1-9][0-9]) *(yr|year)", description)) > 0:
            print "[AGE]", description
            # for each in re.findall(r"([1-9][0-9]) *(yr|year)", description.lower()):
            for each in re.findall(r"([1-9][0-9]) *(yr|yrs|year|years) old", description.lower()):
            
                myage = each[0]
            # print "age", myage, screen_name
            output.write("\t".join(["age", myage, screen_name])+"\n")

        if boolTest and line_cnt > 10000:
            break
