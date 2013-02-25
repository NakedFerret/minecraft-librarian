#! /usr/bin/env python2

import urllib
from BeautifulSoup import BeautifulSoup
from collections import OrderedDict

BLOCKIDSTITLE = 'Block IDs'
ITEMSIDSTITLE = 'Item IDs'
WIKIURL = 'http://www.minecraftwiki.net/wiki/Data_values'

class WikiTableScraper(object):
    
    def __init__(self):
        self.dataValues = OrderedDict()
                
    def populateData(self,table):

        rows = table.findAll('tr')
        print rows
        for tr in rows[1:]:
            dec = -1
            name = None
            list = tr.contents

            
            #[2] and [4] contain dec and block type,respectively
            if(list[2].span == None):
                dec = list[2].string.strip()
            else:
                dec = list[2].span.string.strip()

            sup = list[4].find('sup')`
            if sup != None:
                sup.extract()
                
            linkText = ''
            ays = list[4].findAll('a')
            for ay in ays:
                linkText = linkText.strip()
                linkText = linkText + ' ' +  ay.string
                ay.extract()
                
            text = str(list[4])
            text  = text.lstrip("<td>")
            text = text.split("<")[0]
            text = text.strip()
        
            if len(text) > 0:
                text = text + " " + linkText.strip()
                name = text
            else:
                name = linkText

            self.dataValues[str(dec).strip()] = name.strip()


    def mineTablesAfterTitle(self,title,numOfTables=1):
        
        htwos = self.soup.findAll('h3')
        for h2 in htwos:
            if h2.renderContents().find(title) != -1:
                H2 = h2
                
        table = H2.findNext('table')
        self.populateData(table)

        for i in range(numOfTables-1):
            table = table.findNext('table')
            self.populateData(table)


    def scrapeTables(self):
        f = urllib.urlopen(WIKIURL)
        source = f.read()
        f.close()
        self.soup = BeautifulSoup(source)
        self.mineTablesAfterTitle(BLOCKIDSTITLE,3)
        self.mineTablesAfterTitle(ITEMSIDSTITLE,4)
        return self.dataValues

    def getValues(self):
        return self.dataValues

    def reset(self):
        self.dataValues.clear()

