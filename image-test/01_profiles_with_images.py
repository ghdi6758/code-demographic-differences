import glob
import sys

boolTest = False
allimages = [term.split("/")[2].replace(".jpg", "").split("_")[0] for term in glob.glob("./images/*")]

print len(allimages)
print allimages[100]


cities = ["NY", "texas"]
for city in cities:
    total_users = 0
    users_with_images = 0
    with open("../data/screenname_agegroup_race_gender_%s.txt" % (city)) as fi, open("./withimage_screenname_agegroup_race_gender_%s.txt" % (city), "w") as output:
        for line_cnt, line in enumerate(fi):
            screen_name, age, age_range, age_group, race, race_conf, gender, gender_conf = [term.strip() for term in line.split("\t")]

            if screen_name in allimages:
                users_with_images += 1
                output.write(line)
            total_users += 1

            if boolTest and line_cnt > 100:
                break

    print city, users_with_images, total_users
