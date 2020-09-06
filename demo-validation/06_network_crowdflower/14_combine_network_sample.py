import random

boolTest = False

myparam = "1st_random"
# myparam = "1st_linktype"

# if myparam == "1st_random":
#     linktype = "fr_network"
# elif myparam == "1st_linktype":
#     linktype = "fr_network_linktype"

with open("cfonlyus_%s_network_random_screenname_faceplusplus_name_imageurl.txt" % (myparam), "w") as output:
    cities = ["NY", "texas"]

    
    for city in cities:
        cnt_multi = 0
        cnt_other = 0
        cnt_yes = 0
        multiplefaces = {}
        with open("../../crawl-tweets/03_faceplusplus/multiple_faces_%s.txt" % (city)) as fi:
            for line_cnt, line in enumerate(fi):
                screen_name = line.strip()
                multiplefaces[screen_name] = 1
        
        
        inputfilename = "cfonlyus_%s_random_inferred_users_follower_network_%s.txt" % (myparam, city)

        myusers = {}
        with open(inputfilename) as fi:
            for line_cnt, line in enumerate(fi):

                from_user, from_race, to_user, to_race, linktype = [term.strip() for term in line.split("\t")]

                myusers[from_user] = 1
                myusers[to_user] = 1

        print city, len(myusers)

        allusers = {}
        with open("../05_crowdflower/screenname_faceplusplus_name_imageurl_bio_%s.txt" % (city)) as fi:
            for line_cnt, line in enumerate(fi):
                screen_name, age_group, race, gender, name, profile_image_url, description = [term.strip() for term in line.split("\t")]
                name = name.replace(",", " ")
                allusers[screen_name] = 1
                if screen_name in myusers:
                    if screen_name in multiplefaces:
                        cnt_multi += 1
                        continue
                    else:                 
                        cnt_yes += 1
                        output.write("\t".join([city, screen_name, age_group, race, gender, name, profile_image_url, linktype])+"\n")
                else:
                    cnt_other += 1

        print "cnt_multi=", cnt_multi
        print "cnt_yes=", cnt_yes
        print "cnt_other=", cnt_other 


        cnt_user = 0
        cnt_no = 0
        for user in myusers:
            if user in allusers:
                cnt_user += 1
            else:
                cnt_no += 1

        print cnt_user, cnt_no