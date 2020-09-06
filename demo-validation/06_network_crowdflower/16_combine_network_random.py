from collections import defaultdict
import random

cnt_lines = defaultdict(lambda: defaultdict(int))
# myparam = "1st_random"
myparam = "1st_linktype"

if myparam == "1st_random":
    linktype = "fr_network"
elif myparam == "1st_linktype":
    linktype = "fr_network_linetype"
    
with open("./crowdflower_cfonlyus_%s_screenname_faceplusplus_name_imageurl.tsv" % (myparam), "w") as output:

    output.write("\t".join(["city", "screen_name", "age_group", "race", "gender", "name", "image_url", "sample_type"])+"\n")


    with open("./cfonlyus_%s_network_stillonline_random_screenname_faceplusplus_name_imageurl.txt" % (myparam)) as fi:

        for line_cnt, line in enumerate(fi):
            city, screen_name, age_group, race, gender, name, profile_image_url, sample_type = [term.strip() for term in line.split("\t")]

            # output.write(line)
            output.write("\t".join([city, screen_name, age_group, race, gender, name, profile_image_url, linktype])+"\n")
            
            cnt_lines[sample_type][city] += 1

    print cnt_lines
