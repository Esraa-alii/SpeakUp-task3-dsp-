import os
import pandas as pd
from flask import Flask, render_template, request
import pickle
import numpy as np
from werkzeug.utils import secure_filename
from functions import extract_features, feat
import pickle
import librosa
import speech_recognition as sr


def test():
    r = sr.Recognizer()
    filelist = os.listdir('../voices//webtest//')
    filename = "../voices/allvoices/file.wav"
    # with sr.AudioFile(filename) as source:
    #     # listen for the data (load audio to memory)
    #     audio_data = r.record(source)
    # # recognize (convert from speech to text)
    #     text = r.recognize_google(audio_data)
    # print(text)
    # read them into pandas
    df_test = pd.DataFrame(filelist)
    df_test['label'] = 0
    df_test = df_test.rename(columns={0: 'file'})
    features_label2 = df_test.apply(extract_features, axis=1)
    features = feat(features_label2)
    model = pickle.load(open('../SpeakUp.pkl', 'rb'))
    return model.predict(features).reshape(1, -1)[0][0]


app = Flask(__name__)

x = None


@app.route("/")
def man():
    return render_template('index.html', result=x)


@app.route("/predict", methods=['POST', 'GET'])
def predict():
    file = request.files['file']
    path = os.path.dirname(__file__)
    file_path = os.path.join("../voices/allvoices", "file.wav")
    file.save(file_path)
    x = test()
    print(x)
    return x


if __name__ == "__main__":
    app.run(debug=True)
