from flask import Flask, jsonify, request, render_template
from math import radians, cos, sin, asin, sqrt
from flask_cors import CORS
import couchdb
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

app = Flask(__name__)
CORS(app)

couch = couchdb.Server('http://127.0.0.1:5984')
couch.resource.credentials = ('admin', '54321')
db = couch['restos']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rating')
def rating():
    return render_template('rating.html')

@app.route('/name')
def name():
    return render_template('name.html')

@app.route('/minrating')
def min_rating():
    return render_template('min_rating.html')

@app.route('/solo_rating')
def solo_rating():
    return render_template('solo_rating.html')

@app.route('/recent_rating')
def recent_rating():
    return render_template('recent_rating.html')

@app.route('/location')
def location():
    return render_template('location.html')

@app.route('/zipcode')
def zipcode():
    return render_template('zipcode.html')

@app.route('/coordinates')
def coordinates():
    return render_template('coordinates.html')

@app.route('/score')
def score():
    return render_template('score.html')

@app.route('/score_comparar')
def score_comparar():
    return render_template('score_comparar.html')

@app.route('/recent_openings')
def recent_openings():
    return render_template('recent_openings.html')


@app.route('/fetch_restaurants', methods=['GET'])
def fetch_restaurants():
    borough = request.args.get('borough', '')
    cuisine = request.args.get('cuisine', '')
    rating = request.args.get('rating', '')

    mango_query = {
        "selector": {
            "borough": {"$regex": f"{borough}.*"} if borough else {"$exists": True},
            "cuisine": {"$regex": f"{cuisine}.*"} if cuisine else {"$exists": True}
        }
    }

    response = db.find(mango_query)
    restaurants = [doc for doc in response]
    return jsonify(restaurants), 200


@app.route('/fetch_restaurants_by_rating', methods=['GET'])
def fetch_restaurants_by_rating():
    borough = request.args.get('borough', '')
    cuisine = request.args.get('cuisine', '')
    rating = request.args.get('rating', '')

    mango_query = {
        "selector": {
            "borough": {"$regex": f"{borough}.*"} if borough else {"$exists": True},
            "cuisine": {"$regex": f"{cuisine}.*"} if cuisine else {"$exists": True},
            "grades.0.grade": {"$regex": f"{rating}.*"} if rating else {"$exists": True}
        },
        "limit": 20000 
    }

    response = db.find(mango_query)
    restaurants = [doc for doc in response]
    return jsonify(restaurants), 200


@app.route('/restaurants_by_name', methods=['GET'])
def get_restaurants_by_name():
    name = request.args.get('name', '')
    
    mango_query = {
        'selector': {
            'name': {'$regex': f'(?i){name}'}
            },  

        'limit': 100
    }

    response = db.find(mango_query)
    restaurants = [doc for doc in response]
    return jsonify(restaurants), 200

@app.route('/restaurants_by_location', methods=['GET'])
def get_restaurants_by_location():
    location = request.args.get('location', '')

    mango_query = {
        'selector': {
            'address.street': {'$regex': f'(?i){location}'}
            },  

        'limit': 100
    }

    response = db.find(mango_query)
    restaurants = [doc for doc in response]
    return jsonify(restaurants), 200

@app.route('/restaurants_by_zipcode', methods=['GET'])
def get_restaurants_by_zipcode():
    zipcode = request.args.get('location', '')

    mango_query = {
        'selector': {
            'address.zipcode': {'$regex': f'(?i){zipcode}'}
            },  

        'limit': 100
    }

    response = db.find(mango_query)
    restaurants = [doc for doc in response]
    return jsonify(restaurants), 200

@app.route('/fetch_restaurants_solo_rating', methods=['GET'])
def fetch_restaurants_solo_rating():
    rating = request.args.get('rating', '')

    mango_query = {
        "selector": {
            "grades.0.grade": {"$regex": f"{rating}.*"} if rating else {"$exists": True}
        },
        "limit":20000
    }

    response = db.find(mango_query)
    restaurants = [doc for doc in response]
    return jsonify(restaurants), 200

@app.route('/restaurants_by_coordinates', methods=['GET'])
def get_restaurants_by_coordinates():
    lon = float(request.args.get('lon', '0'))
    lat = float(request.args.get('lat', '0'))
    distance = float(request.args.get('distance', '1'))  
    
    delta_lon = distance / (111.32 * cos(radians(lat)))
    delta_lat = distance / 110.574

    min_lon = lon - delta_lon
    max_lon = lon + delta_lon
    min_lat = lat - delta_lat
    max_lat = lat + delta_lat

    mango_query = {
        "selector": {
            "address.coord.0": {"$gte": min_lon, "$lte": max_lon},
            "address.coord.1": {"$gte": min_lat, "$lte": max_lat}
        },
        "limit": 100
    }

    response = db.find(mango_query)
    restaurants = [doc for doc in response]
    return jsonify(restaurants), 200





@app.route('/restaurants_by_score', methods=['GET'])
def get_restaurants_by_score():
    score = request.args.get('score', '')

    mango_query = {
        'selector': {
            'grades.0.score': int(score)
        },
        'limit': 100
    }

    response = db.find(mango_query)
    restaurants = [doc for doc in response]
    return jsonify(restaurants), 200


@app.route('/restaurants_by_score_comparison', methods=['GET'])
def get_restaurants_by_score_comparison():
    score = request.args.get('score', '')
    comparison = request.args.get('comparison', 'lt')

    if comparison == 'lt':
        mango_query = {
            'selector': {
                'grades.0.score': {'$lt': int(score)}
            },
            'limit': 100
        }
    elif comparison == 'gt':
        mango_query = {
            'selector': {
                'grades.0.score': {'$gt': int(score)}
            },
            'limit': 100
        }
    else:
        return jsonify({'error': 'Invalid comparison parameter'}), 400

    response = db.find(mango_query)
    restaurants = [doc for doc in response]
    return jsonify(restaurants), 200

@app.route('/fetch_recent_openings', methods=['GET'])
def fetch_recent_openings():
    recent_date_str = request.args.get('recent_date', '')
    recent_date = datetime.strptime(recent_date_str, '%Y-%m-%d').isoformat()


    mango_query = {
        "selector": {
            "grades.0.date": {
                "$gte": recent_date
            }
        },
        "limit": 100
    }

    response = db.find(mango_query)
    restaurants = [doc for doc in response]

    return jsonify(restaurants), 200



if __name__ == '__main__':
    app.run(debug=True)