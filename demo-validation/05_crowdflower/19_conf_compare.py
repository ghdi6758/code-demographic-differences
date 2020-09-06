import json
from collections import defaultdict
import codecs
import math

# boolTest = True

compare = defaultdict(lambda: defaultdict(list))

with open("./2nd_round_CF_aggregated_all.txt") as fi, open("./2nd_round_screenname_cfnameonlyrace_fprace_nbrace_csrace.txt", "w") as output:
    cnt_passed = 0
    screenname2cfrace = {}
    for line_cnt, line in enumerate(fi):
        screen_name, city, sample_type, fpp_race, cfrace_first_choice, cfrace_first_choice_conf, cfrace_first_rating, cfrace_first_rating_var, cfrace_second_choice, cfrace_second_choice_conf, cfrace_second_rating, cfrace_second_rating_var, name, image_url = [term.strip() for term in line.split("\t")]

        if sample_type == "random":
            cf_race = cfrace_first_choice
            confidence = cfrace_first_rating
            compare[city][screen_name] = [cf_race, confidence, name, image_url]


for city in ["NY", "texas"]:
    cnt_write_error = 0
    with open("../../crawl-tweets/03_faceplusplus/facepp_%s.txt" % (city)) as fi, codecs.open("./2nd_compare_conf_%s.txt" % (city), "w", "utf-8") as output:
        
        output.write("\t".join(["city", "screen_name", "cf_race", "cf_race_conf", "cf_race_group_2", "facepp_race", "facepp_race_conf", "facepp_group_91"])+"\n")

        for line_cnt, line in enumerate(fi):
            try:
                terms = [term.strip() for term in line.split("\t")]
                screen_name = terms[0]

                if screen_name in compare[city]:

                    result_json = json.loads(terms[1])
                    
                    facepp_race = result_json['face'][0]['attribute']['race']['value']
                    facepp_race_conf = (result_json['face'][0]['attribute']['race']['confidence'])


                    if facepp_race_conf >= 90:
                        facepp_group_82 = "[0.9,1]"
                    else:
                        facepp_group_82 = "[0,0.9)"

                    facepp_race_conf = str(facepp_race_conf * 0.01)

                    cf_race, cf_race_conf, name, image_url = compare[city][screen_name]
                    new_cf_race_conf = float(cf_race_conf) 
                    
                    if new_cf_race_conf != 10:
                        cf_race_group_2 = "0"
                    else:
                        cf_race_group_2 = "1"
                    
                    try:
                        output.write("\t".join([city, screen_name, cf_race, cf_race_conf, cf_race_group_2, facepp_race, facepp_race_conf, facepp_group_82])+"\n")
                    except:
                        print "error", city, screen_name, cf_race, cf_race_conf, facepp_race, facepp_race_conf

                        raise
                        name = "name error"
                        output.write("\t".join([city, screen_name, cf_race, cf_race_conf, cf_race_group_2, facepp_race, facepp_race_conf, facepp_group_82])+"\n")
                        cnt_write_error += 1
                        
                    
            except:
                raise
                # continue
        print city, cnt_write_error
            # if boolTest and line_cnt > 50:
            #     break