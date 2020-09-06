import json
from collections import defaultdict
import codecs
import math

screenname2fpp = defaultdict(list)


with open("./screenname2fppraceandconf.txt", "w") as output:
    output.write("\t".join(["city", "screen_name", "facepp_race", "facepp_race_conf"])+"\n")
    
    for city in ["NY", "texas"]:
        with open("../../crawl-tweets/03_faceplusplus/facepp_%s.txt" % (city)) as fi:
            for line_cnt, line in enumerate(fi):

                terms = [term.strip() for term in line.split("\t")]
                screen_name = terms[0]

                if terms[1] == "error":
                    continue

                try:
                    result_json = json.loads(terms[1])            
                    facepp_race = result_json['face'][0]['attribute']['race']['value']
                    facepp_race_conf = (result_json['face'][0]['attribute']['race']['confidence'])

                    screenname2fpp[screen_name] = [city, facepp_race, str(facepp_race_conf)]
                except:
                    print "JSON not complete"
                

    print len(screenname2fpp)
    for screen_name in sorted(screenname2fpp):
        city, facepp_race, facepp_race_conf = screenname2fpp[screen_name]
        
        output.write("\t".join([city, screen_name, facepp_race, facepp_race_conf])+"\n")