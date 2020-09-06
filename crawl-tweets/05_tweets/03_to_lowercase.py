import sys

with open("./sorted_user_time_tweetid_hashtag.txt") as fi, open("../../data/sorted_user_time_tweetid_hashtag_lower.txt", "w") as output:
    for line_cnt, line in enumerate(fi):
        screenname, createdat, tweetid, hashtag = [term.strip() for term in line.split("\t")]
        hashtag = hashtag.lower()
        output.write("\t".join([screenname, createdat, tweetid, hashtag])+"\n")
