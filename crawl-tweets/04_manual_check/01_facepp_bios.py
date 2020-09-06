# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from datetime import datetime
from dateutil.parser import *

boolTest = False

user2demo = {}
# with open("../../data/screenname_agegroup_race_gender_NY.txt") as fi:
with open("../../data/screenname_agegroup_race_gender_Texas.txt") as fi:
    for line_cnt, line in enumerate(fi):
        screen_name, age, age_range, age_group, race, race_conf, gender, gender_conf = [term.strip() for term in line.split("\t")]

        user2demo[screen_name] = [age_group, gender, race]

print "len(user2demo) = ", len(user2demo)

facepp_bios = {}
# with open("../../data/human_bios_newyork.txt") as fi, open("../../data/facepp_bios_newyork.txt", "w") as output:
with open("../../data/human_bios_texas.txt") as fi, open("../../data/facepp_bios_texas.txt", "w") as output:
    for line_cnt, line in enumerate(fi):
        userid, screen_name, name, location, lang, days_since_join, statuses_count, followers_count, friends_count, listed_count, favourites_count, profile_image_url, description, days_since_active = [term.strip() for term in line.split("\t")]

        if screen_name in user2demo:
            output.write(line)
            facepp_bios[screen_name] = 1
        if boolTest and line_cnt > 10000:
            break

print "Facepp users with bios=", len(facepp_bios)

print "DONE"

# len(user2demo) =  377410
# Facepp users with bios= 377410
# DONE
