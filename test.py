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
    for tr in rows[1:]:
        non_empty_tds = [x for x in tr.contents if str(x).strip()]
        name = non_empty_tds[3].find('a').string

        dec = non_empty_tds[1]
        if dec.span:
            dec = dec.span.string
        else:
            dec = dec.string

        print dec, name
        
        # Name -- print tr.find('a', title=True)
        # ['', ' ', '\n', 'first']
        # [x for x in l if x.strip()]



print "done!"

