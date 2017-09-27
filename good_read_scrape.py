#!/usr/bin/env python2.7
from bs4 import BeautifulSoup
import urllib2

text = []
author = []

for i in range(1,37):
	url = 'https://www.goodreads.com/quotes/list/27968333-around-io?page=%s' %str(i)
	usock = urllib2.urlopen(url)
	data = usock.read()
	soup = BeautifulSoup(data, 'html.parser')
	for script in soup("script"):
		script.extract()
	q = soup.findAll('div',{'class': 'quoteText'})
	quotes = []
	for ele in q:
		quotes.append(ele.get_text())
	print i
	for line in quotes:
		text.append(line.split('    ')[1].encode('ascii', 'ignore').strip('\n').strip(' '))
		author.append(line.split('    ')[3].encode('ascii', 'ignore').strip('\n'))
