from collections import defaultdict

cnt_cfrace = defaultdict(lambda: defaultdict(int))
cnt = defaultdict(lambda: defaultdict(lambda:defaultdict(lambda:defaultdict(int))))
with open("./screenname_cfnameonlyrace_fprace_nbrace_csrace.txt") as fi:
    for line_cnt, line in enumerate(fi):
        city, screen_name, cf_race, fpp_race, nb_race, cs_race = [term.strip() for term in line.split("\t")]
        
        cnt_cfrace[city][cf_race] += 1
        cnt[city][cf_race]["fpp_race"][fpp_race] += 1
        cnt[city][cf_race]["nb_race"][nb_race] += 1
        cnt[city][cf_race]["cs_race"][cs_race] += 1

with open("./result_nameonly.txt", "w") as output:
    for city in ["NY", "texas"]:
        print city
        output.write(city+"\n")

        for cf_race in ["white", "black", "asian", "hispanic"]:
            print "\ncf_race=", cf_race, cnt_cfrace[city][cf_race]
            output.write("\n")
            output.write("\t".join(["cf_race=", cf_race, str(cnt_cfrace[city][cf_race])])+"\n")


            for method in ["fpp_race", "nb_race", "cs_race"]:
                print method
                output.write("\t".join([" ", method])+"\n")

                list_fpp = [" ", " "]
                list_value = [" ", " "]
                list_frac = [" ", " "]
                for fpp_race in sorted(cnt[city][cf_race][method]):
                    frac = "%.4f" % (float(cnt[city][cf_race][method][fpp_race])/float(cnt_cfrace[city][cf_race]))
                    list_fpp.append(fpp_race)
                    list_value.append(str(cnt[city][cf_race][method][fpp_race]))
                    list_frac.append(frac)

                print list_fpp
                print list_value
                print list_frac
                output.write("\t".join(list_fpp)+"\n")
                output.write("\t".join(list_value)+"\n")
                output.write("\t".join(list_frac)+"\n")

