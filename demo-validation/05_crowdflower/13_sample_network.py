import random

boolTest = False

param = "fr"



cities = ["NY", "texas"]
for city in cities:

    if param == "fr":
        inputfilename = "../../analysis/05_network/inferred_users_follower_network_%s.txt" % (city)
        outputfilename = "random_inferred_users_follower_network_%s.txt" % (city)

    mylinks = {}
    with open(inputfilename) as fi, open(outputfilename, "w") as output:
        for line_cnt, line in enumerate(fi):

            from_user, from_age, from_gender, from_race, to_user, to_age, to_gender, to_race, strength, meaning = [term.strip() for term in line.split("\t")]

            mylinks[line_cnt] = [from_user, from_race, to_user, to_race]
            

            if boolTest and line_cnt > 1000:
                break

        random_samples = random.sample(mylinks.keys(), 650)

        for link_cnt in sorted(random_samples):
            from_user, from_race, to_user, to_race = mylinks[link_cnt]
            output.write("\t".join([from_user, from_race, to_user, to_race])+"\n")
