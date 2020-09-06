import glob
from bs4 import BeautifulSoup
import codecs 
import sys

boolTest=False

try: 
    param = int(sys.argv[1])
except:
    print "[usage] parse_html.py [param]"
    print "param=0, 1, 2, ... n"


all_files = glob.glob("./crawled_%s/*/*" % (param))

output=codecs.open("profiles_newyork_%s.txt" % (param), "w", "utf-8")

for my_file in all_files:
    print my_file

    with codecs.open(my_file, "r", "utf-8") as fi:
        html_result = fi.read()
        soup = BeautifulSoup(html_result)

        for profile in soup.findAll('tbody',{"class":"stripable_doublerow"}):
            # print profile

        # for profile in soup.findAll('div',{"class":"person_basic"}):
            try:
                name=profile.find('a').text.strip().replace("\t","").replace("\n","")
                screenname=str(profile.find('span', {"class":"person_scrn"}).text).replace("@", "")
                location=profile.find('div', {"class":"person_loc"}).text.strip().replace("\t","").replace("\n","")
                bio=profile.find('div', {"class":"person_bio"}).text.strip().replace("\t","").replace("\n","")

                # print "!!", name, screenname, location, bio

                tweets, following, followers, days, social_authority = [str(number.text.strip()).replace(",","") for number in profile.findAll('td', {"class":"a_r num"})]
                # print tweets, following, followers, days, social_authority
                
                output.write("\t".join([screenname,tweets, following, followers, days, social_authority,name,location,bio])+"\n")
            except:
                print "ERROR"
                continue
            

    if boolTest:
        break


        
