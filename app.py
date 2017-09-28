#!/usr/bin/env python2.7
from PIL import Image, ImageDraw, ImageFont
import requests, textwrap, csv, random, StringIO, base64, io
from flask import send_file, render_template

def getFont():
	fontl = ['Lato-Regular.ttf', 'Pacifico-Regular.ttf', 'Lobster-Regular.ttf', 'GermaniaOne-Regular.ttf']
	num = random.randint(0,3)
	fnt = fontl[num]
	response = {}
	response['quote_font'] = ImageFont.truetype(fnt, 24)
	response['author_font'] = ImageFont.truetype(fnt, 14)
	return response

#method to fetch quotes
def getQuote():
	#opening csv
	file = open('good_read.csv', 'rU')
	reader = csv.DictReader(file)
	#building list 
	qlist = []
	for r in reader:
		qlist.append(r)
	#for giving random quotes
	num = random.randint(1,1060)
	quote_auth = qlist[num]
	qu = {'author' : quote_auth['author'], 'quote' : quote_auth['quote']}
	return qu

#method to fetch image
def getImage():
	#random page selection
	num = random.randint(1,5)
	url = 'https://pixabay.com/api/?key=6553074-1b6f2bc332fcf4f5589fcc559&q=landscape&image_type=photo&pretty=true&page=%s' % num
	page = requests.get(url)
	data = page.json()
	pick_url = random.randint(1,10)
	img_url = data['hits'][pick_url]['webformatURL']
	#returns image url to processImage method
	print img_url
	return img_url

#method to process image
def prcoessImage(img, quote):
	#opening image for work.
	im = Image.open('fff3.png')
	width, height = im.size
	print width
	while width < 640:
		print 'reach'
		img_url = getImage()
		print img_url
		img = requests.get(img_url, stream=True).raw
		im = Image.open(img)
		width, height = im.size
	print width, height
	cropDim = im.size[1]
	left = (im.size[0]/2) - (cropDim/2)
	right = (im.size[0]/2) + (cropDim/2)
	im = im.crop((left, 0, right, cropDim))
	#adding grey filter for text
	filter = Image.new("RGBA", im.size, (62, 39, 35, 127))
	im.paste(filter, None, filter)
	#tweaking text
	quoteText = textwrap.wrap(quote['quote'], width = 25)
	quoteAuthor = quote['author']
	#writing text
	fnt = getFont()
	qfont = fnt['quote_font']
	afont = fnt['author_font']
	draw = ImageDraw.Draw(im)
	x, y = 20, cropDim/8
	for text in quoteText:
		draw.text((x,y), text, 'white', qfont)
		y = y + 20
	#writing author
	y = y + 50
	x = x + 20
	draw.text((x,y), '-'+quoteAuthor, 'white', afont)
	#displaying image
	byte_io = io.BytesIO()
	im.save(byte_io, 'PNG')
	byte_io.seek(0)
	return byte_io