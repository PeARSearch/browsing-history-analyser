#A script to help you search your own history

import os
import sys
import retrieve_raw_data,runDistSemWeighted,mkWordClouds,mkLocalProfile

def isInt(n):
    '''Check that a string is an int'''
    try:
        int(n)
        return True
    except ValueError:
        return False

num_pages=50
if not os.path.isdir("./local-history"):
  os.mkdir("./local-history/")

user_in=raw_input(
"\nHi, welcome to the PeARS Firefox history analyser.\n\
This program allows you to index the pages in your Web history\n\
to subsequently search them with the PeARS search engine.\n\n\
IMPORTANT: Please note that the analyser has to retrieve every page\n\
it indexes from the Web, so if you have concerns about processing time,\n\
bandwidth, or making too many calls to a particular domain, please\n\
use the program carefully. By default, the program is set to only\n\
index the 50 pages you visited most.\n\nWhat would you like to do?\n\
    a) yeah, index those 50 pages (y)\n\
    b) get me out of here (x)\n\
    c) index this number of pages (enter a number)\n")

user_in=user_in.strip()

while user_in not in ["y","x"] and not isInt(user_in):
  user_in=raw_input("Please press 'y', 'x', or enter a number.")

if isInt(user_in):
	num_pages=int(user_in)
if user_in=="x":
	sys.exit()

retrieve_raw_data.runScript(num_pages,"./local-history/documents.txt")
#runDistSemWeighted.runScript("./local-history/documents.txt","./local-history/urls.dists.txt")
#mkWordClouds.runScript()
#mkLocalProfile.runScript()
