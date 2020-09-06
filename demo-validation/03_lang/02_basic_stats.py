from collections import defaultdict
import operator

boolTest = False

# city = "NY"
city = "texas"

cnt_langs = defaultdict(int)
cnt_users = defaultdict(int)
with open("./screenname_tweet_language_%s.txt" % (city)) as fi, open("./simple_screenname_tweet_language_%s.txt" % (city), "w") as output:
    for line_cnt, line in enumerate(fi):
        screen_name, langs = [term.strip() for term in line.split("\t")]

        new_langs = []
        for str_lang in langs.split("||"):
            try:
                lang, prob = [term.strip() for term in str_lang.split(":")]
                prob = float(prob)
                str_prob = "%.4f" % (float(prob))
                new_string = ":".join([lang, str_prob])
            except:
                # print "ERROR", line
                lang = "NA"
                new_string = "NA"
            new_langs.append(new_string)
            
            # print lang
            cnt_langs[lang] += 1

        dom_lang = new_langs[0].split(":")[0]
        str_new_langs = "||".join(new_langs)
        output.write("\t".join([screen_name, str_new_langs, dom_lang])+"\n")


        if len(langs.split("||")) > 1:
            cnt_users["morethantwo"] += 1
        else:
            cnt_users["one"] += 1
    
        if lang == "NA":
            cnt_users["NA"] += 1
        if boolTest and line_cnt > 100:
            break
            

print "Number of languages = ", len(cnt_langs)
print "Top 10 languages and # users: "
rank = 1
for mytuple in sorted(cnt_langs.items(), key=operator.itemgetter(1), reverse=True)[0:10]:
    print "\t[%d]" % (rank), mytuple[0], mytuple[1]
    rank += 1


print "Users with no language detected = ", cnt_users["NA"]
print "Users with one languages  = ", cnt_users["one"]
print "Users with more than two languages  = ", cnt_users["morethantwo"]

