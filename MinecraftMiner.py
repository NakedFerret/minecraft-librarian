#! /usr/bin/env python2

import os
from TableScraper import WikiTableScraper
import argparse
import pickle

# the directory where the cache file will be stored
CACHE_DIR = "minecraft-miner"
# Name of the cache file
FILE_NAME = 'minecraft_objects.cache'

# Help texts
DESCRIPTION = """Search for minecraft objects ids by name. Gets information from Minecraft wiki. First run scrapes the wiki and subsequent runs refer to the cache."""
POSITIONAL_HELP = """The search words"""
SEARCH_HELP = """Search for words that contain any of the search words. The default is to search for words that contain ALL the search words"""
ID_HELP = """Only output the ids of the minecraft objects"""
UPDATE_HELP = """Force the program to scrape from the wiki instead of using the cache"""

class Controller(object):
    """This class fetches the minecraft objects from WikiTableScraper, 
    and searches for item names that match search words. 
    Uses a cache through the pickle module to speed up subsequent searches.
    """
    def __init__(self):
        """Setup the argument parser"""
        # Dict of minecraft object in form of "dict[id] = name"
        self.data_values = dict()
        self.parser = self.setup_parser()

    def main(self):
        """Get the objects from the parser (or cache), 
        search through them, and print the results """

        args = self.parser.parse_args()
        # Little magic/abomination to avoid a if-else
        # funct == search_all or search_any
        funct = getattr(self, "search_" + args.search_funct) 
        cache_file_path = self.get_cache_file_path()

        # If cache is missing or user asked to force an update
        # then scrape the wiki
        if not os.path.isfile( cache_file_path ) or args.update:
            self.data_values = WikiTableScraper().scrapeTables()
            pickle.dump( self.data_values, open( cache_file_path, "wb" ) )
        # else load the minecraft objects from cache
        else:
            self.data_values = pickle.load( open( cache_file_path, "rb" ) )

        # call the search function (will return list of ids)
        for k in funct(args.words):
            print k.ljust(4), # Don't print a newline
            # Don't print the name if user requested only id's
            if not args.only_id:
                print self.data_values[k],
            print # print the newline now

    def get_cache_file_path(self):
        """Returns the path of the cache file.
        Side-Effect: creates ~/.cache or ~/.cache/CACHE_DIR"""
        home_path = os.path.expanduser("~")
        # path to the programs cache directory
        full_cache_dir =  os.path.join(home_path, ".cache", CACHE_DIR)

        if not os.path.exists( full_cache_dir ):
            os.makedirs( full_cache_dir )
        
        return os.path.join( full_cache_dir, FILE_NAME )

    def search_all(self, word_list):
        """Returns list of keys of minecraft objects whose names contain
        ALL the search words """
        return [k for k,v in self.data_values.iteritems() 
                if all(w.lower() in v.lower() for w in word_list)]

    def search_any(self, word_list):
        """Returns list of keys of minecraft objects whose names contain
        ANY the search words """
        # Same as search_all except uses the built-in any()
        return [k for k,v in self.data_values.iteritems() 
                if any(w.lower() in v.lower() for w in word_list)]

    def setup_parser(self):
        """Returns an argument parser already initialized"""
        parser = argparse.ArgumentParser(description=DESCRIPTION)
        parser.add_argument('words', metavar='W', nargs='+', help=POSITIONAL_HELP)
        parser.add_argument('-a','--any', dest="search_funct", action="store_const", 
                            const='any', default='all', help=SEARCH_HELP)
        parser.add_argument('-o','--only-id', action='store_true', help=ID_HELP)
        parser.add_argument('-u', '--update', action='store_true', help=UPDATE_HELP)
        return parser
        
if __name__ == "__main__":
    controller = Controller()
    controller.main()








    
