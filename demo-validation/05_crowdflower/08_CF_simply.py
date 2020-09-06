from collections import defaultdict
import csv

boolTest = False
agreement = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
cnt_fpp_race = defaultdict(lambda: defaultdict(int))
cnt_cf_race = defaultdict(lambda: defaultdict(int))
cnt_city = defaultdict(int)

# with open('CF_aggregated_all.csv', 'rb') as csvfile, open("./CF_face_only_aggregated_all.txt","w") as output:
with open('CF_face_name_aggregated_all.csv', 'rb') as csvfile, open("./CF_face_name_aggregated_all.txt","w") as output:

    output.write("\t".join(["screen_name", "cf_race", "confidence", "city", "name", "image_url"])+"\n")
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
        confidence = (row[6])
        city = row[8]
        image_url = row[10]
        name = row[11]
        fpp_race = row[12]
        screen_name = row[13]

        output.write("\t".join([screen_name, cf_race, confidence, city, name, image_url])+"\n")
