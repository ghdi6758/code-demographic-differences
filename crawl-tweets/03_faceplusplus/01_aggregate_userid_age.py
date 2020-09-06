import json

boolTest = False
cnt_error = 0

# output = open("./screenname_age_race_gender_NY_3.txt", "w")
# output_screenname = open("./to_crawl_tweets_NY_3.txt", "w")
# output_retry = open("./retry_NY_3.txt", "w")
output = open("./screenname_age_race_gender_Texas.txt", "w")
output_screenname = open("./to_crawl_tweets_Texas.txt", "w")
output_retry = open("./retry_Texas.txt", "w")


# with open("facepp-python-sdk-master/crawled_3/crawled_3") as fi:
with open("facepp_texas.txt") as fi:
    for line_cnt, line in enumerate(fi):
        try:
            terms = [term.strip() for term in line.split("\t")]
            screenname = terms[0]

            if terms[1] != "error":
                try: 
                    result_json = json.loads(terms[1])
                    
                    age =  str(result_json['face'][0]['attribute']['age']['value'])
                    age_range =  str(result_json['face'][0]['attribute']['age']['range'])
                    race = result_json['face'][0]['attribute']['race']['value']
                    race_conf = str(result_json['face'][0]['attribute']['race']['confidence'])
                    gender = result_json['face'][0]['attribute']['gender']['value']
                    gender_conf = str(result_json['face'][0]['attribute']['gender']['confidence'])

                    output.write("\t".join([screenname, age, age_range, race, race_conf, gender, gender_conf])+"\n")
                    output_screenname.write(screenname+"\n")
                except:
                    output_retry.write(screenname+"\n")
            else:
                cnt_error += 1
        except:
            print "ERROR", line
            raise

        if boolTest and line_cnt > 5:
            break

print "Total=", line_cnt+1
print "Error=", cnt_error
print "Inferred=", line_cnt+1-cnt_error