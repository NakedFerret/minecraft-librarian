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
        The tds can come in one of 4 ways
        1. <td> text </td>
        2. <td> <a> link_text </a> </td>
        3. <td> text <a> link_text </a> </td>
        4. <td> <a> link_text </a> text </td>

        The information to be extracted should be in the form of
        1. text
        2. link_text
        3. text + link_text
        4. link_text + text
        """
        name = ""
        log_string = ""
        log_string +=  "-----\n"
        log_string += str(td) + "\n"
        # if there is a sup tag, take it out
        sup = td.find('sup')
        if sup:
            log_string += str(sup) + "\n"
            sup.extract()

        # if there is a link, extract the text
        a = td.find('a')
        link_text = ""
        if a:
            log_string += str(a) + "\n"
            link_text = a.string
            a.extract()
            
        
        log_string += str(td) + "\n"
        if td.string and td.string.strip():
            if td.string.find(' ') == 0:
                log_string += "space at start \n"
                name = link_text + td.string
            else:
                log_string += "space at end \n"
                name = td.string + link_text
        else:
            log_string += "empty string \n"
            name = link_text

        log_string += name + "\n"
        log_string += "-----\n\n\n"
        if re.match("<td>([ a-zA-Z]+)</td>",str(td)):
            print log_string
            
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


