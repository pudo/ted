from bs4 import BeautifulSoup as bs
import sys,glob

def get_contracts(filename):

    print "opening..." # big files, takes time

    awards = [] # newdata

    soup = bs(filename, "lxml")

    for doc in soup.find_all("doc"): # each notice is a <doc>
        if doc.natnotice['code'] == "7": # we only want contract award notices (code 7). [1]
            awards.append(doc)
            
    return awards

# test_i = open(sys.argv[1])

for i in glob.glob('*_META_ORG'):
	newdata = get_contracts(open(i))
	#print newdata

	with open(i+"CN.xml", "w") as output:
	   output.write(' '.join(str(doc) for doc in newdata))

# [1] in 2008 and 2009 are <proc> and <natnotice> often the same, except of cases where natnotice is 2 = additional info.
#     In 2010, <proc> holds information on procedure (open, negotiated, etc.), which of course makes more sense.
