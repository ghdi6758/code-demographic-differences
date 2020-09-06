import csv
from collections import defaultdict
boolTest = False


screenname2csrace = {}
screenname2nbrace = {}
for city in ["NY", "texas"]:
    with open("../02_race/census_race/screenname_fpagegroup_fprace_fpgender_bios_cnrace_%s.txt" % (city)) as fi:
        for line_cnt, line in enumerate(fi):
            screen_name, age_group, race, gender, userid, name, location, lang, days_since_join, statuses_count, followers_count, friends_count, listed_count, favourites_count, profile_image_url, description, days_since_active, cnrace, cnrace_hard = [term.strip() for term in line.split("\t")]
            screenname2csrace[screen_name] = cnrace_hard

    
    with open("../04_combine/screenname_fpagegroup_fpgender_nbgender_fprace_nbrace_userlang_tweetlang_tweetdomlang_%s.txt" % (city)) as fi:
        for line_cnt, line in enumerate(fi):
            screen_name, age_group, gender, nb_gender, race, nb_race, lang, tw_lang, tw_dom_lang = [term.strip() for term in line.split("\t")]
            screenname2nbrace[screen_name] = nb_race

# with open('CF_aggregated_all.csv', 'rb') as csvfile, open("./result_CF_face.txt","w") as output:
with open('CF_face_name_aggregated_all.csv', 'rb') as csvfile, open("./screenname_cfrace_fprace_nbrace_csrace.txt","w") as output:

    output.write("\t".join(["city", "screen_name", "cf_race", "fpp_race", "nb_race", "cs_race"])+"\n")
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    cnt_line = 0
    cnt_passed = 0
    for row in spamreader:
        if cnt_line == 0:
            cnt_line += 1
            continue

        state = row[2]

        if state != "finalized":
            continue
        cf_race = row[5]
        confidence = float(row[6])
        city = row[8]
        name = row[11]
        fpp_race = row[12]
        screen_name = row[13]

        if confidence > 0.9:
            if screen_name not in screenname2nbrace:
                print "ERROR no nb_race"
                nb_race = "NA"
            else:
                nb_race = screenname2nbrace[screen_name]

            if screen_name not in screenname2csrace:
                print "ERROR no cs_race"
                cs_race = "NA"
            else:
                cs_race = screenname2csrace[screen_name]

            output.write("\t".join([city, screen_name, cf_race, fpp_race, nb_race, cs_race])+"\n")
            
