import requests
import datetime
from flask import Flask, jsonify, request

API_TOKEN = ""
API_KEY = ""

app = Flask(__name__)


@app.route('/weather', methods=['GET'])
def get_weather():
    token = request.args.get('token')
    
    if token is None:
        raise InvalidUsage("token is required", status_code=400)

    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)

    requester_name = request.args.get('requester_name')
    location = request.args.get('location')
    date = request.args.get('date')

    url = f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={location}&dt={date}"
    response = requests.get(url)

    if response.status_code == 200:
        date_data = response.json()['forecast']['forecastday'][0]['date']

        weather_data = response.json()['forecast']['forecastday'][0]['day']
        weather = {
            "avg_temp_c": weather_data['avgtemp_c'],
            "avg_humidity": weather_data['avghumidity'],
            "max_wind_kph": weather_data['maxwind_kph'],
            "condition": weather_data['condition']['text']
        }
        location_data = response.json()['location']
        location = {
            "name": location_data['name'],
            "region": location_data['region'],
            "country": location_data['country'],
            "latitude": location_data['lat'],
            "longitude": location_data['lon'],
            "tz_id": location_data['tz_id']
        }
        weather_response = {
            "requester_name": requester_name,
            "timestamp": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "date": date_data,
            "location": location,
            "weather": weather
        }
        return jsonify(weather_response)
    else:
        return jsonify({"error": f"Error: {response.status_code} - {response.reason}"}), response.status_code

@app.route("/")
def home_page():
    return "<p><h2>KMA HW1: Weather API.</h2></p>"

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv