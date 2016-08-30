import sys
import sqlite3
from urllib2 import HTTPError
import requests
import csv
from bs4 import BeautifulSoup
import os
import re

# Output a big file (csv) or a database where documents
# are neatly separated, and the following information is available:
# 1) URL of the document, 2) title of the document.

# This is a modified version of retrieve_data.py, written by Bharat Shetty
# Barkur, itself a modification of Veesa Norman's retrieve_pages.py.

drows = []
status_code_freqs = {}
home_directory = os.path.expanduser('~')

#A small ignore list for sites that don't need indexing.
ignore=["twitter", "google", "duckduckgo", "bing", "yahoo", "facebook"]


def mk_ignore():
    '''Make ignore list'''
    s = []
    for i in ignore:
        s.append("www."+i)
        s.append("://"+i)
    return s


def get_firefox_history_db(in_dir):
    """Given a home directory it will search it for the places.sqlite file
    in Mozilla Firefox and return the path. This should work on Windows/
    Linux"""

    firefox_directory = in_dir + "/.mozilla/firefox"
    for files in os.walk(firefox_directory):
        # Build the filename
        if re.search('places.sqlite', str(os.path.join(files))):
            history_db = str(os.path.realpath(files[0]) + '/places.sqlite')
            # print history_db
            return history_db

    return None


def write_urls_to_process(db_urls, num_pages, ignore_list):
  '''Select and write urls that will be processed, so that user can check the list\
   before proceeding.'''

  urls_to_process = []
  i = 0
  urlsfile = open("./local-history/urls.txt", 'w')
  for url_str in db_urls:
    url = url_str[1]
    if i < num_pages:
      if not any( i in url for i in ignore_list):
        urlsfile.write(url+"\n")
        urls_to_process.append(url)
        i += 1
    else:
      break
  urlsfile.close()
  return urls_to_process


def extract_from_url(url):
    '''From history info, extract url, title and body of page,
    cleaned with BeautifulSoup'''
    if url.startswith('http'):
        print url
    else:
        return

    try:
        # TODO: Is there any issue in using redirects?
        req = requests.get(url, allow_redirects=True)
        req.encoding = 'utf-8'

        # Gather stats about status codes
        if str(req.status_code) not in status_code_freqs:
            status_code_freqs[str(req.status_code)] = 1
        else:
            status_code_freqs[str(req.status_code)] += 1

        if req.status_code is not 200:
            print str(req.url) + ' has a status code of: ' \
                + str(req.status_code) + ' omitted from database.'

        bs_obj = BeautifulSoup(req.text,"lxml")

        if hasattr(bs_obj.title, 'string') \
                & (req.status_code == requests.codes.ok):
            try:
                title = unicode(bs_obj.title.string)
                if url.startswith('http'):
                    if title is None:
                        title = u'Untitled'
                    checks = ['script', 'style', 'meta', '<!--']
                    for chk in bs_obj.find_all(checks):
                        chk.extract()
                    body = bs_obj.get_text()
                    pattern = re.compile('(^[\s]+)|([\s]+$)', re.MULTILINE)
                    body_str=re.sub(pattern," ",body)
                    drows.append([title, url, body_str])

                if title is None:
                    title = u'Untitled'
            except HTTPError as error:
                title = u'Untitled'
            except None:
                title = u'Untitled'
    # can't connect to the host
    except:
        error = sys.exc_info()[0]
        print "Error - %s" % error


def runScript(num_pages, outfile):
    ignore_list = mk_ignore()
    # [TODO] Set the firefox path here via config file
    HISTORY_DB = get_firefox_history_db(home_directory)
    if HISTORY_DB is None:
        print 'Error - Cannot find the Firefox history database.\n\nExiting...'
        sys.exit(1)

    # connect to the sqlite history database
    db = sqlite3.connect(HISTORY_DB)
    cursor = db.cursor()

    # get the list of all visited places via firefox browser
    cursor.execute("SELECT * FROM 'moz_places' ORDER BY visit_count DESC")
    rows = cursor.fetchall()

    urls_to_process=write_urls_to_process(rows, num_pages, ignore_list)

    check = raw_input("\nAll URLS to be processed have been written in \
./local-history/urls.txt. You can check this file before \
proceeding further.\nContinue? (y/n)\n")
    while check not in ["y", "n"]:
        check = raw_input("Please press y or n.")

    if check == "n":
        sys.exit(1)

    with open(outfile, 'w') as urlfile:
      for url in urls_to_process:
        extract_from_url(url)
      for s in drows:
          title = unicode(s[0]).encode("ascii", 'ignore')
          url = unicode(s[1]).encode("ascii", 'ignore')
          body = unicode(s[2]).encode("ascii", 'ignore')
          print title, url
          urlfile.write("<doc url=\""+url+"\" title=\""+title+"\">\n")
          urlfile.write(body+"\n")
          urlfile.write("</doc>\n")
    urlfile.close()

    db.close()

    # Output status code stats
    print "\n---\nStatus code stats:\n---\n"
    for k, v in status_code_freqs.items():
        print k, v

if __name__ == '__main__':
    runScript(sys.argv[1], sys.argv[2])
