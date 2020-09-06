import shutil
import requests
from collections import defaultdict
import time
import sys

# param = sys.argv[1]

boolTest = False

cnt_still_online = 0

myparam = int(sys.argv[1])

with open("./5th_network_random_screenname_faceplusplus_name_imageurl.txt") as fi, open("./5th_network_random_error.txt", "a") as output_error, open("./5th_network_stillonline_random_screenname_faceplusplus_name_imageurl_%s.txt" % (myparam), "a") as output:

    for line_cnt, line in enumerate(fi):
        # if line_cnt <= 796:
        #     continue
        if line_cnt % 5 != myparam:
            continue
        # print line_cnt
        # continue
        city, screen_name, age_group, race, gender, name, profile_image_url, sample_type = [term.strip() for term in line.split("\t")]

        print line_cnt, profile_image_url
        r = requests.get(profile_image_url, stream=True)
        image_name = profile_image_url.split("/")[-1]
        path = "./images_5/%s_%s" % (screen_name, image_name)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            cnt_still_online += 1
            output.write(line)
        else:
            print "\t", "ERROR", screen_name
            output_error.write(screen_name+"\n")

        if boolTest and line_cnt > 2:
            break

        time.sleep(1)


print "cnt_still_online=", cnt_still_online


