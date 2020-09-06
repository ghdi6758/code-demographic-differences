
cities = ["NY", "texas"]
for city in cities:

    screen2fprace = {}
    with open("./screenname_faceplusplus_name_imageurl_bio_%s.txt" % (city)) as fi:
        for line_cnt, line in enumerate(fi):
            screen_name, age_group, race, gender, name, profile_image_url, description = [term.strip() for term in line.split("\t")]

            if race == "Black": race = "b"
            elif race == "Asian": race = "a"
            elif race == "White": race = "w"

            screen2fprace[screen_name] = race

    inputfilename = "random_inferred_users_follower_network_%s.txt" % (city)
    outputputfilename = "random_inferred_users_follower_network_%s_new.txt" % (city)
    with open(inputfilename) as fi, open(outputputfilename,"w") as output:

        for line_cnt, line in enumerate(fi):
            from_user, from_race, to_user, to_race = [term.strip() for term in line.split("\t")]

            if from_user in screen2fprace:
                new_from_race = screen2fprace[from_user]

            if to_user in screen2fprace:
                new_to_race = screen2fprace[to_user]

            output.write("\t".join([from_user, new_from_race, to_user, new_to_race])+"\n")
