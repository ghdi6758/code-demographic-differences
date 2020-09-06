
boolTest = False

basic_dropbox_url = "https://dl.dropboxusercontent.com/u/2166050/CF_race_detection"

with open("./crowdflower_2nd_cfonlyus_all_screenname_faceplusplus_name_imageurl.tsv", "r") as fi, open("./crowdflower_2nd_cfonlyus_all_screenname_faceplusplus_name_dropboximageurl.tsv", "w") as output:

    output.write("\t".join(["city", "screen_name", "age_group", "race", "gender", "name", "image_url", "sample_type"])+"\n")

    next(fi)
    
    for line_cnt, line in enumerate(fi):
        city, screen_name, age_group, race, gender, name, profile_image_url, linktype = [term.strip() for term in line.split("\t")]

        image_name = profile_image_url.split("/")[-1]

        filename = "%s_%s" % (screen_name, image_name)

        dropbox_url = "%s/%s" % (basic_dropbox_url, filename)
        
        output.write("\t".join([city, screen_name, age_group, race, gender, name, dropbox_url, linktype])+'\n')

        if boolTest and line_cnt > 10:
            print screen_name, profile_image_url
            print dropbox_url
            break