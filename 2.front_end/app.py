from flask import Flask, flash, request, redirect, url_for, render_template
from flask import Flask
from werkzeug.utils import secure_filename
import json
import os
#import magic
import urllib.request
from flask import Flask
import cv2
from pyzbar import pyzbar
from PIL import Image
import ast

# from werkzeug import secure_filename
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
space=[]
lst = []

#GET DATA FROM JSON
# def get_rankedcoins():
with open('backend_data/sample.json') as f:
   data = json.load(f)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template('index.html',data = data)

@app.route('/', methods=['POST','GET'])
def upload_image():
    #5.1.GET USERNAME
    if request.method == "POST":
        print("in location")

    #5.2.IMPLEMENT ERROR HANDLING
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        #READ QR CODE
        image = Image.open('static/uploads/'+filename)
        qr_code = pyzbar.decode(image)[0]
        #convert into string
        new_data= qr_code.data.decode("utf-8")
        #APPEND DATA IN JSON
        data.append(ast.literal_eval(new_data))

        #WRITE TO JSON FILE
        with open('backend_data/sample.json', 'w') as json_file:
         json.dump(data, json_file, 
                         indent=4,  
                         separators=(',',': '))
        
        return render_template('index.html', filename=filename, data = data)

     
        

     #    return render_template('index.html', filename=filename, data = data)
        

    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

if __name__ == '__main__':
   app.run(debug = True)