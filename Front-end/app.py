import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
from functions import extract_features, feat, extract_features_of_speech, feat_of_speech
import pickle
from PIL import Image
import base64
import io


def test():
    filelist = os.listdir('../Speaker_Recognition//voices//webtest//')
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
    Fs, aud = wavfile.read('../Speaker_Recognition/voices/allvoices/file.wav')
    aud = aud[:, 0]  # select left channel only
    powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(
        aud, Fs=Fs)
    plt.colorbar()
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.savefig('static/images/spectro.png')
    #im = Image.open("static/images/spectro.png")
    #data = io.BytesIO()
    #im.save(data, "JPEG")
    #encoded_img_data = base64.b64encode(data.getvalue())
    plt.close()
    return speakmodel.predict(features1).reshape(1, -1)[0][0], speechmodel.predict(features2).reshape(1, -1)[0][0]


app = Flask(__name__)
app.testing = True


@app.route("/")
def man():
    return render_template('poster.html', result="")


@app.route("/predict", methods=['POST', 'GET'])
def predict():
    file = request.files['file']
    file_path = os.path.join(
        "../Speaker_Recognition/voices/allvoices", "file.wav")
    file.save(file_path)
    x, y = test()
    print(x, y)
    return render_template('poster.html')


if __name__ == "__main__":
    app.run(debug=True)
