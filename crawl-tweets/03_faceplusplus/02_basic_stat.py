from collections import defaultdict

# total = 377410 #NY
total = 143881 #Texas

countGender = defaultdict(int)
countRace = defaultdict(int)
countAge = defaultdict(int)
# with open("../../data/screenname_age_race_gender_NY.txt") as fi:
with open("./screenname_age_race_gender_Texas.txt") as fi:
    for line_cnt, line in enumerate(fi):
        screenname, age, age_range, race, race_conf, gender, gender_conf = [term.strip() for term in line.split("\t")]
        age = float(age)
        bin_age = int(age / 10)
        countAge[bin_age] += 1
        countGender[gender] += 1
        countRace[race] += 1


for each in countGender:
    print "[%s]" % (each), countGender[each], "(%.2f%%), " % ((float(countGender[each])/float(total))*100),

print "\n"
for each in countRace:
    print "[%s]" % (each), countRace[each], "(%.2f%%), " % ((float(countRace[each])/float(total))*100), 

print "\n"
for each in countAge:
    print "[%s]" % (each), countAge[each], "(%.2f%%), " % ((float(countAge[each])/float(total))*100), 
