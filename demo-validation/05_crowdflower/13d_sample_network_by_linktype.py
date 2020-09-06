import random
from collections import defaultdict

boolTest = False

list_count = ["", "2nd_", "3rd_", "4th_"]

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
    outputfilename = "5th_random_inferred_users_follower_network_%s.txt" % (city)

    mylinks = defaultdict(dict)
    with open(inputfilename) as fi, open(outputfilename, "w") as output:
        for line_cnt, line in enumerate(fi):

            from_user, from_age, from_gender, from_race, to_user, to_age, to_gender, to_race, strength, meaning = [term.strip() for term in line.split("\t")]

            if [from_user,to_user] in already:
                continue

            mylinktype = "%s_%s" % (from_race, to_race)
            # if mylinktype not in ["b_w", "b_b", "w_w", "w_b"]:
            if mylinktype not in ["b_w", "w_b"]:
                continue

            mylinks[mylinktype][line_cnt] = [from_user, from_race, to_user, to_race]
            

            if boolTest and line_cnt > 10000:
                break

        for mylinktype in mylinks:
            print mylinktype, len(mylinks[mylinktype].keys())
            random_samples = random.sample(mylinks[mylinktype].keys(), 400)

            for link_cnt in sorted(random_samples):
                from_user, from_race, to_user, to_race = mylinks[mylinktype][link_cnt]
                output.write("\t".join([from_user, from_race, to_user, to_race])+"\n")
