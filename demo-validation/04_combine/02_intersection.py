from collections import defaultdict
boolTest = False
city = "NY"


cnt_asian = 0
cnt_name_asian = 0
cnt_agree = 0
cnt_race = defaultdict(int)

asian_lang = ["CHI", "JAP", "KOR", "VIE"]
with open("./screenname_fpagegroup_fpgender_nbgender_fprace_nbrace_userlang_tweetlang_tweetdomlang_%s.txt" % (city)) as fi:
    for line_cnt, line in enumerate(fi):
        screen_name, age_group, gender, nb_gender, race, nb_race, lang, tw_lang, tw_dom_lang = [term.strip() for term in line.split("\t")]
        # print race, nb_race

        if race == "Asian":
            cnt_asian += 1
            if nb_race in asian_lang:
                cnt_agree += 1

        if nb_race in asian_lang:
            cnt_name_asian += 1

            cnt_race[race] += 1


        if boolTest and line_cnt > 10:
            break

print cnt_asian
print cnt_name_asian

print cnt_asian + cnt_name_asian - cnt_agree
print cnt_asian - cnt_agree
print cnt_name_asian - cnt_agree
print cnt_agree


print cnt_race