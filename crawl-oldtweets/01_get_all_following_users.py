
boolTest = False
city = "NY"
inputfilename = "../analysis/05_network/only_following_network_strength_%s.txt" % (city)
# totallines = "16,437,982" ## Texas
# inferred_users_follower_network_NY.txt

cnt_links = 0
all_from_users = set()
all_to_users = set()
with open(inputfilename) as fi:
    for line_cnt, line in enumerate(fi):
        
        from_user, to_user, strength, meaning = [term.strip() for term in line.split("\t")]

        all_from_users.add(from_user)
        all_to_users.add(to_user)

        if boolTest and line_cnt > 10000:
            break

print "line_cnt=", line_cnt

common_users = all_to_users.intersection(all_from_users)
print "all from users=", len(all_from_users)
print "all to users=", len(all_to_users)
print "common=", len(common_users)
print "users to crawl=", len(all_from_users) + len(all_to_users) - len(common_users)

with open("./list_to_crawl_oldtweets_%s.txt" % (city), "w") as output:
    for each in common_users:
        output.write(each+"\n")

