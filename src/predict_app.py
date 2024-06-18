"""House price prediction service"""

from flask import Flask, request
from flask_httpauth import HTTPTokenAuth
from flask_cors import CORS
from joblib import load
from dotenv import dotenv_values
import json
import catboost

app = Flask(__name__)
CORS(app)

MODEL_PATH = 'models/catboost_v02.joblib'
config = dotenv_values(".env")
auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    config["APP_TOKEN"]: "user1",
}

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]



def predict(in_data: dict) -> int:
    """ Predict house price from input data parameters.
    :param in_data: house parameters.
    :raise Error: If something goes wrong.
    :return: House price, RUB.
    :rtype: int
    """
    area = float(in_data['total_meters'])
    floor = int(in_data["floor"])
    floors_count = int(in_data["floors_count"])
    rooms = int(in_data["rooms_count"])
    underground = str(in_data["underground"])
    author_type = str(in_data["author_type"])

    floor = floor if floor <= floors_count else floors_count
    first_floor = floor == 1
    last_floor = floor == floors_count

    #in_file = open("data/dicts/underground.json", "r", encoding='utf8')
    #underground_dict = json.load(in_file)
    #try:
     #   underground = underground_dict[underground]
    #except KeyError:
     #   underground = underground_dict["NaN"]

    #in_file.close()

    model = load(MODEL_PATH)
    price = model.predict([[area,author_type,first_floor,
                            last_floor,floor,floors_count,rooms,underground]])
    return int(price.squeeze())

@app.route("/")
def home():
    return '<h1>Housing price service.</h1> Use /predict endpoint'

@app.route("/predict", methods=['POST'])
@auth.login_required
def predict_web_serve():
    """Dummy service"""
    in_data = request.get_json()
    price = predict(in_data)
    return {'price': price}


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
