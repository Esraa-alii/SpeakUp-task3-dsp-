import os
from flask import Flask, render_template, request
import pickle
import numpy as np
from werkzeug.utils import secure_filename

model = pickle.load(open('model.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def man():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
       if request.files['audio']:
           file=request.files['audio']
           path=os.path.dirname(__file__)
           file_path=os.path.join(path,'Uploads',secure_filename(file.filename) )
           file_path+='.wav'
           file.save(file_path)
       
   

if __name__ == "__main__":
    app.run(debug=True)














