from flask import Flask

# configuration

app = Flask(__name__)
app.secret_key='tekst'

from app.modules import routes