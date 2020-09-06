import shutil
import requests
from collections import defaultdict
import time

boolTest = False

cities = ["NY", "texas"]
# cities = ["NY"]
cnt_still_online = defaultdict(int)

for city in cities:

    with open("./random_screenname_faceplusplus_name_imageurl_bio_%s.txt" % (city)) as fi, open("./error_%s.txt" % (city), "w") as output_error, open("./stillonline_random_screenname_faceplusplus_name_imageurl_bio_%s.txt" % (city), "w") as output:
        for line_cnt, line in enumerate(fi):
            screen_name, age_group, race, gender, name, profile_image_url, description = [term.strip() for term in line.split("\t")]

            print line_cnt, profile_image_url
            r = requests.get(profile_image_url, stream=True)
            image_name = profile_image_url.split("/")[-1]
            path = "./images/%s/%s_%s" % (city, screen_name, image_name)
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                cnt_still_online[city] += 1
                output.write(line)
            else:
                print "\t", "ERROR", screen_name
                output_error.write(screen_name+"\n")

            if boolTest and line_cnt > 2:
                break

            time.sleep(1)

for city in cnt_still_online:
    print city, "cnt_still_online=", cnt_still_online[city]


