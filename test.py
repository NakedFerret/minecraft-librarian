#! /usr/bin/env python2

from BeautifulSoup import BeautifulSoup, SoupStrainer

block_type_header = "<th>Block type</th>"
item_header = "<th>Item</th>"

f = open("data_values.html")
source = f.read()
f.close();

soup =  BeautifulSoup(source, parseOnlyThese=SoupStrainer('table'))

tables = list()

for t in soup:
    if block_type_header in t.first().renderContents():
        tables.append(t)
    if item_header in t.first().renderContents():
        tables.append(t)

for t in tables[:1]:
    rows = t.findAll('tr')
    for tr in rows[1:2]:
        td_list = [x for x in tr.contents if strip(x)]
        print td_list
        # Name -- print tr.find('a', title=True)
        # ['', ' ', '\n', 'first']
        # [x for x in l if x.strip()]



print "done!"

