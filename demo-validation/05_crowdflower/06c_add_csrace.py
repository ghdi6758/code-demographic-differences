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



screenname2fpprace = {}
for city in ["NY", "texas"]:
    with open("../04_combine/screenname_fpagegroup_fpgender_nbgender_fprace_nbrace_userlang_tweetlang_tweetdomlang_%s.txt" % (city)) as fi:
            for line_cnt, line in enumerate(fi):
                screen_name, age_group, gender, nb_gender, race, nb_race, lang, tw_lang, tw_dom_lang = [term.strip() for term in line.split("\t")]
                screenname2fpprace[screen_name] = race

with open("./2nd_round_CF_aggregated_all.txt") as fi, open("./2nd_round_screenname_cfnameonlyrace_fprace_nbrace_csrace.txt", "w") as output:
    cnt_passed = 0
    screenname2cfrace = {}
    for line_cnt, line in enumerate(fi):
        screen_name, city, sample_type, fpp_race, cfrace_first_choice, cfrace_first_choice_conf, cfrace_first_rating, cfrace_first_rating_var, cfrace_second_choice, cfrace_second_choice_conf, cfrace_second_rating, cfrace_second_rating_var, name, image_url = [term.strip() for term in line.split("\t")]

        if sample_type == "random":

            cf_race = cfrace_first_choice
            confidence = float(cfrace_first_choice_conf)
        
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
            
