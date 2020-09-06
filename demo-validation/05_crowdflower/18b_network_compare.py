from collections import defaultdict
import random

def fixrace(race):
    if race == "b": newrace = "black"
    elif race == "a": newrace = "asian"
    elif race == "w": newrace = "white"

    return newrace


output_all = open("./link_analysis/link_analysis_linktype.txt", "w")
output_image = open("./manual_inspection_images_link_analysis_linktype.txt", "w")

# list_test_method = ["fpp", "classifier"]
list_test_method = ["fpp"]
# list_param = ["all", "3raters", "2raters"]
list_param = ["3raters"]

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

            screenname2predrace = {}
            with open("./sn_pred_predprob.txt") as fi:
                for line_cnt, line in enumerate(fi):
                    screen_name, pred, predprob = [term.strip() for term in line.split("\t")]


                    if pred == "0":
                        pred_race = "white"
                    elif pred == "1":
                        pred_race = "black"

                    predprob = float(predprob)

                    if pred_param == "pred_all":
                        screenname2predrace[screen_name] = pred_race
                    elif pred_param == "pred_filtered":
                        if predprob < 0.5:
                            continue
                        else:
                            screenname2predrace[screen_name] = pred_race

            print "len(screenname2predrace)=", len(screenname2predrace)

            # sys.exit()

            screenname2cfrace = {}
            screenname2line = {}
            with open("./5th_round_CF_aggregated_all.txt") as fi:
                for line_cnt, line in enumerate(fi):
                    screen_name, city, sample_type, fpp_race, cfrace_first_choice, cfrace_first_choice_conf, cfrace_first_rating, cfrace_first_rating_var, cfrace_second_choice, cfrace_second_choice_conf, cfrace_second_rating, cfrace_second_rating_var, name, image_url = [term.strip() for term in line.split("\t")]
                    if "fr_network" in sample_type:
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
            with open("./all_network_random_screenname_faceplusplus_name_imageurl.txt") as fi:
                for line_cnt, line in enumerate(fi):
                    city, screen_name, age_group, race, gender, name, profile_image_url, sample_type = [term.strip() for term in line.split("\t")]
                    cntusers[city][screen_name] = 1


            cntusers_stillonline = defaultdict(dict)
            with open("./all_network_stillonline_random_screenname_faceplusplus_name_imageurl.txt") as fi:
                for line_cnt, line in enumerate(fi):

                    city, screen_name, age_group, race, gender, name, profile_image_url, sample_type = [term.strip() for term in line.split("\t")]
                    if screen_name in screenname2cfrace:
                        cntusers_stillonline[city][screen_name] = 1

            cntlinks = defaultdict(lambda: defaultdict(int))
            cities = ["NY", "texas"]
            linkall = defaultdict(dict)
            global_cnt = 0
            for city in cities:
                inputfilename = "all_random_inferred_users_follower_network_%s.txt" % (city)
                outputfilename = "all_withcfrace_random_inferred_users_follower_network_%s.txt" % (city)
                
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

            outputfilename_random100 = "all_withcfrace_random_inferred_users_follower_network_random100.txt"

            with open(outputfilename_random100, "w") as output_random100:
                for mytag in linkall:
                    print "!!", mytag, len(linkall[mytag])
                    random100 = random.sample(linkall[mytag].keys(), 100)
                    for cnt in random100:
                        myline = linkall[mytag][cnt] 
                        output_random100.write(myline+"\n")

            misclass = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

            # cities = ["NY", "texas"]
            cities = ["random100"]
            for city in cities:

                inputfilename = "all_withcfrace_random_inferred_users_follower_network_%s.txt" % (city)

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

                        if test_method == "fpp":
                            from_race = from_race
                        elif test_method == "classifier":
                            if from_user in screenname2predrace:
                                from_race = screenname2predrace[from_user]

                        misclass[mytag][from_cfrace][from_race] += 1
                        misclass[mytag][from_cfrace]["total"] += 1
                        
                        if mytag in ["black_white", "black_black"]:
                            
                            myline = screenname2line[from_user]
                            myfpprace = myline.split("\t")[3]

                            if myfpprace == "Black":
                                output_image.write("%s\t%s" % (mytag, myline) + "\n")

            print "\n\n"
            print "==============================================="
            print "\t".join(["!!", param, test_method, pred_param])
            print "\n\n"

            output_all.write("==============================================="+"\n")
            output_all.write("\t".join(["!!", param, test_method, pred_param])+"\n\n")

            
            for city in ["NY", "texas"]:
                print city, "originally there were", cntlinks[city]["original"], "links with", len(cntusers[city])
                print "\t", "For",len(cntusers_stillonline[city]), "users who are still online and cf_conf %s are," % (str_cf_conf), "we have", cntlinks[city]["both"], "links"
                print "\n"
                
                output_all.write("%s, originally there were %d links with %d users. \n" % (city, cntlinks[city]["original"], len(cntusers[city])))
                output_all.write("For %d users who are still online and cf_agrrement %s, we have %d links.\n" % (len(cntusers_stillonline[city]),str_cf_conf, cntlinks[city]["both"]))
                output_all.write("\n")


            for mytag in ["white_white", "white_black", "black_white", "black_black"]:

                # if "asian" in mytag:
                #     continue
                print mytag, "--------"
                output_all.write("%s --------\n" % (mytag))
                for from_cfrace in misclass[mytag]:
                    myresult = [from_cfrace, "|"]
                    total = misclass[mytag][from_cfrace]["total"]
                    myheader = ["CF\\F++", "|"]
                    for from_race in misclass[mytag][from_cfrace]:
                        if not from_race == "total":
                            myheader.append(from_race)
                            myheader.append("|")
                            cnt = misclass[mytag][from_cfrace][from_race]
                            perc = float(cnt)/float(total)*100.0
                            myresult.append("%d(%.1f%%) |" % (cnt, perc))
                    print "\t".join(myheader)
                    print "\t".join(myresult)
                    print "\n"

                    output_all.write("\t".join(myheader)+"\n")
                    output_all.write("\t".join(myresult)+"\n")
                    output_all.write("\n")



