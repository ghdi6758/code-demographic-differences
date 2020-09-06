import random

boolTest = True


with open("./crowdflower_screenname_faceplusplus_name_imageurl_bio.tsv", "w") as output:
    output.write("\t".join(["city", "screen_name", "age_group", "race", "gender", "name", "image_url", "description"])+"\n")
    cities = ["NY", "texas"]
    for city in cities:

        multiplefaces = {}
        with open("../../crawl-tweets/03_faceplusplus/multiple_faces_%s.txt" % (city)) as fi:

            for line_cnt, line in enumerate(fi):
                screen_name = line.strip()
                multiplefaces[screen_name] = 1

        screenname2line = {}
        with open("./stillonline_random_screenname_faceplusplus_name_imageurl_bio_%s.txt" % (city)) as fi:

            for line_cnt, line in enumerate(fi):
                screen_name, age_group, race, gender, name, profile_image_url, description = [term.strip() for term in line.split("\t")]

                if screen_name in multiplefaces:
                    continue

                screenname2line[screen_name] = line
        print city
        print "Still online, one face=", len(screenname2line)
        print "Total=", line_cnt

        random_samples = random.sample(screenname2line.keys(), 1020)


        for screen_name in sorted(random_samples):
            myline = screenname2line[screen_name]
            output.write("%s\t%s" % (city, myline))
        
