from collections import defaultdict
import sys

# total = 377410 ## NY
total = 143881 ## Texas
countAge = defaultdict(int)
countGender = defaultdict(int)
countRace = defaultdict(int)
# with open("screenname_age_race_gender_NY.txt") as fi, open("../../data/screenname_agegroup_race_gender_NY.txt", "w") as output:
with open("screenname_age_race_gender_Texas.txt") as fi, open("../../data/screenname_agegroup_race_gender_Texas.txt", "w") as output:
    for line_cnt, line in enumerate(fi):
        screenname, age, age_range, race, race_conf, gender, gender_conf = [term.strip() for term in line.split("\t")]
        age = int(age)

        myagegroup = ""
        # if age <= 12:
        #     myagegroup = "age-12"
        # elif age >= 13 and age <= 17:
        #     myagegroup = "age13-17"
        if age <= 17:
            myagegroup = "age-17"
        elif age >= 18 and age <= 24:
            myagegroup = "age18-24"
        elif age >= 25 and age <= 34:
            myagegroup = "age25-34"
        elif age >= 35 and age <= 44:
            myagegroup = "age35-44"
        elif age >= 45 and age <= 54:
            myagegroup = "age45-54"
        elif age >= 55:
            myagegroup = "age55-"
        # elif age >= 65:
        #     myagegroup = "age65-"


        countAge[myagegroup] += 1
        countGender[gender] += 1
        countRace[race] += 1

        output.write("\t".join([screenname, str(age), age_range, myagegroup, race, race_conf, gender, gender_conf])+"\n")
# for agegroup in sorted(countAge):
#     print agegroup, countAge[agegroup]


for each in sorted(countAge):
    print "[%s]" % (each), countAge[each], "(%.2f%%), " % ((float(countAge[each])/float(total))*100), 
