from collections import defaultdict
import csv

boolTest = False
agreement = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
cnt_fpp_race = defaultdict(lambda: defaultdict(int))
cnt_cf_race = defaultdict(lambda: defaultdict(int))
cnt_city = defaultdict(int)

cnt_sampletype = defaultdict(int)
# with open('test.csv', 'rb') as csvfile, open("./test.txt","w") as output:
with open('5th_round_CF_aggregated_all.csv', 'rb') as csvfile, open("./5th_round_CF_aggregated_all.txt","w") as output:

    output.write("\t".join(["screen_name", "city", "sample_type", "fpp_race", "cfrace_first_choice", "cfrace_first_choice_conf", "cfrace_first_rating", "cfrace_first_rating_var", "cfrace_second_choice", "cfrace_second_choice_conf", "cfrace_second_rating", "cfrace_second_rating_var", "name", "image_url"])+"\n")
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    cnt_line = 0
    cnt_passed = 0


    for row in spamreader:

        # print row

        if cnt_line == 0:
            cnt_line += 1
            continue

        if len(row) != 21:
            print "ERROR", len(row), row
            continue

        _golden = row[1]

        state = row[2]

        if state == "golden":
            continue
            
        cfrace_second_choice = row[5]
        cfrace_second_choice_conf = row[6]
        cfrace_first_rating = row[7]
        cfrace_first_rating_var = row[8]
        cfrace_second_rating = row[9]
        cfrace_second_rating_var = row[10]
        cfrace_first_choice = row[11]
        cfrace_first_choice_conf = row[12]

        fpp_age_group = row[13]
        city = row[14]
        fpp_gender = row[15]
        image_url = row[16]
        name = row[17]
        fpp_race = row[18]
        sample_type = row[19]
        screen_name = row[20]
        cnt_sampletype[sample_type] += 1
        output.write("\t".join([screen_name, city, sample_type, fpp_race, cfrace_first_choice, cfrace_first_choice_conf, cfrace_first_rating, cfrace_first_rating_var, cfrace_second_choice, cfrace_second_choice_conf, cfrace_second_rating, cfrace_second_rating_var, name, image_url])+"\n")


print cnt_sampletype



# 0 _unit_id
# 1 _golden
# 2 _unit_state
# 3 _trusted_judgments
# 4 _last_judgment_at
# 5 whatd_be_your_second_choice_if_this_person_were_not_a_member_of_the_group_of_your_first_choice
# 6 whatd_be_your_second_choice_if_this_person_were_not_a_member_of_the_group_of_your_first_choice:confidence
# 7 whats_your_confidence_this_person_is_a_member_of_group_
# 8 whats_your_confidence_this_person_is_a_member_of_group_:variance
# 9 whats_your_confidence_this_person_is_a_member_of_group_of_your_second_choice_
# 10 whats_your_confidence_this_person_is_a_member_of_group_of_your_second_choice_:variance
# 11 which_categories_describe_this_person
# 12 which_categories_describe_this_person:confidence
# 13 age_group
# 14 city
# 15 gender
# 16 image_url
# 17 name
# 18 race
# 19 sample_type
# 20 screen_name
# 21 whatd_be_your_second_choice_if_this_person_were_not_a_member_of_the_group_of_your_first_choice_gold
# 22 whats_your_confidence_this_person_is_a_member_of_group__gold
# 23 whats_your_confidence_this_person_is_a_member_of_group_of_your_second_choice__gold
# 24 which_categories_describe_this_person_gold

