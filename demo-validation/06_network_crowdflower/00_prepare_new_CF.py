import json
from collections import defaultdict
import codecs
import math

# boolTest = True

compare = defaultdict(lambda: defaultdict(list))

alreadydone = {}
with open("./result_1_20160725/1st_CF_aggregated_all.txt") as fi:
    for line_cnt, line in enumerate(fi):
        screen_name, city, sample_type, fpp_race, cfrace_first_choice, cfrace_first_choice_conf, cfrace_first_rating, cfrace_first_rating_var, cfrace_second_choice, cfrace_second_choice_conf, cfrace_second_rating, cfrace_second_rating_var, name, image_url = [term.strip() for term in line.split("\t")]
        alreadydone[screen_name] = 1

print "len(alreadydone)=", len(alreadydone)

notyet = 0
with open("./crowdflower_cfonlyus_all_screenname_faceplusplus_name_imageurl.tsv", "r") as fi, open("./crowdflower_2nd_cfonlyus_all_screenname_faceplusplus_name_imageurl.tsv", "w") as output:
    output.write("\t".join(["city", "screen_name", "age_group", "race", "gender", "name", "image_url", "sample_type"])+"\n")
    
    for line_cnt, line in enumerate(fi):
        city, screen_name, age_group, race, gender, name, profile_image_url, linktype = [term.strip() for term in line.split("\t")]
    
        if screen_name not in alreadydone:
            output.write(line)
            notyet += 1

print line_cnt
print notyet



        