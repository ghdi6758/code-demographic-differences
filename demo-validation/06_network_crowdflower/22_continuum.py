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
    else: 
        print "!!", race
        raise Exception("")
    return newrace

screenname2fpp = {}
with open("./screenname2fppraceandconf.txt") as fi:
    for line_cnt, line in enumerate(fi):
        city, screen_name, fpp_race, fpp_race_conf = [term.strip() for term in line.split("\t")]
        screenname2fpp[screen_name] = [fpp_race, fpp_race_conf]

list_sampling = ["", "5th_"]
# list_sampling = [""]

for sampling in list_sampling:

    cnt_no_fpp = 0
    if sampling == "":
        dataset = "Random edges"
        linktype = "fr_network"
    elif sampling == "5th_":
        dataset = "Selected edges"
        linktype = "fr_network_linktype"

    cities = ["NY", "texas"]

    screenname2cfrace = {}
    screenname2cfrace_3raters = {}
    with open("./5th_round_CF_aggregated_all.txt") as fi:
        for line_cnt, line in enumerate(fi):
            screen_name, city, sample_type, fpp_race, cfrace_first_choice, cfrace_first_choice_conf, cfrace_first_rating, cfrace_first_rating_var, cfrace_second_choice, cfrace_second_choice_conf, cfrace_second_rating, cfrace_second_rating_var, name, image_url = [term.strip() for term in line.split("\t")]
            
            if sample_type == linktype:

                cfrace_first_choice_conf = float(cfrace_first_choice_conf)
                cfrace_first_rating = float(cfrace_first_rating)

                screenname2cfrace[screen_name] = [cfrace_first_choice, cfrace_first_choice_conf, cfrace_first_rating]

                # if cfrace_first_choice_conf > 0.99:
                screenname2cfrace_3raters[screen_name] = [cfrace_first_choice, cfrace_first_choice_conf, cfrace_first_rating]
     

    with open("./continuum_check_%s.txt" % (dataset.split()[0]), "w") as output:
        # output.write("\t".join(["city", "cfrace_first_choice", "cfrace_first_choice_conf", "cfrace_first_rating", "fpp_race", "fpp_race_conf", "linktype", "usertype"]) +"\n")
        output.write("\t".join(["city", "conf_value", "conf_type", "linktype", "usertype"]) +"\n")

        for city in cities:
            inputfilename = "%srandom_inferred_users_follower_network_%s.txt" % (sampling, city)
            with open(inputfilename) as fi:
                for line_cnt, line in enumerate(fi):
                    
                    from_user, from_race, to_user, to_race = [term.strip() for term in line.split("\t")]

                    if from_user in screenname2cfrace_3raters:
                        from_cfrace_first_choice, from_cfrace_first_choice_conf, from_cfrace_first_rating = screenname2cfrace_3raters[from_user]
                        from_cfrace_first_rating = str(float(from_cfrace_first_rating)*0.1)
                        if to_user in screenname2cfrace_3raters:
                            to_cfrace_first_choice, to_cfrace_first_choice_conf, to_cfrace_first_rating = screenname2cfrace_3raters[to_user]
                            to_cfrace_first_rating = str(float(to_cfrace_first_rating)*0.1)

                            # mytag = "%s_%s" % (from_cfrace_first_choice, to_cfrace_first_choice)

                            if from_user in screenname2fpp:
                                from_fpp_race, from_fpp_race_conf = screenname2fpp[from_user]
                                from_fpp_race_conf = str(float(from_fpp_race_conf) * 0.01)
                            else:
                                cnt_no_fpp += 1
                            if to_user in screenname2fpp:
                                to_fpp_race, to_fpp_race_conf = screenname2fpp[to_user]
                                to_fpp_race_conf = str(float(to_fpp_race_conf) * 0.01)
                            else:
                                cnt_no_fpp += 1
                            
                            short_from_cfrace = shortrace(from_cfrace_first_choice)
                            short_to_cfrace = shortrace(to_cfrace_first_choice)
                            cftag = "%s->%s" % (short_from_cfrace, short_to_cfrace)

                            if cftag in ["w->w", "w->b", "b->w", "b->b"]:
                                output.write("\t".join([city, str(from_cfrace_first_choice_conf), "CF self-reported", cftag, "following"]) +"\n")

                                output.write("\t".join([city, from_cfrace_first_rating, "CF inter-agreement", cftag, "following"]) +"\n")

                                output.write("\t".join([city, from_fpp_race_conf, "F++ confidence", cftag, "following"]) +"\n")


                                output.write("\t".join([city, str(to_cfrace_first_choice_conf), "CF self-reported", cftag, "followed"]) +"\n")

                                output.write("\t".join([city, to_cfrace_first_rating, "CF inter-agreement", cftag, "followed"]) +"\n")

                                output.write("\t".join([city, to_fpp_race_conf, "F++ confidence", cftag, "followed"]) +"\n")

    print sampling, "cnt_no_fpp=", cnt_no_fpp
                            


