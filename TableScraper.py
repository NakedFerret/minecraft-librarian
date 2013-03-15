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
        """
        The tds can come in the following ways
        <td> [text] [<a>] [<sup>] </td>

        At least one has to be there and as many as all can be there
        """
        name = ""
        # if there is a sup tag, take it out
        sup = td.find('sup')
        if sup:
            sup.extract()

        # if there is a link, extract the text
        a_list = td.findAll('a')
        link_text = ""
        if a_list:
            for a in a_list:
                link_text += a.string + " "
                a.extract()

        match = re.match("<td>([ \w\(\)]{2,})</td>", str(td))
        if match:
            text = match.group(1)
            if text.find(' ') == 0:
                name = link_text.strip() + " " + text.strip()
            else:
                name = text.strip() + " " + link_text.strip()
        else:
            name = link_text.strip()

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


