from collections import defaultdict
import random
import sys


def fixrace(race):
    if race == "b": newrace = "black"
    elif race == "a": newrace = "asian"
    elif race == "w": newrace = "white"

    return newrace


def shortrace(race):
    if race == "black": 
        newrace = "b"
    elif race == "asian": 
        newrace = "a"
    elif race == "white": 
        newrace = "w"
    elif race == "hispanic": 
        newrace = "h"
    elif race == "other": 
        newrace = "o"
    # else: 
    #     print "!!", race
    #     raise Exception("")
    return newrace

# list_test_method = ["fpp", "classifier"]
list_test_method = ["fpp"]
# list_param = ["all", "3raters", "2raters"]
list_param = ["3raters"]



forbayes = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
forbayes_cf_row_count = defaultdict(lambda: defaultdict(int))
forbayes_fpp_col_count = defaultdict(lambda: defaultdict(int))
forbayes_total = defaultdict(int)

list_sampling = ["1st_random", "1st_linktype"]
# list_sampling = [""]

for sampling in list_sampling:

    if sampling == "1st_random":
        dataset = "Random edges"
        linktype = "fr_network"
    elif sampling == "1st_linktype":
        dataset = "Selected edges"
        linktype = "fr_network_linktype"


    for test_method in list_test_method:
        if test_method == "fpp":
            list_pred_param = [""]
        elif test_method == "classifier":
            list_pred_param = ["pred_all", "pred_filtered"]
        for param in list_param:
            for pred_param in list_pred_param:

                if test_method == "fpp":
                    pred_param = ""

                if param == "all":
                    str_cf_conf = "> 0.5"
                elif param == "3raters":
                    str_cf_conf = "> 0.99"
                elif param == "2raters":
                    str_cf_conf = ">0.5 and <= 0.99"

                print "-------------------------------------"
                print dataset, param, test_method, pred_param


                screenname2cfrace = {}
                screenname2line = {}
                with open("./result_all/usonly_CF_aggregated_all.txt") as fi:
                    for line_cnt, line in enumerate(fi):
                        screen_name, city, sample_type, fpp_race, cfrace_first_choice, cfrace_first_choice_conf, cfrace_first_rating, cfrace_first_rating_var, cfrace_second_choice, cfrace_second_choice_conf, cfrace_second_rating, cfrace_second_rating_var, name, image_url = [term.strip() for term in line.split("\t")]
                        if sample_type == linktype:

                            screenname2line[screen_name] = line.strip()

                            cfrace_first_choice_conf = float(cfrace_first_choice_conf)

                            if cfrace_first_choice_conf < 0.5:
                                if param == "low":
                                    screenname2cfrace[screen_name] = cfrace_first_choice
                                continue
                            if param == "all":
                                screenname2cfrace[screen_name] = cfrace_first_choice
                            elif param == "3raters":
                                if cfrace_first_choice_conf > 0.99:
                                    screenname2cfrace[screen_name] = cfrace_first_choice
                            elif param == "2raters":
                                if cfrace_first_choice_conf <= 0.99:
                                    screenname2cfrace[screen_name] = cfrace_first_choice

                print param, len(screenname2cfrace)



                cntusers = defaultdict(dict)
                with open("./cfonlyus_%s_network_random_screenname_faceplusplus_name_imageurl.txt" % (sampling)) as fi:
                    for line_cnt, line in enumerate(fi):
                        city, screen_name, age_group, race, gender, name, profile_image_url, sample_type = [term.strip() for term in line.split("\t")]
                        cntusers[city][screen_name] = 1


                cntusers_stillonline = defaultdict(dict)
                with open("./cfonlyus_%s_network_stillonline_random_screenname_faceplusplus_name_imageurl.txt" % (sampling)) as fi:
                    for line_cnt, line in enumerate(fi):

                        city, screen_name, age_group, race, gender, name, profile_image_url, sample_type = [term.strip() for term in line.split("\t")]
                        if screen_name in screenname2cfrace:
                            cntusers_stillonline[city][screen_name] = 1

                cntlinks = defaultdict(lambda: defaultdict(int))
                cities = ["NY", "texas"]
                linkall = defaultdict(dict)
                global_cnt = 0
                for city in cities:
                    inputfilename = "cfonlyus_%s_random_inferred_users_follower_network_%s.txt" % (sampling, city)
                    outputfilename = "cfonlyus_%s_withcfrace_random_inferred_users_follower_network_%s.txt" % (sampling, city)
                    # outputfilename = "test_%s.txt" % (city)
                    
                    cntlink_both = 0
                    cnt_stillonline = 0
                    with open(inputfilename) as fi, open(outputfilename, "w") as output:
                        for line_cnt, line in enumerate(fi):

                            from_user, from_race, to_user, to_race, mylinktype = [term.strip() for term in line.split("\t")]

                            if test_method == "classifier":
                                if from_user not in screenname2predrace:
                                    continue

                            if from_user in screenname2cfrace:
                                from_cfrace = screenname2cfrace[from_user]

                                if to_user in screenname2cfrace:
                                    to_cfrace = screenname2cfrace[to_user]

                                    mytag = "%s_%s" % (from_cfrace, to_cfrace)

                                    if mytag in ["white_white", "white_black", "black_white", "black_black"]:
                                    # if mytag in ["white_white", "black_black"]:
                                        linkall[mytag][global_cnt] = "\t".join([from_user, from_race, from_cfrace, to_user, to_race, to_cfrace])

                                    output.write("\t".join([from_user, from_race, from_cfrace, to_user, to_race, to_cfrace])+"\n")

                                    global_cnt += 1
                                    cntlink_both += 1

                    cntlinks[city]["original"] = line_cnt+1
                    cntlinks[city]["both"] = cntlink_both

                misclass = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
                linktype_cmatrix = defaultdict(lambda: defaultdict(int))

                list_tags = {}
                cities = ["NY", "texas"]
                # cities = ["random100"]
                for city in cities:

                    inputfilename = "cfonlyus_%s_withcfrace_random_inferred_users_follower_network_%s.txt" % (sampling, city)

                    cnt_fprace = defaultdict(lambda: defaultdict(int))
                    cnt_cfrace = defaultdict(lambda: defaultdict(int))
                    fprace_total = defaultdict(int)
                    cfrace_total = defaultdict(int)


                    with open(inputfilename) as fi:

                        for line_cnt, line in enumerate(fi):
                            from_user, from_race, from_cfrace, to_user, to_race, to_cfrace = [term.strip() for term in line.split("\t")]

                            from_race = fixrace(from_race)
                            to_race = fixrace(to_race)

                            cnt_fprace[from_race][to_race] += 1
                            cnt_cfrace[from_cfrace][to_cfrace] += 1

                            fprace_total[from_race] += 1
                            cfrace_total[from_cfrace] += 1

                            mytag = "%s_%s" % (from_cfrace, to_cfrace)
                            
                            short_from_cfrace = shortrace(from_cfrace)
                            short_to_cfrace = shortrace(to_cfrace)
                            short_from_race = shortrace(from_race)
                            short_to_race = shortrace(to_race)

                            cftag = "%s->%s" % (short_from_cfrace, short_to_cfrace)
                            fpptag = "%s->%s" % (short_from_race, short_to_race)
                            list_tags[fpptag] = 1
                            linktype_cmatrix[cftag][fpptag] += 1

                            if test_method == "fpp":
                                from_race = from_race
                            elif test_method == "classifier":
                                if from_user in screenname2predrace:
                                    from_race = screenname2predrace[from_user]

                            misclass[mytag][from_cfrace][from_race] += 1
                            misclass[mytag][from_cfrace]["total"] += 1
                            
                myheader = [" ", "|"]
                for fpptag in sorted(list_tags):    
                    myheader.append("%s|" % str(fpptag))
                    # myheader.append("|")
                print "\t".join(myheader)
                
                total_count = 0
                row_count = defaultdict(int)
                col_count = defaultdict(int)
                for cftag in sorted(linktype_cmatrix):
                    myresult = [cftag, "| "]
                    for fpptag in sorted(list_tags):
                        if linktype_cmatrix[cftag][fpptag]:
                            mycount = linktype_cmatrix[cftag][fpptag]
                            total_count += mycount
                        else:
                            mycount = 0
                        row_count[cftag] += mycount
                        col_count[fpptag] += mycount

                        myresult.append(str(mycount))
                        myresult.append("| ")
                    myresult.append(str(row_count[cftag]))
                    myresult.append("|")
                    print "\t".join(myresult)

                myresult = [" ", "|"]
                for fpptag in sorted(list_tags):
                    myresult.append(str(col_count[fpptag]))
                    myresult.append("|")
                myresult.append(str(total_count))
                myresult.append("|")
                print "\t".join(myresult)

                print "N(CF edges) =", total_count 

                forbayes[sampling] = linktype_cmatrix
                forbayes_cf_row_count[sampling] = row_count
                forbayes_fpp_col_count[sampling] = col_count
                forbayes_total[sampling] = total_count
                
                print "!!!", sampling, linktype_cmatrix["w->w"]["a->w"]
                print "!!!", forbayes[sampling]["w->w"]["a->w"]



list_sampling = ["1st_random", "1st_linktype"]

# p_selected = float(forbayes["1st_linktype"]["w->w"]["b->w"])/float(forbayes_fpp_col_count["1st_linktype"]["b->w"])
# p_random_fpp = float(forbayes_fpp_col_count["1st_random"]["b->w"])/float(forbayes_total["1st_random"])
# p_random_cf = float(forbayes_cf_row_count["1st_random"]["w->w"])/float(forbayes_total["1st_random"])

# # bayes["f_b->w"]["cf_w->w"] = p_selected * p_random_fpp / p_random_cf
# # print bayes["f_b->w"]["cf_w->w"]
# print "f_b->w", "cf_w->w", p_selected * p_random_fpp / p_random_cf


print "f_a->w", "cf_w->w", float(forbayes["1st_random"]["a->w"]["w->w"])/float(forbayes_cf_row_count["1st_random"]["w->w"])
# bayes["f_b->w"]["cf_w->w"] = p_selected * p_random_fpp / p_random_cf
# print bayes["f_b->w"]["cf_w->w"]

bayes = defaultdict(lambda: defaultdict(float))


list_race = ["a"]
list_otherrace = ["w", "b", "a"]
list_linktype = ["w->w", "w->b", "b->w", "b->b"]

for race in list_race:
    for givenlink in list_linktype:
        tag_race = "f_%s" % (race)
        tag_givenlink = "cf_%s" % (givenlink)

        for otherrace in list_otherrace:
            possiblelink = "%s->%s" % (race, otherrace)
            tag_possiblelink = "f_%s" % (possiblelink)


            bayes[tag_possiblelink][tag_givenlink] = float(forbayes["1st_random"][givenlink][possiblelink])/float(forbayes_cf_row_count["1st_random"][givenlink])

            bayes[tag_race][tag_givenlink] += bayes[tag_possiblelink][tag_givenlink]

            # print tag_possiblelink, tag_givenlink, possiblelink, givenlink
            # print "\t", forbayes["1st_random"][givenlink][possiblelink], forbayes_cf_row_count["1st_random"][givenlink]
            # print "\t", bayes[tag_possiblelink][tag_givenlink]
            
        print tag_race, tag_givenlink, bayes[tag_race][tag_givenlink]

        # sys.exit()

list_race = ["b", "w"]
list_otherrace = ["w", "b", "a"]
list_linktype = ["w->w", "w->b", "b->w", "b->b"]

for race in list_race:
    for givenlink in list_linktype:
        tag_race = "f_%s" % (race)
        tag_givenlink = "cf_%s" % (givenlink)

        # bayes["f_b"]["cf_w->w"]

        for otherrace in list_otherrace:
            possiblelink = "%s->%s" % (race, otherrace)
            tag_possiblelink = "f_%s" % (possiblelink)

            p_selected = float(forbayes["1st_linktype"][givenlink][possiblelink])/float(forbayes_fpp_col_count["1st_linktype"]["b->w"])
            p_random_fpp = float(forbayes_fpp_col_count["1st_random"][possiblelink])/float(forbayes_total["1st_random"])
            p_random_cf = float(forbayes_cf_row_count["1st_random"][givenlink])/float(forbayes_total["1st_random"])

            bayes[tag_possiblelink][tag_givenlink] = p_selected * p_random_fpp / p_random_cf

            bayes[tag_race][tag_givenlink] += bayes[tag_possiblelink][tag_givenlink]

            # print tag_possiblelink, tag_givenlink, bayes[tag_possiblelink][tag_givenlink]
            
        print tag_race, tag_givenlink, bayes[tag_race][tag_givenlink]
        

list_race = ["w", "b", "a"]

print "\n"
for givenlink in list_linktype:
    splited = givenlink.split("->")
    fromrace = fixrace(splited[0])
    torace = fixrace(splited[1])

    print "CF_%s->%s" % (fromrace.title(), torace.title())
    print "CF\F++  White   Black   Asian   TOTAL"
    
    myresult = [fromrace.title()]
    total = 0.0
    for race in list_race:
        tag_race = "f_%s" % (race)
        tag_givenlink = "cf_%s" % (givenlink)
        total += bayes[tag_race][tag_givenlink]
        myresult.append("%.4f" % (bayes[tag_race][tag_givenlink]))
    myresult.append("%.4f" % (total))
    print "\t".join(myresult)
    print ""


print "\n\n"

print "Probability that one tagged as a certain race by CF given a particular link" 


list_race = ["w", "b", "a"]
list_linktype = ["w->w", "w->b", "b->w", "b->b"]

prob_givenlink = defaultdict(lambda: defaultdict(float))


for race in list_race:
    if race == "a":
        continue
    for givenlink in list_linktype:
        tag_race = "f_%s" % (race)
        tag_givenlink = "cf_%s" % (givenlink)

        mysum = 0
        for otherrace in list_race:
            possiblelink = "%s->%s" % (race, otherrace)
            tag_possiblelink = "f_%s" % (possiblelink)

            mysum += float(forbayes["1st_random"][givenlink][possiblelink])

        prob_givenlink[tag_race][tag_givenlink] = mysum/float(forbayes_cf_row_count["1st_random"][givenlink])
            
        print "Prob. tagged as", fixrace(race).title(), "given %s is %.4f." % (givenlink, prob_givenlink[tag_race][tag_givenlink])



# "CF White->White"           
# "CF\F++  White   Black   Asian   TOTAL"
# "White"  
# 0.858045469 0.018581526 0.071283096 0.947910091
                
# CF White->Black             
# CF\F++  White   Black   Asian   TOTAL
# White   1.09270217  0.046153846 0.038461538 1.177317554
                
# CF Black->White             
# CF\F++  White   Black   Asian   TOTAL
# Black   0.329558608 0.742105263 0.078947368 1.15061124
                
# CF Black->Black             
# CF\F++  White   Black   Asian   TOTAL
# Black   0.081259634 0.729411765 0.070175439 0.880846838

# P(Face++ outputs "black-white" | true edge according to CF is "white-white") = (35/170)*(36/6475/(482/675) = 0.01735
# 0.015377105
# P(true edge according to CF is "white-white" | Face++ outputs "black-white") = 35/170
# 0.205882353
# P(Face++ outputs "black-white" for a random edge) = 36/675
# 0.053333333
# P(probability of a random edge to be "white-white" as per CF) = 482/675
# 0.714074074


