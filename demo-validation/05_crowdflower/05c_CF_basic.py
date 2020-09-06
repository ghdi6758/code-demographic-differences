from collections import defaultdict
import csv

boolTest = False
agreement = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
cnt_fpp_race = defaultdict(lambda: defaultdict(int))
cnt_cf_race = defaultdict(lambda: defaultdict(int))
cnt_city = defaultdict(int)




with open("./2nd_round_CF_aggregated_all.txt") as fi, open("./result_2nd_round_CF_face.txt", "w") as output:
    cnt_passed = 0
    screenname2cfrace = {}
    for line_cnt, line in enumerate(fi):
        screen_name, city, sample_type, fpp_race, cfrace_first_choice, cfrace_first_choice_conf, cfrace_first_rating, cfrace_first_rating_var, cfrace_second_choice, cfrace_second_choice_conf, cfrace_second_rating, cfrace_second_rating_var, name, image_url = [term.strip() for term in line.split("\t")]

        if sample_type == "random":
            
            cf_race = cfrace_first_choice
            confidence = float(cfrace_first_choice_conf)

            cnt_fpp_race[city][fpp_race] += 1
            if confidence > 0.9:
                cnt_passed += 1
                # print cf_race, confidence,  city, name, fpp_race, screen_name
                agreement[city][fpp_race][cf_race] += 1
                
                cnt_cf_race[city][cf_race] += 1
            else:
                agreement[city][fpp_race]["low_conf"] += 1
            cnt_city[city] += 1

            if boolTest and cnt_line > 5:
                break
        

    print "Out of %d samples, %d faces are classified by human coders." % (line_cnt, cnt_passed)

    print cnt_fpp_race
    print cnt_cf_race

    for city in agreement:
        output.write("\t".join([city, str(cnt_city[city])])+"\n")
        for fpp_race in sorted(agreement[city]):
            output.write("\t".join([fpp_race, str(cnt_fpp_race[city][fpp_race])])+"\n")
            list_myvalue = []
            list_frac = []
            for cf_race in ["white", "hispanic", "black", "asian", "other", "low_conf"]:
                if not agreement[city][fpp_race][cf_race]:
                    myvalue = 0 
                else:
                    myvalue = agreement[city][fpp_race][cf_race]
                frac = "%.4f" % (float(myvalue)/float(cnt_fpp_race[city][fpp_race]))
                list_myvalue.append(str(myvalue))
                list_frac.append(frac)

            output.write("\t".join(list_myvalue)+"\n")
            output.write("\t".join(list_frac)+"\n")
