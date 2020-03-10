from os import environ
from flask import Flask
 
APP = Flask(__name__)
APP.run(host='0.0.0.0', port=environ.get('PORT'))