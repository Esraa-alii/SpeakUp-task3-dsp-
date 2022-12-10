import os
import pandas as pd
from flask import Flask, render_template, request
import pickle
import numpy as np
from werkzeug.utils import secure_filename
from functions import extract_features, feat, extract_features_of_speech, feat_of_speech
import pickle
import librosa


def test():
    filelist = os.listdir('../Speaker_Recognition//voices//webtest//')
    filename = "../voices/allvoices/file.wav"
    # read them into pandas
    df_test = pd.DataFrame(filelist)
    df_test['label'] = 0
    df_test = df_test.rename(columns={0: 'file'})
    features_label1 = df_test.apply(extract_features, axis=1)
    features1 = feat(features_label1)
    features_label2 = df_test.apply(extract_features_of_speech, axis=1)
    features2 = feat_of_speech(features_label2)
    speakmodel = pickle.load(open('../Speaker_Recognition/SpeakUp.pkl', 'rb'))
    speechmodel = pickle.load(
        open('../Speaker_Recognition/SpeechUp.pkl', 'rb'))
    return speakmodel.predict(features1).reshape(1, -1)[0][0], speechmodel.predict(features2).reshape(1, -1)[0][0]


app = Flask(__name__)

x = None


@app.route("/")
def man():
    return render_template('poster.html', result=x)


@app.route("/predict", methods=['POST', 'GET'])
def predict():
    file = request.files['file']
    path = os.path.dirname(__file__)
    file_path = os.path.join(
        "../Speaker_Recognition/voices/allvoices", "file.wav")
    file.save(file_path)
    x, y = test()
    print(y)
    return x


if __name__ == "__main__":
    app.run(debug=True)
