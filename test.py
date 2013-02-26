#! /usr/bin/env python2

from BeautifulSoup import BeautifulSoup, SoupStrainer

block_type_header = "<th>Block type</th>"
item_header = "<th>Item</th>"

def extract_decimal(td):
    dec = td
    if td.span:
        dec = td.span.string
    else:
        dec = td.string
        
    return dec
                           
def extract_name(td):
    name = td
    if td.find('sup'):
        td.find('sup').extract()

    if td.find('a'):
        name = td.find('a').string
    else:
        name = td.string

    return name


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

for t in tables:
    rows = t.findAll('tr')
    for tr in rows[1:]:
        non_empty_tds = [x for x in tr.contents if str(x).strip()]

        dec = extract_decimal(non_empty_tds[1])
        name = extract_name(non_empty_tds[3])
        
        if len(name) < 3:
            print("-error-") 

        print dec,name
        

print "done!"

