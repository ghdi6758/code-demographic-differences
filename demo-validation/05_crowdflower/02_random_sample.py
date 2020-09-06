import random


cities = ["NY", "texas"]
for city in cities:

    screenname2line = {}
    with open("./screenname_faceplusplus_name_imageurl_bio_%s.txt" % (city)) as fi:
        for line_cnt, line in enumerate(fi):
            screen_name, age_group, race, gender, name, profile_image_url, description = [term.strip() for term in line.split("\t")]

            screenname2line[screen_name] = line

            
    random_samples = random.sample(screenname2line.keys(), 3000)

    with open("./random_screenname_faceplusplus_name_imageurl_bio_%s.txt" % (city), "w") as output:
        for screen_name in sorted(random_samples):
            myline = screenname2line[screen_name]
            output.write(myline)
        
