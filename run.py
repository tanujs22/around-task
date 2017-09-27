from flask import Flask, send_file
# from app import prcoessImage, getQuote, getImage
from app import *


app = Flask(__name__)


@app.route('/')
def requiredImage():
	image = prcoessImage(requests.get(getImage(), stream=True).raw, getQuote())
	return send_file(image, mimetype = 'image/jpg')

if __name__ == "__main__":
		app.run()