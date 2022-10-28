from NIC_main import main_func
from flask import Flask
import flask
import json

app = Flask(__name__)


@app.route('/', methods=['POST'])
def test():
    input_1 = json.loads(flask.request.data.decode('utf-8'))['img_to_ocr']

    return main_func(input_1)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
