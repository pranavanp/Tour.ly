from flask import Flask, render_template
import requests
import json
import mysql.connector
import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyCCS5T6FWRBoUlqqZr2_of2nAX7yja6T4M')
""""
mydb=mysql.connector.connect(
    host="us-cdbr-iron-east-04.cleardb.net",
    user="bbdccec165669c",
    passwd="cda80eaf32106b7",
)
mycursor =mydb.cursor()
mycursor.execute("CREATE DATABASE response_data")

"""
API_KEY = 'eeRfgoKD6VwjLh3bIiXPsu-h59GJ2AcGZV6M7RmzqDNx87VGgx3TMgf9RwPjE8b38pYqOJFtqnY2N5zPqSIEguy4F6HfupmEAsV0xphGW_sXrSlCeJlIFVXl3TtPXnYx'
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % API_KEY}

##keyword
##expensive=input()

terms = 'pasta'
keywords = 'italian,restaurants'
location = 'Toronto'
pick_up_adress = 'Scarborough, Ontario'
num_of_attractions = 10
price = '$$'

PARAMETERS = {'term': 'arts',
              'limit': num_of_attractions,
              'offset': 150,
              'radius': 10000,
              'price': 2,
              'sort_by': 'rating',
              'location': location}

response = requests.get(url=ENDPOINT,
                        params=PARAMETERS,
                        headers=HEADERS)

destinations = []
business_data = response.json()
for biz in business_data['businesses']:
    biz_name = biz['name']
    biz_address = biz['location']['address1']
    directions = gmaps.distance_matrix(pick_up_adress, biz_address,
                                       departure_time=datetime.now(),
                                       mode="transit")
    travel_data = directions['rows'][0]['elements'][0]
    status = travel_data['status']
    if (status == 'ZERO_RESULTS'):
        print('N/A')
    else:
        travel_distance = travel_data['distance']['text']
        travel_time = travel_data['duration']['text']
        destinations.append([biz_name, biz_address, travel_distance, travel_time])
print(destinations)

app = Flask(__name__)
# defining home page
@app.route('/')
def homepage():
    # returning index.html and list
    # and length of list to html page
    return render_template("test.html", len=len(destinations), destinations=destinations)

if __name__ == '__main__':
    app.run()
