import json
from collections import defaultdict
import codecs
import math

# boolTest = True

compare = defaultdict(lambda: defaultdict(list))
# with open("./CF_face_only_aggregated_all.txt") as fi:
with open("./CF_face_name_aggregated_all.txt") as fi:
    for line_cnt, line in enumerate(fi):
        screen_name, cf_race, confidence, city, name, image_url = [term.strip() for term in line.split("\t")]

        compare[city][screen_name] = [cf_race, confidence, name, image_url]



# for city in ["texas"]:
with codecs.open("./compare_conf_%s.txt" % (city), "w", "utf-8") as output:
    for city in ["NY", "texas"]:
        cnt_write_error = 0
        with open("../../crawl-tweets/03_faceplusplus/facepp_%s.txt" % (city)) as fi, codecs.open("./compare_conf_%s.txt" % (city), "w", "utf-8") as output:
            
            output.write("\t".join(["city", "screen_name", "cf_race", "cf_race_conf", "cf_race_group_3", "facepp_race", "facepp_race_conf", "facepp_group_3", "facepp_group_5", "facepp_group_10", "facepp_group_82"])+"\n")

            for line_cnt, line in enumerate(fi):
                try:
                    terms = [term.strip() for term in line.split("\t")]
                    screen_name = terms[0]

                    if screen_name in compare[city]:

                        result_json = json.loads(terms[1])
                        
                        facepp_race = result_json['face'][0]['attribute']['race']['value']
                        facepp_race_conf = (result_json['face'][0]['attribute']['race']['confidence'])

                        facepp_group_3 = int(math.floor(facepp_race_conf // 33.3333333))
                        facepp_group_5 = int(math.floor(facepp_race_conf // 20.0))
                        facepp_group_10 = int(math.floor(facepp_race_conf // 10.0))
                        
                        if facepp_race_conf >= 100.0:
                            facepp_group_3 = facepp_group_3 - 1
                            facepp_group_5 = facepp_group_5 - 1
                            facepp_group_10 = facepp_group_10 - 1

                        if facepp_race_conf >= 80:
                            facepp_group_82 = "[0.8,1]"
                        else:
                            facepp_group_82 = "[0,0.8)"

                        facepp_race_conf = str(facepp_race_conf * 0.01)

                        cf_race, cf_race_conf, name, image_url = compare[city][screen_name]
                        new_cf_race_conf = float(cf_race_conf)
                        if new_cf_race_conf < 0.4:
                            cf_race_group_3 = "0"
                        elif new_cf_race_conf < 0.7:
                            cf_race_group_3 = "1"
                        else:
                            cf_race_group_3 = "2"
                        
                        # print city, screen_name, cf_race, cf_race_conf, facepp_race, facepp_race_conf, name, image_url
                        try:
                            # output.write("\t".join([city, screen_name, cf_race, cf_race_conf, facepp_race, facepp_race_conf, name, image_url])+"\n")
                            output.write("\t".join([city, screen_name, cf_race, cf_race_conf, cf_race_group_3, facepp_race, facepp_race_conf, str(facepp_group_3), str(facepp_group_5), str(facepp_group_10), facepp_group_82])+"\n")
                        except:
                            print "error", city, screen_name, cf_race, cf_race_conf, facepp_race, facepp_race_conf
                            name = "name error"
                            output.write("\t".join([city, screen_name, cf_race, cf_race_conf, cf_race_group_3, facepp_race, facepp_race_conf, str(facepp_group_3), str(facepp_group_5), str(facepp_group_10), facepp_group_82])+"\n")
                            cnt_write_error += 1
                            
                        
                except:
                    raise
                    # continue
            print city, cnt_write_error
                # if boolTest and line_cnt > 50:
                #     break