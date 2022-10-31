import easyocr
import cv2
import numpy as np
from translate import Translator
count = 0

if count == 0:
    # translator = Translator(service_urls=[
    #     'translate.google.com',
    #     'translate.google.co.kr',
    # ])
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
        # translations = translator.translate(credential[0], src='en', dest='ur')

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
