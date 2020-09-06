import random

with open("./2ndround_random_screenname_faceplusplus_name_imageurl.txt", "w") as output:

    cities = ["NY", "texas"]
    for city in cities:

        multiplefaces = {}
        with open("../../crawl-tweets/03_faceplusplus/multiple_faces_%s.txt" % (city)) as fi:
            for line_cnt, line in enumerate(fi):
                screen_name = line.strip()
                multiplefaces[screen_name] = 1
                

        screenname2line = {}
        black2line = {}
        with open("./screenname_faceplusplus_name_imageurl_bio_%s.txt" % (city)) as fi:
            for line_cnt, line in enumerate(fi):

                screen_name, age_group, race, gender, name, profile_image_url, description = [term.strip() for term in line.split("\t")]

                if screen_name in multiplefaces:
                    continue

                name = name.replace(",", " ")
                screenname2line[screen_name] = [screen_name, age_group, race, race, name, profile_image_url]
                if race == "Black":
                    black2line[screen_name] = [screen_name, age_group, race, gender, name, profile_image_url]

        print len(screenname2line)
        
        random_samples = random.sample(screenname2line.keys(), 1500)
        for screen_name in sorted(random_samples):
            screen_name, age_group, race, race, name, profile_image_url = screenname2line[screen_name]
            output.write("\t".join([city, screen_name, age_group, race, race, name, profile_image_url, "random"])+"\n")
        
        random_samples = random.sample(black2line.keys(), 700)
        for screen_name in sorted(random_samples):
            screen_name, age_group, race, race, name, profile_image_url = black2line[screen_name]
            output.write("\t".join([city, screen_name, age_group, race, race, name, profile_image_url, "black_random"])+"\n")


