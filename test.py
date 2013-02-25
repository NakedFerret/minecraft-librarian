#! /usr/bin/env python2

from BeautifulSoup import BeautifulSoup, SoupStrainer

block_type_header = "<th>Block type</th>"
item_header = "<th>Item</th>"


f = open("data_values.html")
source = f.read()
f.close();

soup =  BeautifulSoup(source, parseOnlyThese=SoupStrainer('table'))

for t in soup:
    if block_type_header in t.first().renderContents():
        print t.first()
    if item_header in t.first().renderContents():
        print t.first()

print "done!"

