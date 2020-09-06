from collections import defaultdict
import random
import sys


list_sampling = ["1st_random", "1st_linktype"]
# list_sampling = [""]

for sampling in list_sampling:

    if sampling == "1st_random":
        dataset = "Random edges"
        linktype = "fr_network"
    elif sampling == "1st_linktype":
        dataset = "Selected edges"
        linktype = "fr_network_linktype"

    cities = ["NY", "texas"]

    cntlinks = defaultdict(dict)
    cntlinks_users = defaultdict(dict)

    all_links = 0
    for city in cities:
        inputfilename = "cfonlyus_%s_random_inferred_users_follower_network_%s.txt" % (sampling, city)
        with open(inputfilename) as fi:
            for line_cnt, line in enumerate(fi):
                all_links += 1
                from_user, from_race, to_user, to_race, mylinktype = [term.strip() for term in line.split("\t")]
                mylink = "%s_%s" % (from_user, to_user)
                cntlinks[city][mylink] = 1
                cntlinks_users[city][from_user] = 1
                cntlinks_users[city][to_user] = 1

    all_users = 0 
    for city in cntlinks_users:
        all_users += len(cntlinks_users[city])

    cntusers = defaultdict(dict)
    with open("./cfonlyus_%s_network_random_screenname_faceplusplus_name_imageurl.txt" % (sampling)) as fi:
        for line_cnt, line in enumerate(fi):
            city, screen_name, age_group, race, gender, name, profile_image_url, sample_type = [term.strip() for term in line.split("\t")]
            cntusers[city][screen_name] = 1
            cntusers["all"][screen_name] = 1


    cntusers_stillonline = defaultdict(dict)
    with open("./cfonlyus_%s_network_stillonline_random_screenname_faceplusplus_name_imageurl.txt" % (sampling)) as fi:
        for line_cnt, line in enumerate(fi):

            city, screen_name, age_group, race, gender, name, profile_image_url, sample_type = [term.strip() for term in line.split("\t")]
            cntusers_stillonline[city][screen_name] = 1
            cntusers_stillonline["all"][screen_name] = 1

    cnt_entries = defaultdict(dict)
    cnt_entries_3raters = defaultdict(dict)
    screenname2cfrace = {}
    screenname2cfrace_3raters = {}
    with open("./result_all/usonly_CF_aggregated_all.txt") as fi:
        for line_cnt, line in enumerate(fi):
            screen_name, city, sample_type, fpp_race, cfrace_first_choice, cfrace_first_choice_conf, cfrace_first_rating, cfrace_first_rating_var, cfrace_second_choice, cfrace_second_choice_conf, cfrace_second_rating, cfrace_second_rating_var, name, image_url = [term.strip() for term in line.split("\t")]
            
            if sample_type == linktype:
                cnt_entries["all"][screen_name] = 1
                cnt_entries[city][screen_name] = 1

                cfrace_first_choice_conf = float(cfrace_first_choice_conf)
                screenname2cfrace[screen_name] = cfrace_first_choice

                if cfrace_first_choice_conf > 0.99:
                    screenname2cfrace_3raters[screen_name] = cfrace_first_choice

                    cnt_entries_3raters["all"][screen_name] = 1
                    cnt_entries_3raters[city][screen_name] = 1

    cf_overlap = 0
    for screen_name in cnt_entries["NY"]:
        if screen_name in cnt_entries["texas"]:
            cf_overlap += 1
            # print screen_name
            


    cnt_links_cf = defaultdict(dict)
    cnt_links_cf_3raters = defaultdict(dict)
    for city in cities:
        inputfilename = "cfonlyus_%s_random_inferred_users_follower_network_%s.txt" % (sampling, city)
        with open(inputfilename) as fi:
            for line_cnt, line in enumerate(fi):
                
                from_user, from_race, to_user, to_race, mylinktype = [term.strip() for term in line.split("\t")]

                mylink = "%s_%s" % (from_user, to_user)
                if from_user in screenname2cfrace:
                    if to_user in screenname2cfrace:
                        cnt_links_cf[city][mylink] = 1
                        cnt_links_cf["all"][mylink] = 1
                if from_user in screenname2cfrace_3raters:
                    if to_user in screenname2cfrace_3raters:
                        cnt_links_cf_3raters[city][mylink] = 1
                        cnt_links_cf_3raters["all"][mylink] = 1


    print "=======", dataset, "======="
    print "[All]"
    print "\t# links in initial samples is", all_links
    print "\t# users in initial samples is", all_users
    # print "\t# users with single faces is", len(cntusers["all"])
    print "\t# users still online is", len(cntusers_stillonline["all"])
    print "\t# of users with CF label is", len(cnt_entries["all"]), "(%.2f%% of initial users)" % (float(len(cnt_entries["all"]))/float(all_users)*100.0)
    print "\t# overlap between two cities is ", cf_overlap
    print "\t# of users all 3 CF raters agreed is", len(cnt_entries_3raters["all"]), "(%.2f%% of all CF users)" % (float(len(cnt_entries_3raters["all"]))/float(len(cnt_entries["all"]))*100.0)
    print "\t# links with CF labels is", len(cnt_links_cf["all"]), "(%.2f%% of initial links)" % (float(len(cnt_links_cf["all"]))/float(all_links)*100.0)
    print "\t# links with CF labels (all 3 agreed) is", len(cnt_links_cf_3raters["all"])

    #"(e.g., Carlos Wallace @MrCarlosWallace, Author l Professor l Organizer l Philanthropist, Houston, TX / Queens, NY, https://twitter.com/mrcarloswallace)"
    
    # print "=======", dataset, "by city ======="

    for city in cntlinks:
        print "[%s]" % (city)
        print "\t# links in initial samples is", len(cntlinks[city])
        print "\t# users in initial samples is", len(cntlinks_users[city])
        print "\t# users with single faces is", len(cntusers[city])
        print "\t# users still online is", len(cntusers_stillonline[city])
        print "\t# of users in CF results is", len(cnt_entries[city]), "(%.2f%% of initial users)" % (float(len(cnt_entries[city]))/float(len(cntlinks_users[city]))*100.0)
        print "\t# of users all 3 CF raters agreed is", len(cnt_entries_3raters[city]), "(%.2f%% of all CF users)" % (float(len(cnt_entries_3raters[city]))/float(len(cnt_entries[city]))*100.0)
        print "\t# links with CF labels is", len(cnt_links_cf[city])
        print "\t# links with CF labels (all 3 agreed) is", len(cnt_links_cf_3raters[city])

