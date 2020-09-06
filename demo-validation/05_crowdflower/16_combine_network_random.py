from collections import defaultdict
import random

cnt_lines = defaultdict(lambda: defaultdict(int))

with open("./crowdflower_6thround_screenname_faceplusplus_name_imageurl.tsv", "w") as output:

    output.write("\t".join(["city", "screen_name", "age_group", "race", "gender", "name", "image_url", "sample_type"])+"\n")

    # with open("./2ndround_stillonline_random_screenname_faceplusplus_name_imageurl.txt") as fi:

    #     for line_cnt, line in enumerate(fi):
    #         city, screen_name, age_group, race, gender, name, profile_image_url, sample_type = [term.strip() for term in line.split("\t")]

    #         output.write(line)

    #         cnt_lines[sample_type][city] += 1


    with open("./5th_network_stillonline_random_screenname_faceplusplus_name_imageurl.txt") as fi:

        for line_cnt, line in enumerate(fi):
            city, screen_name, age_group, race, gender, name, profile_image_url, sample_type = [term.strip() for term in line.split("\t")]

            # output.write(line)
            output.write("\t".join([city, screen_name, age_group, race, gender, name, profile_image_url, "fr_network_linetype"])+"\n")
            
            cnt_lines[sample_type][city] += 1

    print cnt_lines
