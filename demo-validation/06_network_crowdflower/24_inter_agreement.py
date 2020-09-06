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
    next(fi)
    for line_cnt, line in enumerate(fi):
        city, screen_name, fpp_race, fpp_race_conf = [term.strip() for term in line.split("\t")]
        fpp_race_conf = str(float(fpp_race_conf) * 0.01)
        screenname2fpp[screen_name] = [fpp_race, fpp_race_conf]



list_sampling = ["1st_random", "1st_linktype"]
# list_sampling = [""]

with open("./inter_agreement_check_all.txt", "w") as output_all:
    output_all.write("\t".join(["city", "cfrace_first_choice", "cfrace_first_choice_conf", "cfrace_first_rating", "fpprace", "fpp_conf", "linktype"]) +"\n")
    for sampling in list_sampling:

        if sampling == "1st_random":
            dataset = "Random edges"
            linktype = "fr_network"
        elif sampling == "1st_linktype":
            dataset = "Selected edges"
            linktype = "fr_network_linktype"


        cities = ["NY", "texas"]

        screenname2cfrace = {}
        with open("./result_all/usonly_CF_aggregated_all.txt") as fi:
            for line_cnt, line in enumerate(fi):
                screen_name, city, sample_type, fpp_race, cfrace_first_choice, cfrace_first_choice_conf, cfrace_first_rating, cfrace_first_rating_var, cfrace_second_choice, cfrace_second_choice_conf, cfrace_second_rating, cfrace_second_rating_var, name, image_url = [term.strip() for term in line.split("\t")]
                
                if sample_type == linktype:

                    # cfrace_first_choice_conf = (cfrace_first_choice_conf)
                    cfrace_first_rating = str(float(cfrace_first_rating)*0.1)
                    if cfrace_first_choice in ["black", "white"]:
                        screenname2cfrace[screen_name] = [city, cfrace_first_choice, cfrace_first_choice_conf, cfrace_first_rating]

         

        # with open("./inter_agreement_check_%s.txt" % (dataset.split()[0]), "w") as output:
        #     output.write("\t".join(["city", "cfrace_first_choice", "cfrace_first_choice_conf", "cfrace_first_rating", "fpprace", "fpp_conf", "linktype"]) +"\n")

            for screen_name in sorted(screenname2cfrace):
                city, cfrace_first_choice, cfrace_first_choice_conf, cfrace_first_rating = screenname2cfrace[screen_name]
                if screen_name in screenname2fpp:
                    fpp_race, fpp_race_conf = screenname2fpp[screen_name]

                    # output.write("\t".join([city, cfrace_first_choice.title(), cfrace_first_choice_conf, cfrace_first_rating, fpp_race, fpp_race_conf, dataset])+"\n")

                    output_all.write("\t".join([city, cfrace_first_choice.title(), cfrace_first_choice_conf, cfrace_first_rating, fpp_race, fpp_race_conf, dataset])+"\n")



