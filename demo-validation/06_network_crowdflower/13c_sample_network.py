import random

boolTest = False

list_count = []
myparam = "1st_random"

cities = ["NY", "texas"]
for city in cities:

    already = []
    for myround in list_count:
        inputfilename = "%srandom_inferred_users_follower_network_%s.txt" % (myround, city)

        with open(inputfilename) as fi:
            for line_cnt, line in enumerate(fi):

                from_user, from_race, to_user, to_race = [term.strip() for term in line.split("\t")]

                already.append([from_user,to_user])

    print city, "already=", len(already)

    
    inputfilename = "../../analysis/05_network/inferred_users_follower_network_%s.txt" % (city)
    outputfilename = "cfonlyus_%s_random_inferred_users_follower_network_%s.txt" % (myparam, city)

    mylinks = {}
    with open(inputfilename) as fi, open(outputfilename, "w") as output:
        for line_cnt, line in enumerate(fi):

            from_user, from_age, from_gender, from_race, to_user, to_age, to_gender, to_race, strength, meaning = [term.strip() for term in line.split("\t")]

            if [from_user,to_user] in already:
                continue

            mylinks[line_cnt] = [from_user, from_race, to_user, to_race]
            

            if boolTest and line_cnt > 1000:
                break

        random_samples = random.sample(mylinks.keys(), 2000)

        for link_cnt in sorted(random_samples):
            from_user, from_race, to_user, to_race = mylinks[link_cnt]
            output.write("\t".join([from_user, from_race, to_user, to_race, "fr_network"])+"\n")
