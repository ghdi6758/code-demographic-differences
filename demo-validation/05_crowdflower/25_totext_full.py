from collections import defaultdict
import csv

boolTest = False

workers = {}
with open('./cf_results/workset912623.csv', 'rb') as csvfile:


    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    cnt_line = 0
    cnt_passed = 0

    for row in spamreader:

        if cnt_line == 0:
            cnt_line += 1
            continue

        worker_id = row[0]
        judgments_count = int(row[2])

        if judgments_count == 0: 
            continue
        country = row[7]
        trust_overall = row[15]

        workers[worker_id] = [str(judgments_count), country, trust_overall]

print "Number of workers=", len(workers)


target_workers = defaultdict(lambda: defaultdict(int))
cnt_sampletype = defaultdict(int)
with open('./cf_results/f912623.csv', 'rb') as csvfile, open("./cf_results/5th_round_CF_full_all.txt", "w") as output, open("./cf_results/5th_round_CF_contributors_all.txt", "w") as output_workers:

    output.write("\t".join(["unit_id", "screen_name", "city", "sample_type", "fpp_race", "cfrace_first_choice", "cfrace_first_rating", "cfrace_second_choice", "cfrace_second_rating", "worker_id", "created_at", "judgments_count", "country", "trust_overall"])+"\n")

    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    cnt_line = 0

    for row in spamreader:
        if cnt_line == 0:
            cnt_line += 1
            continue

        if len(row) != 26:
            print "ERROR", len(row), row
            continue

        unit_id = row[0]
        created_at = row[1]
        golden = row[2]
        if golden == "TRUE":
            continue

        worker_id = row[9]
        cfrace_second_choice = row[14]
        cfrace_first_rating = row[15]
        cfrace_second_rating = row[16]
        cfrace_first_choice = row[17]
        fpp_age_group = row[18]
        city = row[19]
        fpp_gender = row[20]
        image_url = row[21]
        name = row[22]
        fpp_race = row[23]
        sample_type = row[24]
        screen_name = row[25]

        cnt_sampletype[sample_type] += 1

        if sample_type in ["fr_network", "fr_network_linetype"]:
            if worker_id in workers:
                judgments_count, country, trust_overall = workers[worker_id]

                if sample_type == "fr_network_linetype":
                    sample_type = "fr_network_linktype"


                target_workers[sample_type][worker_id] +=1

                output.write("\t".join([unit_id, screen_name, city, sample_type, fpp_race, cfrace_first_choice.title(), cfrace_first_rating, cfrace_second_choice.title(), cfrace_second_rating, worker_id, created_at, judgments_count, country, trust_overall])+"\n")


    output_workers.write("\t".join(["sample_type", "worker_id", "withindata_judgments_count", "judgments_count", "country", "trust_overall"])+"\n")

    for sample_type in target_workers:
        for worker_id in target_workers[sample_type]:
            judgments_count, country, trust_overall = workers[worker_id]
            withindata_judgments_count = target_workers[sample_type][worker_id]


            output_workers.write("\t".join([sample_type, worker_id, str(withindata_judgments_count), judgments_count, country, trust_overall])+"\n")

print cnt_sampletype

print "Workers of interest=", len(target_workers)


# 0 '_unit_id'
# 1 '_created_at'
# 2 '_golden' 
# 3 '_id' 
# 4 '_missed' 
# 5 '_started_at' 
# 6 '_tainted' 
# 7 '_channel' 
# 8 '_trust' 
# 9 '_worker_id' 
# 10 '_country' 
# 11 '_region' 
# 12 '_city' 
# 13 '_ip' 
# 14 'whatd_be_your_second_choice_if_this_person_were_not_a_member_of_the_group_of_your_first_choice' 
# 15 'whats_your_confidence_this_person_is_a_member_of_group_' 
# 16 'whats_your_confidence_this_person_is_a_member_of_group_of_your_second_choice_' 
# 17 'which_categories_describe_this_person' 
# 18 'age_group' 
# 19 'city' 
# 20 'gender' 
# 21 'image_url' 
# 22 'name' 
# 23 'race' 
# 24 'sample_type' 
# 25 'screen_name'




# 0 'worker_id'
# 1 'external_id'
# 2 'judgments_count'
# 3 'missed_count'
# 4 'golds_count'
# 5 'forgiven_count'
# 6 'channel'
# 7 'country'
# 8 'region'
# 9 'city'
# 10 'last_ip'
# 11 'flagged_at'
# 12 'rejected_at'
# 13 'bonus'
# 14 'flag_reason'
# 15 'trust_overall'
# 16 'submission_rate'
# 17 'level_1_contributors'