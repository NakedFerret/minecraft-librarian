#! /usr/bin/env python2

from TableScraper import WikiTableScraper
import difflib
import sys
import os
import pickle

CACHE_FILE_NAME = "data_values.cache"

pathToFile = os.path.join(os.getcwd(), CACHE_FILE_NAME)
if os.path.isfile(pathToFile):
    # we have a cache
    ids = pickle.load( open( CACHE_FILE_NAME, "rb" ) )
else:
    scraper = WikiTableScraper()
    ids = scraper.scrapeTables()
    pickle.dump( ids, open( CACHE_FILE_NAME, "wb" ) )

for i in ids.iteritems():
    print i[1].ljust(4), i[0]


