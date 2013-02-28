#! /usr/bin/env python2

import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer

WIKIURL = 'http://www.minecraftwiki.net/wiki/Data_values'
BLOCK_TYPE_HEADER = "<th>Block type</th>"
ITEM_HEADER = "<th>Item</th>"

class WikiTableScraper(object):
    
    def __init__(self):
        self.dataValues = dict()

    @staticmethod
    def extract_decimal(td):
        dec = td
        if td.span:
            dec = td.span.string
        else:
            dec = td.string
            
        return dec

    @staticmethod
    def extract_name(td):
        name = td
        if td.find('sup'):
            td.find('sup').extract()

        if td.find('a'):
            name = td.find('a').string
        else:
            name = td.string

        return name

    def getRelevantTables(self, source_html):
        tables = list()
        soup =  BeautifulSoup(source_html, parseOnlyThese=SoupStrainer('table'))

        for t in soup:
            if BLOCK_TYPE_HEADER in t.first().renderContents():
                tables.append(t)
            if ITEM_HEADER in t.first().renderContents():
                tables.append(t)

        return tables

    def getValues(self):
        return self.dataValues

    def reset(self):
        self.dataValues.clear()

    def scrapeTables(self):
        # f = urllib.urlopen(WIKIURL)
        f = open('data_values.html')
        source_html = f.read()
        f.close()
        
        tables = self.getRelevantTables(source_html)

        for t in tables:
            rows = t.findAll('tr')
            for tr in rows[1:]:
                non_empty_tds = [x for x in tr.contents if str(x).strip()]

                dec = WikiTableScraper.extract_decimal(non_empty_tds[1])
                name = WikiTableScraper.extract_name(non_empty_tds[3])
                self.dataValues[name] = dec

        return self.dataValues


