#!/usr/bin/env python2.7
from PIL import Image, ImageDraw, ImageFont
import requests, textwrap, csv, random, StringIO
from flask import send_file

_quote_font = ImageFont.truetype('Lato-Regular.ttf', 24)
_author_font = ImageFont.truetype('Lato-Regular.ttf', 14)

#method to process image
def prcoessImage(img, quote, qfont=_quote_font, afont=_author_font):
	#opening image for work.
	im = Image.open(img)
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
	return im.show()

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
	return img_url

def handlingImage(pil_img):
    img_io = StringIO.StringIO()
    return send_file(img_io, mimetype='image/jpeg')