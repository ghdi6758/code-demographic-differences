import sys
import codecs
from langdetect import detect_langs
import logging

reload(sys)
sys.setdefaultencoding("utf-8")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')
#                     filename="opgg.log",
#                     filemode="a")
logger = logging.getLogger(__name__)

boolTest = False

city = "texas"

target_users = {}
with open("../../analysis/05_network/screenname_agegroup_race_gender_bios_%s.txt" % (city)) as fi:
    for line_cnt, line in enumerate(fi):
        screen_name, age_group, race, gender, userid, name, location, lang, days_since_join, statuses_count, followers_count, friends_count, listed_count, favourites_count, profile_image_url, description, days_since_active = [term.strip() for term in line.split("\t")]
        target_users[screen_name] = 1
print "Number of target users in NY=", len(target_users)

with codecs.open("../../data/tweets_%s.txt" % (city), "r", "utf-8") as fi, open("./screenname_tweet_language_%s.txt" % (city), "w") as output:

    last_screen_name = ""
    mytweets = []
    for line_cnt, line in enumerate(fi):
        
        try:
            screen_name, user_id, created_at, tweet_id, text, coordinates = [term.strip() for term in line.split("\t")]
        except:
            logger.exception("")
            continue

        if line_cnt == 0:
            last_screen_name = screen_name

        if line_cnt > 0 and last_screen_name != screen_name:
            try:
                mytweets = " ".join(mytweets)
                mylangs = detect_langs(mytweets)
                logger.debug("%s, %s, %s" % (screen_name, mylangs, mytweets))
                str_mylangs = "||".join([str(term) for term in mylangs])
            except:
                logger.exception("")
                str_mylangs = "NA"

            output.write("\t".join([screen_name, str_mylangs])+"\n")
            last_screen_name = screen_name
            mytweets = []

        logger.debug("%s" % (text))
        newtext = []
        for term in text.split():
            logger.debug("%s" % (term))
            if "@" in term or "http" in term or "rt" in term or "RT" in term:
                continue
            newtext.append(term)
        logger.debug("%s" % (" ".join(newtext)))

        mytweets.append(" ".join(newtext))

        if boolTest == True and line_cnt > 10:
            break

        if line_cnt % 5000 == 0:
            logger.info("Progress line counts = %d" % (line_cnt))

    try:
        mytweets = " ".join(mytweets)
        mylangs = detect_langs(mytweets)
        logger.debug("%s, %s" % (screen_name, mylangs))
        str_mylangs = "||".join([str(term) for term in mylangs])
    except:
        logger.exception("")
        str_mylangs = "NA"

    output.write("\t".join([screen_name, str_mylangs])+"\n")

print "DONE"
