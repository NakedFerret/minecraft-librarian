#! /usr/bin/env python2

import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re

WIKIURL = 'http://www.minecraftwiki.net/wiki/Data_values'
BLOCK_TYPE_HEADER = "<th>Block type</th>"
ITEM_HEADER = "<th>Item</th>"

class WikiTableScraper(object):
    
    def __init__(self):
        self.dataValues = dict()

    def extract_decimal(self, td):
        dec = td
        if td.span:
            dec = td.span.string
        else:
            dec = td.string
            
        return dec

    def extract_name(self, td):
        """
        Extracts the name of the minecraft object from a <td> 
        """
        for sup in td.findAll('sup'):
            sup.extract()
        return td.getText()

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

                dec = self.extract_decimal(non_empty_tds[1])
                name = self.extract_name(non_empty_tds[3])
                self.dataValues[name] = dec

        return self.dataValues


