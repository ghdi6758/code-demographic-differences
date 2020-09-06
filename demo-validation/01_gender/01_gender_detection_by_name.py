# -*- coding: utf-8 -*- 

from collections import defaultdict
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

boolTest = False

def load_gender_dict():
    name_gender = {}
    with open("../../offlinedata/common_data/name_gender.txt", 'r') as inputfile:
        for line_cnt, line in enumerate(inputfile):
            gender, name = [term.strip().lower() for term in line.split("\t")]      
            name_gender[name] = gender

    with open("../../offlinedata/common_data/gabrielNameDictionary.txt", 'r') as inputfile:
        for line_cnt, line in enumerate(inputfile):
            name, gender = [term.strip().lower() for term in line.split("\t")]
            name_gender[name] = gender

    print "... Loaded GENDER dictionary"
    print "Num of gender dictionary", len(name_gender)

    return name_gender


def load_race_dict():
    name_race = {}
    with open("../../offlinedata/common_data/name_race.txt", 'r') as inputfile:
        inputfile.next()
        for line_cnt, line in enumerate(inputfile):
            terms = [term.strip() for term in line.split("\t")]
            name = terms[0].lower()

            try:
                floats = [float(term)*0.01 for term in terms[5:11]]
            except:
                print terms[5:11]
            race = [floats[0], floats[1], floats[3], floats[5]]
            name_race[name] = race

            print line
            print name, race
            sys.exit()
    print "... Loaded RACE dictionary"
    print "Num of race dictionary", len(name_race)

    return name_race

name2gender = load_gender_dict()
# name2race = load_race_dict()

# list_files = ["human_bios_newyork", "facepp_bios_newyork"]
# list_files = ["facepp_bios_newyork"]
list_files = ["facepp_bios_texas"]

city = "texas"
gender_dist = defaultdict(lambda: defaultdict(int))

for filename in list_files:
    with open("../../data/%s.txt" % (filename)) as fi, open("./screenname_nb_gender_%s.txt" % (city), "w") as output:
        for line_cnt, line in enumerate(fi):
            userid, screen_name, name, location, lang, days_since_join, statuses_count, followers_count, friends_count, listed_count, favourites_count, profile_image_url, description, days_since_active = [term.strip() for term in line.split("\t")]

            try:
                firstname = name.split()[0].lower()
            except:
                print "Name error", name
                continue

            if firstname in name2gender:
                gender = name2gender[firstname]
            else:
                gender = "NA"
                
            output.write("\t".join([screen_name, gender])+"\n")

            gender_dist[filename][gender] += 1
            gender_dist[filename]["total"] += 1
            if boolTest and line_cnt > 100:
                break

print ""
with open("./datasets_gender_proportion_%s.txt" % (city), "w") as output:
    for filename in list_files:
        for gender in sorted(gender_dist[filename]):
            if gender != "total":
                cnt_gender = gender_dist[filename][gender]
                ratio = "(%.2f%%)" % (float(cnt_gender)/float(gender_dist[filename]["total"])*100.0)
                print filename, gender, cnt_gender, ratio
                output.write("\t".join([filename, gender, str(cnt_gender), ratio])+"\n")


