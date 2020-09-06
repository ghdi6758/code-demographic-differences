from dateutil.parser import *
from collections import defaultdict
import sys

boolTest = False



with open("r_overtime.txt", "w") as output:
    output.write("\t".join(["dataset", "target_race", "cnt_prev_seen", "str_prob"])+"\n")
    
    for linktype in ["fr_network", "fr_network_linktype"]:

        timeseries = defaultdict(dict)

        if linktype == "fr_network":
            dataset = "Random edges"
        elif linktype == "fr_network_linktype":
            dataset = "Selected edges"

        screenname2cfrace = {}
        screenname2cfrace_3raters = {}
        with open("./5th_round_CF_aggregated_all.txt") as fi:
            for line_cnt, line in enumerate(fi):
                screen_name, city, sample_type, fpp_race, cfrace_first_choice, cfrace_first_choice_conf, cfrace_first_rating, cfrace_first_rating_var, cfrace_second_choice, cfrace_second_choice_conf, cfrace_second_rating, cfrace_second_rating_var, name, image_url = [term.strip() for term in line.split("\t")]
                
                if sample_type == linktype:
                    cfrace_first_choice_conf = float(cfrace_first_choice_conf)
                    cfrace_first_rating = float(cfrace_first_rating)
                    screenname2cfrace[screen_name] = cfrace_first_choice
                    if cfrace_first_choice_conf > 0.99:
                        screenname2cfrace_3raters[screen_name] = cfrace_first_choice

        with open("./cf_results/5th_round_CF_full_all.txt") as fi:
            next(fi)
            for line_cnt, line in enumerate(fi):
                unit_id, screen_name, city, sample_type, fpp_race, cfrace_first_choice, cfrace_first_rating, cfrace_second_choice, cfrace_second_rating, worker_id, created_at, judgments_count, country, trust_overall = [term.strip() for term in line.split("\t")]

                if sample_type == linktype:
                    if screen_name not in screenname2cfrace:
                        continue

                    cf_race = screenname2cfrace[screen_name]
                    created_at = parse(created_at)
                    timeseries[worker_id][created_at] = [cf_race.title(), fpp_race.title(), cfrace_first_choice.title()]
                    
                    if boolTest and line_cnt > 100:
                        break

        
        for target_race in ["White", "Black", "Asian"]:

            cnt_total = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
            cnt_tag_black = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

            for worker_cnt, worker_id in enumerate(timeseries):
                times_seen_race = defaultdict(int)
                nth_task = 1
                for mytimeslot in sorted(timeseries[worker_id]):
                    cf_race, fpp_race, cfrace_first_choice = timeseries[worker_id][mytimeslot]

                    # print worker_id, mytimeslot, cf_race, fpp_race, cfrace_first_choice

                    ### what you see at n-th task
                    seen_race = cf_race
                    # if seen_race in ["Black", "White"]:
                    if seen_race == target_race:
                        # cnt_total[seen_race][times_seen_race[target_race]][nth_task] += 1
                        cnt_total[seen_race][times_seen_race[target_race]]["all"] += 1
                        # sys.exit()
                        if cfrace_first_choice == target_race:
                            # cnt_tag_black[seen_race][times_seen_race[target_race]][nth_task] += 1
                            cnt_tag_black[seen_race][times_seen_race[target_race]]["all"] += 1

                        # print "!!", worker_id, mytimeslot, target_race, seen_race, times_seen_race[target_race], cfrace_first_choice
                        # print cnt_total, cnt_tag_black
                    if seen_race == target_race:
                        times_seen_race[target_race] += 1

                    nth_task += 1

                # if worker_cnt >3:
                #     sys.exit()


            print "===", dataset, ", Target race is", target_race
            for seen_race in cnt_tag_black:
                print "When a person saw", seen_race, "(by CF), "
                for cnt_prev_seen in sorted(cnt_tag_black[seen_race]):
                    mycnt = float(cnt_tag_black[seen_race][cnt_prev_seen]["all"])
                    totalcnt = float(cnt_total[seen_race][cnt_prev_seen]["all"])
                    prob = mycnt/totalcnt

                    if totalcnt <= 10:
                        continue

                    print "\tgiven he previously saw", target_race, cnt_prev_seen, "times,"                    
                    print "\t\tthe probability to tag him as", target_race, "is", "%.3f" % (prob), "(%.0f/%.0f)" % (mycnt,totalcnt)

                    str_prob = "%.3f" % (prob)
                    str_cnt_prev_seen = str(cnt_prev_seen)
                    output.write("\t".join([dataset, target_race, str_cnt_prev_seen, str_prob])+"\n")



        # print "===", dataset, ", Target race is", target_race
        # for seen_race in cnt_tag_black:
        #     print "When a person saw", seen_race, "(by CF), "
        #     for cnt_prev_seen in sorted(cnt_tag_black[seen_race]):
        #         print "\tgiven he previously saw", target_race, cnt_prev_seen, "times,"
        #         for nth_task in sorted(cnt_tag_black[seen_race][cnt_prev_seen]):
        #             mycnt = float(cnt_tag_black[seen_race][cnt_prev_seen][nth_task])
        #             totalcnt = float(cnt_total[seen_race][cnt_prev_seen]["all"])
        #             prob = mycnt/totalcnt

        #             print "\t\tthe probability to tag him as", target_race, "at his %d-th task" % (nth_task), "is", "%.3f" % (prob), "(%.0f/%.0f)" % (mycnt,totalcnt)



