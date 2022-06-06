from flask import Flask, flash, request, redirect, url_for, render_template
from flask import Flask
import json
app = Flask(__name__)

#GET DATA FROM JSON
# def get_rankedcoins():
file= open('backend_data/sample.json')
data = json.load(file)

@app.route("/")
def home():
     return render_template('index.html',data = data)
 
