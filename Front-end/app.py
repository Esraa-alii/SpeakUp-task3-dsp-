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
import pydotplus
from sklearn import tree


def drawpath(feature, clf):

    dot_data = tree.export_graphviz(clf, out_file=None,
                                    filled=True, rounded=True,
                                    special_characters=True)
    graph = pydotplus.graph_from_dot_data(dot_data)

    # empty all nodes, i.e.set color to white and number of samples to zero
    for node in graph.get_node_list():
        if node.get_attributes().get('label') is None:
            continue
        if 'samples = ' in node.get_attributes()['label']:
            labels = node.get_attributes()['label'].split('<br/>')
            for i, label in enumerate(labels):
                if label.startswith('samples = '):
                    labels[i] = 'samples = 0'
            node.set('label', '<br/>'.join(labels))
            node.set_fillcolor('white')

    samples = feature
    decision_paths = clf.decision_path(samples.reshape(1, -1))

    for decision_path in decision_paths:
        for n, node_value in enumerate(decision_path.toarray()[0]):
            if node_value == 0:
                continue
            node = graph.get_node(str(n))[0]
            node.set_fillcolor('green')
            labels = node.get_attributes()['label'].split('<br/>')
            for i, label in enumerate(labels):
                if label.startswith('samples = '):
                    labels[i] = 'samples = {}'.format(
                        int(label.split('=')[1]) + 1)

            node.set('label', '<br/>'.join(labels))

    filename = 'static/images/tree.png'
    graph.write_png(filename)


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
    drawpath(features1[0], speakmodel)
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

    if x == "0" or y == "other":
        playsound("acces.mp3")
    elif x == 'Abdo':
        playsound("abdo.mp3")
    elif x == 'Esraa':
        playsound("Esraa.mp3")
    else:
        playsound("Mariam.mp3")

    return x, y


if __name__ == "__main__":
    app.run(debug=True)
