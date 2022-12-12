import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
from functions import extract_features, feat, extract_features_of_speech, feat_of_speech
import pickle
from playsound import playsound
from gtts import gTTS
from pygame import mixer


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

    # os.remove(
    #    'C:/Users/nasse/OneDrive/Desktop/New folder (5)/SpeakUp-task3-dsp-/Front-end/exam.mp3')
    language = 'en'
    print(x, y)
    text_val = ""
    if x == "0" or y == "other":
        text_val = 'access denied'
    elif x == 'Abdo':
        text_val = 'Abdo'
    elif x == 'Esraa':
        text_val = 'Esraa'
    else:
        text_val = 'Mariam'
    obj = gTTS(text=text_val, lang=language)
    obj.save("exam.mp3")
    playsound("exam.mp3")
    return x, y


if __name__ == "__main__":
    app.run(debug=True)
