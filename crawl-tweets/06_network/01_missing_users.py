
boolTest = False

crawled_users = {}
with open("../../analysis/05_network/sg_first_texas.txt") as fi:

    for line_cnt, line in enumerate(fi):
        # print line
        terms = [term.strip() for term in line.split("\t")]
        screen_name = terms[0]
        link_type = terms[1]
        crawled_users[screen_name] = 1

        if boolTest and line_cnt > 100:
            break

with open("../../analysis/05_network/sg_third_texas.txt") as fi:

    for line_cnt, line in enumerate(fi):
        # print line
        terms = [term.strip() for term in line.split("\t")]
        screen_name = terms[0]
        link_type = terms[1]
        crawled_users[screen_name] = 1

        if boolTest and line_cnt > 100:
            break


missing_users = {}
with open("./to_crawl_tweets_Texas.txt") as fi, open("./retry_crawl_network_texas.txt", "w") as output:
    for line_cnt, line in enumerate(fi):
        screen_name = line.strip()

        if screen_name not in crawled_users:
            output.write(line)
            missing_users[screen_name] = 1

        if boolTest and line_cnt > 100:
            break

print "number of crawled users=", len(crawled_users)
print "number of missing users=", len(missing_users)