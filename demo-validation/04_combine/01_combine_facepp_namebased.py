boolTest = False


# city = "NY"
city = "texas"

user2tweetLang = {}
user2tweetdomLang = {}
with open("../03_lang/simple_screenname_tweet_language_%s.txt" % (city)) as fi:
    for line_cnt, line in enumerate(fi):
        screen_name, langs, dom_lang = [term.strip() for term in line.split("\t")]
        user2tweetLang[screen_name] = langs
        user2tweetdomLang[screen_name] = dom_lang

user2nbRace = {}
with open("../02_race/name2ethnicity/names/names/screenname2name2race_facepp_bios_%s.txt" % (city)) as fi:
    for line_cnt, line in enumerate(fi):
        screen_name, name, race = [term.strip() for term in line.split("\t")]
        user2nbRace[screen_name] = race

user2nbGender = {}
with open("../01_gender/screenname_nb_gender_%s.txt" % (city)) as fi:
    for line_cnt, line in enumerate(fi):
        screen_name, gender = [term.strip() for term in line.split("\t")]
        if gender != "NA":
            gender = gender.title()
        user2nbGender[screen_name] = gender

with open("../../analysis/05_network/screenname_agegroup_race_gender_bios_%s.txt" % (city)) as fi, open("./screenname_fpagegroup_fpgender_nbgender_fprace_nbrace_userlang_tweetlang_tweetdomlang_%s.txt" % (city), "w") as output:
    for line_cnt, line in enumerate(fi):
        screen_name, age_group, race, gender, userid, name, location, lang, days_since_join, statuses_count, followers_count, friends_count, listed_count, favourites_count, profile_image_url, description, days_since_active = [term.strip() for term in line.split("\t")]

        nb_race = "NA"
        nb_gender = "NA"
        tw_lang = "NA"
        tw_dom_lang = "NA"

        if screen_name in user2nbRace:
            nb_race = user2nbRace[screen_name]
        if screen_name in user2nbGender:
            nb_gender = user2nbGender[screen_name]
        if screen_name in user2tweetLang:
            tw_lang = user2tweetLang[screen_name]
            tw_dom_lang = user2tweetdomLang[screen_name]

    
        output.write("\t".join([screen_name, age_group,gender, nb_gender, race, nb_race, lang, tw_lang, tw_dom_lang])+"\n")

        if boolTest and line_cnt > 10:
            break



