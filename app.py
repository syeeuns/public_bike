import requests
import json
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbbike

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    db.bikeSearch.drop()
    word = request.form['name']

    url = 'http://openapi.seoul.go.kr:8088/56664c746a6461653636754642686c/json/bikeList/1/1000'
    data = requests.get(url)
    api = json.loads(data.content)
    target = api['rentBikeStatus']['row']

    for one in target:
        name = one['stationName']
        if word in name:
            rack = one['rackTotCnt']
            parking = one['parkingBikeTotCnt']
            rate = one['shared']
            bike = {
                'name':name,
                'rack':rack,
                'parking':parking,
                'rate':rate
            }
            db.bikeSearch.insert_one(bike)
    return jsonify({'result':'success', 'msg':'검색 완료'})


@app.route('/search', methods=['GET'])
def show():
    result = list(db.bikeSearch.find({},{'_id':0}).sort('parking', -1))
    return jsonify({'result':'success', 'bike':result})


if __name__ == '__main__':
    app.run()
