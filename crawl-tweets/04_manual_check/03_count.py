from collections import defaultdict
import math

user2demo = {}
with open("../../data/screenname_agegroup_race_gender_NY.txt") as fi:
    for line_cnt, line in enumerate(fi):
        screen_name, age, age_range, age_group, race, race_conf, gender, gender_conf = [term.strip() for term in line.split("\t")]

        user2demo[screen_name] = [age_group, gender, race, age]

print "len(user2demo) = ", len(user2demo)

cnt_type = defaultdict(int)
cnt_matched = defaultdict(int)

age_confusion = defaultdict(lambda: defaultdict(int))
gender_confusion = defaultdict(lambda: defaultdict(int))
new_cnt = defaultdict(int)
with open("./pattern_matched_users_2.txt") as fi, open("validation_age_diff.txt", "w") as output:

    for line_cnt, line in enumerate(fi):
        demotype, myvalue, screen_name = [term.strip() for term in line.split("\t")]

        if demotype == "age":
            age = int(myvalue)
            int_age = int(myvalue)
            myagegroup = ""
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
            myvalue = myagegroup


        cnt_type[myvalue] += 1

        # if screen_name in user2demo:
        age_group, gender, race, age = [term.strip() for term in user2demo[screen_name]]
        if demotype == "gender":
            if myvalue == gender:
                cnt_matched[myvalue] += 1
            gender_confusion[gender][myvalue] += 1
            new_cnt[gender] += 1
        if demotype == "age":
            if myvalue == age_group:
                cnt_matched[myvalue] += 1
            age_confusion[age_group][myvalue] += 1
            new_cnt[age_group] += 1

            diff_age = int(math.fabs(int_age - int(age)))
            output.write(str(diff_age)+"\n")
        

for group in sorted(cnt_matched):
    print group, cnt_type[group], cnt_matched[group]

myheader = [""]
for group in sorted(gender_confusion):
    group = group.replace("age","")
    myheader.append("\\textbf{%s}" % (group))
myheader.append("\\textbf{%s}" % ("Total"))
print " & ".join(myheader), "\\\\"
print "\\midrule"

for face_age in sorted(gender_confusion):
    mytotal = 0
    myresult = ["\\textbf{%s}" % (face_age)]
    for bio_age in sorted(gender_confusion[face_age]):
        myresult.append(str(gender_confusion[face_age][bio_age]))
        mytotal += gender_confusion[face_age][bio_age]
    myresult.append(str(mytotal))
    print " & ".join(myresult), "\\\\"
    # print ", ".join(myresult)

total_2 = 0
myresult = ["\\textbf{%s}" % ("Total")]
for bio_age in sorted(gender_confusion):
    myresult.append(str(cnt_type[bio_age]))
    total_2 += cnt_type[bio_age]
myresult.append(str(total_2))
print "\\midrule"
print " & ".join(myresult), "\\\\"

precisions = {}
recalls = {}
for face_age in sorted(gender_confusion):
    for bio_age in sorted(gender_confusion[face_age]):
        value = gender_confusion[face_age][bio_age]
        if face_age == bio_age:
            tp = value

    totalpredicted = new_cnt[face_age]
    totalgoldlable = cnt_type[face_age]
    
    recall = float(tp)/float(totalgoldlable)
    precision = float(tp)/float(totalpredicted)

    precisions[face_age] = "%.2f" % (precision)
    recalls[face_age] = "%.2f" % (recall)

myresult = [""]
for face_age in sorted(precisions):
    myresult.append("\\textbf{%s}" % (face_age))
print " & ".join(myresult), "\\\\"
print "\\midrule"

myresult = ["\\textbf{%s}" % ("Precision")]
for face_age in sorted(precisions):
    myresult.append(precisions[face_age])
print " & ".join(myresult), "\\\\"

myresult = ["\\textbf{%s}" % ("Recall")] 
for face_age in sorted(recalls):
    myresult.append(recalls[face_age])
print " & ".join(myresult), "\\\\"




myheader = [""]
for group in sorted(age_confusion):
    group = group.replace("age","")
    myheader.append("\\textbf{%s}" % (group))
myheader.append("\\textbf{%s}" % ("Total"))
print " & ".join(myheader), "\\\\"
print "\\midrule"

for face_age in sorted(age_confusion):
    mytotal = 0
    myresult = ["\\textbf{%s}" % (face_age)]
    for bio_age in sorted(age_confusion[face_age]):
        myresult.append(str(age_confusion[face_age][bio_age]))
        mytotal += age_confusion[face_age][bio_age]
    myresult.append(str(mytotal))
    print " & ".join(myresult), "\\\\"
    # print ", ".join(myresult)

total_2 = 0
myresult = ["\\textbf{%s}" % ("Total")]
for bio_age in sorted(age_confusion):
    myresult.append(str(cnt_type[bio_age]))
    total_2 += cnt_type[bio_age]
myresult.append(str(total_2))
print "\\midrule"
print " & ".join(myresult), "\\\\"

precisions = {}
recalls = {}
for face_age in sorted(age_confusion):
    for bio_age in sorted(age_confusion[face_age]):
        value = age_confusion[face_age][bio_age]
        if face_age == bio_age:
            tp = value

    totalpredicted = new_cnt[face_age]
    totalgoldlable = cnt_type[face_age]
    
    recall = float(tp)/float(totalgoldlable)
    precision = float(tp)/float(totalpredicted)

    precisions[face_age] = "%.2f" % (precision)
    recalls[face_age] = "%.2f" % (recall)

myresult = [""]
for face_age in sorted(precisions):
    myresult.append("\\textbf{%s}" % (face_age))
print " & ".join(myresult), "\\\\"
print "\\midrule"

myresult = ["\\textbf{%s}" % ("Precision")]
for face_age in sorted(precisions):
    myresult.append(precisions[face_age])
print " & ".join(myresult), "\\\\"

myresult = ["\\textbf{%s}" % ("Recall")] 
for face_age in sorted(recalls):
    myresult.append(recalls[face_age])
print " & ".join(myresult), "\\\\"
