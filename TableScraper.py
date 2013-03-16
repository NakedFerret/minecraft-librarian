#! /usr/bin/env python2

import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re

WIKIURL = 'http://www.minecraftwiki.net/wiki/Data_values'
BLOCK_TYPE_HEADER = "<th>Block type</th>"
ITEM_HEADER = "<th>Item</th>"

class WikiTableScraper(object):
    """Finds all the tables in minecraft wiki and extracts the id and the name"""
    
    def __init__(self):
        self.dataValues = dict()

    def extract_decimal(self, td):
        """Returns the id of the minecraft object from a <td>. 
        Assumes the correct <td> was given"""
        dec = td
        if td.span:
            dec = td.span.string
        else:
            dec = td.string
            
        return dec

    def extract_name(self, td):
        """Returns the name of the minecraft object from a <td>.
        Assumes the correct <td> was given"""
        name = ""
        # if there are any sup tags, take them out
        for sup in td.findAll('sup'):
            sup.extract()

        # if there are any a tags, extract the text,
        # join the text, and take out the tags
        link_text = ""
        for a in td.findAll('a'):
            link_text += a.string + " "
            a.extract()

        # time to put the name of the item together
        match = re.match("<td>([ \w\(\)]{2,})</td>", str(td))
        if match:
            text = match.group(1)
            if text[0] == ' ':
                name = link_text.strip() + " " + text.strip()
            else:
                name = text.strip() + " " + link_text.strip()
        else:
            name = link_text.strip()

        return name
        
    def getRelevantTables(self, source_html):
        """Returns the tables that contain the minecraft object info"""
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
        """Returns a dict of minecraft objects. 
        The id is the key and the name is the value"""
        f = urllib.urlopen(WIKIURL)
        source_html = f.read()
        f.close()
        
        tables = self.getRelevantTables(source_html)

        for t in tables:
            rows = t.findAll('tr')
            for tr in rows[1:]:
                non_empty_tds = [x for x in tr.contents if str(x).strip()]

                # column 1 (0 based) contains the decimal numbers
                dec = self.extract_decimal(non_empty_tds[1])
                # column 3 (0 based) contains the name of the object
                name = self.extract_name(non_empty_tds[3])
                self.dataValues[dec] = name

        return self.dataValues


