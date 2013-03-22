# Minecraft Librarian


## About

Originally I created this program to learn more about python, and to save time in the 

1. Lookup Minecraft Object ID 
2. Write Macro
3. Set Macro 

Process

## Usage


	usage: MinecraftMiner.py [-h] [-a] [-o] [-u] W [W ...]

	Search for minecraft objects ids by name. Gets information from Minecraft
	wiki. First run scrapes the wiki and subsequent runs refer to the cache.

	positional arguments:
	  W              The search words

	optional arguments:
	  -h, --help     show this help message and exit
	  -a, --any      Search for words that contain any of the search words. The
					 default is to search for words that contain ALL the search
					 words
	  -o, --only-id  Only output the ids of the minecraft objects
	  -u, --update   Force the program to scrape from the wiki instead of using
					 the cache

## Examples

Something Simple

	$ MinecraftMiner.py leather
	298  Leather Cap
	299  Leather Tunic
	300  Leather Pants
	301  Leather Boots
	334  Leather
	
Something more useful for scripts

	$ MinecraftMiner.py leather boots
	301  Leather Boots

Order not required!

	$ MinecraftMiner.py boots leather
	301  Leather Boots
	
Multi search

	$ MinecraftMiner.py -a leather fish
	346  Fishing Rod
	298  Leather Cap
	299  Leather Tunic
	300  Leather Pants
	301  Leather Boots
	334  Leather
	349  Raw Fish
	350  Cooked Fish
	
Force an Update (Useful when the wiki gets updated)

	$ MinecraftMiner.py redstone block
	$ MinecraftMiner.py -u redstone block
	152  Block of Redstone

Return only the id (Useful for making scripts that make macros!)

	$ MinecraftMiner.py -o iron sword
	267
	
## Disclaimer
This software is released under the [MIT License](http://opensource.org/licenses/MIT)
