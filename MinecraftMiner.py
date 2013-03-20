#! /usr/bin/env python2

import os
from TableScraper import WikiTableScraper
import argparse
import pickle

CACHE_DIR = "minecraft-miner"
FILE_NAME = 'minecraft_objects.cache'

DESCRIPTION = """Search for minecraft objects ids by name. Gets information from Minecraft wiki. First run scrapes the wiki and subsequent runs refer to the cache."""
POSITIONAL_HELP = """The search words"""
SEARCH_HELP = """Search for words that contain any of the search words. The default is to search for words that contain ALL the search words"""
ID_HELP = """Only output the ids of the minecraft objects"""
UPDATE_HELP = """Force the program to scrape from the wiki instead of using the cache"""

class Controller(object):

    def get_cache_file_path(self):
        home_path = os.path.expanduser("~")
        full_cache_dir =  os.path.join(home_path, ".cache", CACHE_DIR)

        if not os.path.exists( full_cache_dir ):
            os.makedirs( full_cache_dir )
        
        return os.path.join( full_cache_dir, FILE_NAME )

    def search_all(self, word_list):
        return [k for k,v in self.ids.iteritems() 
                if all(w.lower() in v.lower() for w in word_list)]

    def search_any(self, word_list):
        return [k for k,v in self.ids.iteritems() 
                if any(w.lower() in v.lower() for w in word_list)]

    def main(self):
        args = self.parser.parse_args()
        funct = getattr(self, "search_" + args.search_funct)
        cache_file_path = self.get_cache_file_path()

        if not os.path.isfile( cache_file_path ) or args.update:
            self.ids = WikiTableScraper().scrapeTables()
            pickle.dump( self.ids, open( cache_file_path, "wb" ) )
        else:
            self.ids = pickle.load( open( cache_file_path, "rb" ) )

        for k in funct(args.words):
            print k.ljust(4),

            if not args.only_id:
                print self.ids[k],

            print 
                        
    def setupParser(self):
        parser = argparse.ArgumentParser(description=DESCRIPTION)
        parser.add_argument('words', metavar='W', nargs='+', help=POSITIONAL_HELP)
        parser.add_argument('-a','--any', dest="search_funct", action="store_const", 
                            const='any', default='all', help=SEARCH_HELP)
        parser.add_argument('-o','--only-id', action='store_true', help=ID_HELP)
        parser.add_argument('-u', '--update', action='store_true', help=UPDATE_HELP)
        return parser

    def __init__(self):
        self.ids = dict()
        self.parser = self.setupParser()
        
if __name__ == "__main__":
    controller = Controller()
    controller.main()








    
