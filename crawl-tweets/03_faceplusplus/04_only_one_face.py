import json

boolTest = False

city = "NY"
# city = "texas"
with open("facepp_%s.txt" % (city)) as fi, open("./multiple_faces_%s.txt" % (city), "w") as output:
    cnt_error = 0
    cnt_parse_error = 0
    cnt_oneface = 0
    cnt_multipleface = 0
    users_multiplefaces = {}
    for line_cnt, line in enumerate(fi):
        try:
            terms = [term.strip() for term in line.split("\t")]
            screenname = terms[0]

            if terms[1] != "error":
                result_json = json.loads(terms[1])
                num_faces = len(result_json['face'])
                
                if num_faces == 1:
                    cnt_oneface += 1
                elif num_faces > 1:
                    cnt_multipleface += 1
                    users_multiplefaces[screenname] = 1

                # age =  str(result_json['face'][0]['attribute']['age']['value'])
                # age_range =  str(result_json['face'][0]['attribute']['age']['range'])
                # race = result_json['face'][0]['attribute']['race']['value']
                # race_conf = str(result_json['face'][0]['attribute']['race']['confidence'])
                # gender = result_json['face'][0]['attribute']['gender']['value']
                # gender_conf = str(result_json['face'][0]['attribute']['gender']['confidence'])

                
            else:
                cnt_error += 1
        except:
            # print "ERROR", line
            cnt_parse_error += 1
            continue

        if boolTest and line_cnt > 50:
            break

    print "Total=", line_cnt+1
    print "Error=", cnt_error
    print "Parsing error=", cnt_parse_error
    print "Inferred=", line_cnt+1-cnt_error
    print "One face =", cnt_oneface
    print "Multiple faces =", cnt_multipleface
    print cnt_oneface+cnt_multipleface

    for screenname in sorted(users_multiplefaces):
        output.write(screenname+"\n")

# Texas
# Total= 254325
# Error= 110444
# Inferred= 143881
# One face = 122084
# Multiple faces = 21797
# 143881

# NY
# Total= 728460
# Error= 351005
# Parsing error= 46
# Inferred= 377455
# One face = 328630
# Multiple faces = 48779
# 377409