from collections import defaultdict
import csv

boolTest = False
agreement = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
cnt_fpp_race = defaultdict(lambda: defaultdict(int))
cnt_cf_race = defaultdict(lambda: defaultdict(int))
cnt_city = defaultdict(int)

# with open('CF_aggregated_all.csv', 'rb') as csvfile, open("./result_CF_face.txt","w") as output:
with open('CF_face_name_aggregated_all.csv', 'rb') as csvfile, open("./result_CF_face_name.txt","w") as output:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    cnt_line = 0
    cnt_passed = 0
    for row in spamreader:
        if cnt_line == 0:
            cnt_line += 1
            continue

        state = row[2]

        if state != "finalized":
            continue
        cf_race = row[5]
        confidence = float(row[6])
        city = row[8]
        name = row[11]
        fpp_race = row[12]
        screen_name = row[13]

        # if screen_name not in target_users:
        #     print screen_name
        #     continue

        confidence = float(confidence)

        cnt_fpp_race[city][fpp_race] += 1
        if confidence > 0.9:
            cnt_passed += 1
            # print cf_race, confidence,  city, name, fpp_race, screen_name
            agreement[city][fpp_race][cf_race] += 1
            
            cnt_cf_race[city][cf_race] += 1
        else:
            agreement[city][fpp_race]["low_conf"] += 1
        cnt_city[city] += 1
        cnt_line += 1
        if boolTest and cnt_line > 5:
            break
        

    print "Out of %d samples, %d faces are classified by human coders." % (cnt_line, cnt_passed)

    print cnt_fpp_race
    print cnt_cf_race

    
    for city in agreement:
        output.write("\t".join([city, str(cnt_city[city])])+"\n")
        for fpp_race in sorted(agreement[city]):
            output.write("\t".join([fpp_race, str(cnt_fpp_race[city][fpp_race])])+"\n")
            list_myvalue = []
            list_frac = []
            for cf_race in ["white", "hispanic", "black", "asian", "other", "low_conf"]:
                if not agreement[city][fpp_race][cf_race]:
                    myvalue = 0 
                else:
                    myvalue = agreement[city][fpp_race][cf_race]
                frac = "%.4f" % (float(myvalue)/float(cnt_fpp_race[city][fpp_race]))
                list_myvalue.append(str(myvalue))
                list_frac.append(frac)

            output.write("\t".join(list_myvalue)+"\n")
            output.write("\t".join(list_frac)+"\n")


                # print ""

            
