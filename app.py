import os

from flask import Flask
import flask
import json
import easyocr
import cv2
import numpy as np
from translate import Translator

app = Flask(__name__)

count = 0
if count == 0:
    translator = Translator(from_lang="en", to_lang="ur")
    reader = easyocr.Reader(['en'], gpu=False)
    count += 1


def applying_ocr(img):
    return reader.readtext(img, detail=0)

def processing(image):
    text = applying_ocr(image)
    credential = []
    for i in range(len(text)):
        if len(text[i]) == 0:
            pass
        elif text[i][0].lower() == 'n' and text[i][-1].lower() == 'e' and len(text[i]) <= 5:
            credential.append(text[i + 1])
        elif 'ame' in text[i].lower() and len(text[i]) <= 5:
            credential.append(text[i + 1])
        elif 'nam' in text[i].lower() and len(text[i]) <= 5:
            credential.append(text[i + 1])
        elif '-' in text[i] and len(text[i]) >= 13:
            credential.append(text[i])
            break
    if len(credential) == 2 or len(credential) == 3:
        word = translator.translate(credential[0])
        data = {'Name': credential[0], 'Urdu_Name': word, 'ID Num': credential[-1]}
    else:
        data = 'None'

    return data


def main_func(encoded):
    numpy = np.array(encoded, dtype='uint8')
    decode = cv2.imdecode(numpy, cv2.IMREAD_COLOR)
    data = processing(decode)
    return data




@app.route('/', methods=['POST'])
def test():
    input_1 = json.loads(flask.request.data.decode('utf-8'))['img_to_ocr']

    return main_func(input_1)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get('PORT', 8080)))
