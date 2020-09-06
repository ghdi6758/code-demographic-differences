from collections import defaultdict
import random

cnt_lines = defaultdict(lambda: defaultdict(int))
myparam = "1st_random"
# myparam = "1st_linktype"


    
all_lines = {}
for myparam in ["1st_random", "1st_linktype"]:
    if myparam == "1st_random":
        linktype = "fr_network"
    elif myparam == "1st_linktype":
        linktype = "fr_network_linetype"

    with open("./crowdflower_cfonlyus_%s_screenname_faceplusplus_name_imageurl.tsv" % (myparam), "r") as fi:

        next(fi)
        
        for line_cnt, line in enumerate(fi):
            city, screen_name, age_group, race, gender, name, profile_image_url, linktype = [term.strip() for term in line.split("\t")]
            all_lines[screen_name] = line.strip()


with open("./crowdflower_cfonlyus_all_screenname_faceplusplus_name_imageurl.tsv", "w") as output:

    output.write("\t".join(["city", "screen_name", "age_group", "race", "gender", "name", "image_url", "sample_type"])+"\n")

    for screen_name in sorted(all_lines):
        myline = all_lines[screen_name]
        output.write(myline+"\n")
