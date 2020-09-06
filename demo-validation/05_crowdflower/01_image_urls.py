
cities = ["NY", "texas"]
for city in cities:
    with open("../../analysis/05_network/screenname_agegroup_race_gender_bios_%s.txt" % (city)) as fi, open("./screenname_faceplusplus_name_imageurl_bio_%s.txt" % (city), "w") as output:
        for line_cnt, line in enumerate(fi):
            screen_name, age_group, race, gender, userid, name, location, lang, days_since_join, statuses_count, followers_count, friends_count, listed_count, favourites_count, profile_image_url, description, days_since_active = [term.strip() for term in line.split("\t")]

            output.write("\t".join([screen_name, age_group, race, gender, name, profile_image_url, description])+"\n")

        
