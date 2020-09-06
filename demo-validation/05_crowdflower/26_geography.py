from collections import defaultdict
import operator

cnt_country = defaultdict(lambda: defaultdict(int))
with open("./cf_results/5th_round_CF_contributors_all.txt") as fi:
    for line_cnt, line in enumerate(fi):
        sample_type, worker_id, withindata_judgments_count, judgments_count, country, trust_overall = [term.strip() for term in line.split("\t")]
        cnt_country[sample_type][country] += 1


for sampling in cnt_country:
    print sampling
    rank = 1
    for mytuple in sorted(cnt_country[sampling].items(), key=operator.itemgetter(1), reverse=True)[0:10]:
        print "[%d]" % (rank), mytuple[0], mytuple[1]
        rank += 1
