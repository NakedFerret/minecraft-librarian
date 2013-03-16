#! /usr/bin/env python2

from TableScraper import WikiTableScraper

scraper = WikiTableScraper()
ids = scraper.scrapeTables()

for k,v in sorted(ids.iteritems()):
    print k.ljust(4), v

