from flask import Flask
import logging

app = Flask(__name__)
app.config.from_object('config')


from app import views
logging.basicConfig(level=logging.DEBUG)