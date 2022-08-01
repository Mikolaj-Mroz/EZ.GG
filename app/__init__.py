# Author: Mikołaj Mróz
# E-mail: mikolajmroz.biz@gmail.com
# Created on: 24.07.2022

from flask import Flask

# configuration

app = Flask(__name__)
app.config.from_pyfile('config.py')

from app.modules import routes