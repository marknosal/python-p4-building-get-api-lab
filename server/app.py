#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    response_body = []
    for bakery in Bakery.query.all():
        bakery_dict = bakery.to_dict()
        response_body.append(bakery_dict)
    response = make_response(jsonify(response_body), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    bakery_dict = bakery.to_dict()
    response = make_response(jsonify(bakery_dict), 200)
    response.headers['Content-Type'] = 'application/json'
    return response 

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    sorted_goods = BakedGood.query.order_by(BakedGood.price).all()

    response_body = [bg.to_dict() for bg in sorted_goods]

    response = make_response(jsonify(response_body), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    sorted_by_price_ascending = BakedGood.query.order_by(BakedGood.price).all()
    most_expensive_bg = sorted_by_price_ascending[-1]
    response_body = most_expensive_bg.to_dict()
    response = make_response(jsonify(response_body), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
