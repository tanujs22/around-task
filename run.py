#!/usr/bin/env python2.7
from flask import Flask, send_file, render_template
import io
from app import *


app = Flask(__name__)


@app.route('/')
def requiredImage():
	image = prcoessImage(requests.get(getImage(), stream=True).raw, getQuote())
	return send_file(io.BytesIO(image), mimetype = 'image/jpeg')

if __name__ == "__main__":
		app.run()