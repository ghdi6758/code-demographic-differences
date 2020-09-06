import glob

list_tocrawl=[]

for i in range(7,72):
    list_tocrawl.append(i)

for i in range(81,144):
    list_tocrawl.append(i)

for i in range(158,216):
    list_tocrawl.append(i)

for i in range(238,288):
    list_tocrawl.append(i)

for i in range(320,360):
    list_tocrawl.append(i)

for i in range(405,432):
    list_tocrawl.append(i)

for i in range(492,504):
    list_tocrawl.append(i)


### from backup
files = glob.glob("./backup for retry/*")

for myfile in files:
    with open(myfile) as fi:
        for line_cnt, line in enumerate(fi):
            # print line
            numpage, numfollower = [term.strip() for term in line.split("\t")]
            numfollower = int(numfollower)
            list_tocrawl.append(numfollower)

print sorted(list_tocrawl)

with open("./to_crawl.txt", "w") as output:
    for each in sorted(list_tocrawl):
        output.write(str(each)+"\n")

