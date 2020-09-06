

boolTest = False
        
city = "texas"
crawled_users = {}
with open("../../data/tweets_%s.txt" % (city)) as fi:
    for line_cnt, line in enumerate(fi):
        try:
            terms = [term.strip() for term in line.split("\t")]
            screen_name = terms[0]
            user_id = terms[1]
            created_at = terms[2]
            tweet_id = terms[3]
            text = terms[4]
            coordinates = terms[5]
        except:
            print "ERROR", line
            raise

        crawled_users[screen_name] = 1

        if line_cnt % 500000 == 0:
            print "Progress line counts = %d out of %s" % (line_cnt, "53000000")

        if boolTest and line_cnt > 100:
            break


missing_users = {}
with open("./to_crawl_tweets_Texas.txt") as fi, open("./retry_crawl_tweets_texas.txt", "w") as output:
    for line_cnt, line in enumerate(fi):
        screen_name = line.strip()

        if screen_name not in crawled_users:
            output.write(line)
            missing_users[screen_name] = 1

        if boolTest and line_cnt > 100:
            break

print "number of crawled users=", len(crawled_users)
print "number of missing users=", len(missing_users)

