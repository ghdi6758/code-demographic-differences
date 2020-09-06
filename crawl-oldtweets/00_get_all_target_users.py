cities = ["NY", "texas"]
for city in cities:
    user2demo = {}
    with open("../data/facepp_bios_%s.txt" % (city)) as fi:
        for line_cnt, line in enumerate(fi):
            userid, screen_name, name, location, lang, days_since_join, statuses_count, followers_count, friends_count, listed_count, favourites_count, profile_image_url, description, days_since_active = [term.strip() for term in line.split("\t")]
            user2demo[userid] = screen_name
            
    # with open("../data/screenname_agegroup_race_gender_bios_%s.txt" % (city)) as fi:
    #     for line_cnt, line in enumerate(fi):
    #         screen_name, age_group, race, gender, userid, name, location, lang, days_since_join, statuses_count, followers_count, friends_count, listed_count, favourites_count, profile_image_url, description, days_since_active = [term.strip() for term in line.split("\t")]
    #         user2demo[screen_name] = [age_group, gender, race]
    print "number of users with demographics=", city, len(user2demo)
