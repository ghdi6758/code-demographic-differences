import json
from collections import defaultdict
import codecs


firstnames = {}
lastnames = {}
with open("./black_names_examples.tsv") as fi:
    for line_cnt, line in enumerate(fi):
        name_type, name = [term.strip() for term in line.split("\t")]
        name = name.lower()
        if name_type == "first":
            firstnames[name] = 1
        elif name_type == "last":
            lastnames[name] = 1

compare = defaultdict(lambda: defaultdict(list))
# with open("./CF_face_only_aggregated_all.txt") as fi:
with open("./CF_face_name_aggregated_all.txt") as fi:
    for line_cnt, line in enumerate(fi):
        screen_name, cf_race, confidence, city, name, image_url = [term.strip() for term in line.split("\t")]

        newname = name.split(" ")


        # print newname
        nofirst = " ".join(newname[1:])
        # print nofirst
        for each_last in lastnames:
            if each_last in nofirst.lower():
                print "@@ last matched", each_last, name

                myfirst = newname[0].lower()
                if myfirst in firstnames:
                    isblack = 1
                    print "!! first matched", name

        # compare[city][screen_name] = [cf_race, confidence, name, image_url]

