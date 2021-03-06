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

def getColor():
	colorl = ['#F44336', '#9C27B0', '#3F51B5', '#009688', '#607D8B']
	num = random.randint(0,4)
	clr = colorl[num]
	response = {}
	response['color'] = clr
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
	try:
		data = page.json()
	except Exception:
		return 'https://pixabay.com/get/e830b10b29fd063ed95c4518b74a4393e077e5d104b0144193f5c970a0efbc_640.jpg'
	pick_url = random.randint(1,10)
	img_url = data['hits'][pick_url]['webformatURL']
	#returns image url to processImage method
	return img_url

#method to process image
def prcoessImage(img, quote):
	#opening image for work.
	im = Image.open(img)
	width, height = im.size
	while width < 640 and height < 380:
		img_url = getImage()
		img = requests.get(img_url, stream=True).raw
		im = Image.open(img)
		width, height = im.size
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
	clr = getColor()
	draw = ImageDraw.Draw(im)
	x, y = 20, cropDim/8
	for text in quoteText:
		draw.text((x,y), text, clr['color'], qfont)
		y = y + 20
	#writing author
	y = y + 50
	x = x + 20
	draw.text((x,y), '-'+quoteAuthor, clr['color'], afont)
	#displaying image
	byte_io = io.BytesIO()
	im.save(byte_io, 'PNG')
	byte_io.seek(0)
	return byte_io