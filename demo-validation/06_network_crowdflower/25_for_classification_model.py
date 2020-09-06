
with open("./result_all/usonly_CF_aggregated_all.txt") as fi, open("./result_all/usonly_CF_aggregated_simple.txt", "w") as output:
    
    output.write("\t".join(["screen_name", "city", "cfrace", "cfrace_agreement", "cfrace_selfreported_rating"])+"\n")

    next(fi)
    for line_cnt, line in enumerate(fi):
        screen_name, city, sample_type, fpp_race, cfrace_first_choice, cfrace_first_choice_conf, cfrace_first_rating, cfrace_first_rating_var, cfrace_second_choice, cfrace_second_choice_conf, cfrace_second_rating, cfrace_second_rating_var, name, image_url = [term.strip() for term in line.split("\t")]

        output.write("\t".join([screen_name, city, cfrace_first_choice, cfrace_first_choice_conf, cfrace_first_rating])+"\n")