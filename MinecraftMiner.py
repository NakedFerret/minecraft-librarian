#! /usr/bin/env python2

import os
import sys
from TableScraper import WikiTableScraper
from collections import OrderedDict

WORKDIRPATH = '.minecraft-miner'
NAMEOFFILE = 'List-Of-Ids'

class Controller(object):

    def fillFromFile(self):
        f = open(NAMEOFFILE,"r")
        line = f.readline()
        dec = -1
        while len(line) > 0:
            if dec == -1:
                dec = line.strip()
            else:
                self.ids[dec] = line.strip()
                dec = -1
            line = f.readline()
        f.close()
                
    def saveToFile(self):
        f = open(NAMEOFFILE,'w')
        fileContents = ""
        for k in self.ids:
            fileContents += "{0}\n{1}\n".format(k,self.ids[k])
        f.write(fileContents)
        f.close()

    def showHelp(self):
        pass

    def fillData(self,forceUpdate = False):
        self.ids.clear()
        #Check to see if the file is there
        pathToFile = os.path.join(os.getcwd(), NAMEOFFILE)
        if not forceUpdate and os.path.isfile(pathToFile):
            self.fillFromFile()
        else:
            scraper = WikiTableScraper()
            self.ids = scraper.scrapeTables()            
            self.saveToFile()

    def matchWholeWords(self,words):
        #Match whole words, Ignore uppercase
        wordKeyList = []
        for arg in words:
            for k in self.ids:
                for word in self.ids[k].split():
                    if(word.lower() == arg.lower()):
                        wordKeyList.append(k)

        singleMatches = {}
        for k in wordKeyList:
            singleMatches[k] = singleMatches.get(k,0) + 1

        result = []
        for m in singleMatches:
            if(singleMatches[m] >= len(words)):
                result.append(m)

        return result
                
    def findClosestMatch(self,words):
        matchedWords = self.matchWholeWords(words)
        
        #Make a new dic with [dec : length of all words combined]
        lenOfMatchedWords = OrderedDict()
        for d in matchedWords:
            length = 0
            for w in self.ids[d].split():
                length = length + len(w)
            lenOfMatchedWords[d] = length
       
        #Length of all the args combined
        lenOfArgs = 0
        for w in words:
            lenOfArgs += len(w)
       
        #Now find the best match i.e. one with closest length
        bestMatch = matchedWords[0]
        for i in range(len(lenOfMatchedWords)):
            bestDiff = lenOfArgs - lenOfMatchedWords[bestMatch]
            newDiff = lenOfArgs - lenOfMatchedWords[matchedWords[i]]
            if(abs(newDiff) < abs(bestDiff)):
                bestMatch = matchedWords[i]

        return [bestMatch]
    
    def contains(self,words):
        wordKeyList = []
        #Compare everyword with everyword in every
        #Dic entry
        for arg in words:
            for k in self.ids:
                for word in self.ids[k].split():
                    if(arg.lower() in word.lower()):
                        wordKeyList.append(k)

        return wordKeyList

    def handleArgs(self):
        args = sys.argv
        if args[1] == '-h' or args[1] == '--help':
            self.showHelp()
            return 0
        if args[1][:1] == "-":
            options = args[1][1:]
            f = self.matchWholeWords
            
            if 'w' in options:
                f = self.matchWholeWords
            elif 'm' in options:
                f = self.findClosestMatch
            elif 'c' in options:
                f = self.contains

            if 'u' in options:
                self.fillData(True)
            else:
                self.fillData()

            result = f(args[2:])
            for r in result:
                if('o' in options):
                    print(r)
                else:
                    print('{0} : {1}'.format(r,self.ids[r]))
            
        else:
            self.fillData()            
            result = self.matchWholeWords(args[1:])
            for r in result:
                print('{0} : {1}'.format(r,self.ids[r]))
            

    def __init__(self):
        self.args = sys.argv[1:]
        self.ids = {}
        
        
if __name__ == "__main__":
    controller = Controller()
    controller.handleArgs()








    
