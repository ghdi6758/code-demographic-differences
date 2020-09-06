from collections import defaultdict
import random


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

# # sampling = ""
# sampling = "5th_"

list_sampling = ["", "5th_"]

for sampling in list_sampling:

    if sampling == "":
        linktype = "fr_network"
    elif sampling == "5th_":
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
                print param, test_method, pred_param


                screenname2cfrace = {}
                screenname2line = {}
                with open("./5th_round_CF_aggregated_all.txt") as fi:
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
                with open("./%snetwork_random_screenname_faceplusplus_name_imageurl.txt" % (sampling)) as fi:
                    for line_cnt, line in enumerate(fi):
                        city, screen_name, age_group, race, gender, name, profile_image_url, sample_type = [term.strip() for term in line.split("\t")]
                        cntusers[city][screen_name] = 1


                cntusers_stillonline = defaultdict(dict)
                with open("./%snetwork_stillonline_random_screenname_faceplusplus_name_imageurl.txt" % (sampling)) as fi:
                    for line_cnt, line in enumerate(fi):

                        city, screen_name, age_group, race, gender, name, profile_image_url, sample_type = [term.strip() for term in line.split("\t")]
                        if screen_name in screenname2cfrace:
                            cntusers_stillonline[city][screen_name] = 1

                cntlinks = defaultdict(lambda: defaultdict(int))
                cities = ["NY", "texas"]
                linkall = defaultdict(dict)
                global_cnt = 0
                for city in cities:
                    inputfilename = "%srandom_inferred_users_follower_network_%s.txt" % (sampling, city)
                    outputfilename = "%swithcfrace_random_inferred_users_follower_network_%s.txt" % (sampling, city)
                    # outputfilename = "test_%s.txt" % (city)
                    
                    cntlink_both = 0
                    cnt_stillonline = 0
                    with open(inputfilename) as fi, open(outputfilename, "w") as output:
                        for line_cnt, line in enumerate(fi):

                            from_user, from_race, to_user, to_race = [term.strip() for term in line.split("\t")]

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

                    inputfilename = "%swithcfrace_random_inferred_users_follower_network_%s.txt" % (sampling, city)

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

                forbayes[linktype] = linktype_cmatrix
                forbayes_cf_row_count[linktype] = row_count
                forbayes_fpp_col_count[linktype] = col_count
                forbayes_total[linktype] = total_count
                
                print "!!!", linktype, linktype_cmatrix["w->w"]["a->w"]
                print "!!!", forbayes[linktype]["w->w"]["a->w"] 

                # print "\n\n"
                # print "==============================================="
                # print "\t".join(["!!", param, test_method, pred_param])
                # print "\n\n"

                # output_all.write("==============================================="+"\n")
                # output_all.write("\t".join(["!!", param, test_method, pred_param])+"\n\n")

                
                # for city in ["NY", "texas"]:
                #     print city, "originally there were", cntlinks[city]["original"], "links with", len(cntusers[city])
                #     print "\t", "For",len(cntusers_stillonline[city]), "users who are still online and cf_conf %s are," % (str_cf_conf), "we have", cntlinks[city]["both"], "links"
                #     print "\n"
                    
                #     output_all.write("%s, originally there were %d links with %d users. \n" % (city, cntlinks[city]["original"], len(cntusers[city])))
                #     output_all.write("For %d users who are still online and cf_agrrement %s, we have %d links.\n" % (len(cntusers_stillonline[city]),str_cf_conf, cntlinks[city]["both"]))
                #     output_all.write("\n")


                # for mytag in ["white_white", "white_black", "black_white", "black_black"]:

                #     # if "asian" in mytag:
                #     #     continue
                #     print mytag, "--------"
                #     output_all.write("%s --------\n" % (mytag))
                #     for from_cfrace in misclass[mytag]:
                #         myresult = [from_cfrace, "|"]
                #         total = misclass[mytag][from_cfrace]["total"]
                #         myheader = ["CF\\F++", "|"]
                #         for from_race in misclass[mytag][from_cfrace]:
                #             if not from_race == "total":
                #                 myheader.append(from_race)
                #                 myheader.append("|")
                #                 cnt = misclass[mytag][from_cfrace][from_race]
                #                 perc = float(cnt)/float(total)*100.0
                #                 myresult.append("%d(%.1f%%) |" % (cnt, perc))
                #         print "\t".join(myheader)
                #         print "\t".join(myresult)
                #         print "\n"

                #         output_all.write("\t".join(myheader)+"\n")
                #         output_all.write("\t".join(myresult)+"\n")
                #         output_all.write("\n")





# p_selected = float(forbayes["fr_network_linktype"]["w->w"]["b->w"])/float(forbayes_fpp_col_count["fr_network_linktype"]["b->w"])
# p_random_fpp = float(forbayes_fpp_col_count["fr_network"]["b->w"])/float(forbayes_total["fr_network"])
# p_random_cf = float(forbayes_cf_row_count["fr_network"]["w->w"])/float(forbayes_total["fr_network"])

# # bayes["f_b->w"]["cf_w->w"] = p_selected * p_random_fpp / p_random_cf
# # print bayes["f_b->w"]["cf_w->w"]
# print "f_b->w", "cf_w->w", p_selected * p_random_fpp / p_random_cf



print "f_a->w", "cf_w->w", float(forbayes["fr_network"]["a->w"]["w->w"])/float(forbayes_cf_row_count["fr_network"]["w->w"])
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


            bayes[tag_possiblelink][tag_givenlink] = float(forbayes["fr_network"][givenlink][possiblelink])/float(forbayes_cf_row_count["fr_network"][givenlink])

            bayes[tag_race][tag_givenlink] += bayes[tag_possiblelink][tag_givenlink]

            # print tag_possiblelink, tag_givenlink, possiblelink, givenlink
            # print "\t", forbayes["fr_network"][givenlink][possiblelink], forbayes_cf_row_count["fr_network"][givenlink]
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

            p_selected = float(forbayes["fr_network_linktype"][givenlink][possiblelink])/float(forbayes_fpp_col_count["fr_network_linktype"]["b->w"])
            p_random_fpp = float(forbayes_fpp_col_count["fr_network"][possiblelink])/float(forbayes_total["fr_network"])
            p_random_cf = float(forbayes_cf_row_count["fr_network"][givenlink])/float(forbayes_total["fr_network"])

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

            mysum += float(forbayes["fr_network"][givenlink][possiblelink])

        prob_givenlink[tag_race][tag_givenlink] = mysum/float(forbayes_cf_row_count["fr_network"][givenlink])
            
        print "Prob. tagged as", fixrace(race).title(), "given %s is %.4f." % (givenlink, prob_givenlink[tag_race][tag_givenlink])

