import urllib.request
import json
import requests
from pprint import pprint
import time
import pdb

f = open('key.txt')
API_KEY = f.read()
f.close()

def error_code(code):
    return (code > 400)

def get_routes(origin_id, destination_id, date_out, date_in):

    session_params = {
        'cabinclass':"Economy",
        'country':"UK",
        'currency':'GBP',
        'locale':'en-GB',
        'locationSchema':'iata',
        'originplace': origin_id,
        'destinationplace': destination_id,
        'outbounddate':date_out,
        'inbounddate':date_in,
        'adults':1,
        'apiKey': API_KEY,
        'limit':3
    }

    response = requests.post('http://partners.api.skyscanner.net/apiservices/pricing/v1.0', session_params)
    session_key = response.headers.get('location')
    print("Session key", session_key)
    if response.status_code != 201:
        return None

    json = None
    success = False
    while (not error_code(response.status_code)):
        print("POLLING")
        response = requests.get(session_key, {
            'apiKey': API_KEY
        }, headers={'Cache-Control': 'no-cache'})
        print(response.status_code, response.headers)

        if response.status_code == 200:
            json = response.json()
            if json['Status'] == 'UpdatesComplete':
                success = True
                break

        time.sleep(.25)

    if not success:
        return None


    itineraries = json['Itineraries']

    result = []
    flights_itineraries = itineraries[0]

    if flights_itineraries:
        flights = itineraries[0]
        pricing_options = flights_itineraries['PricingOptions']
        for index, flight in enumerate(pricing_options):
            flight_price = pricing_options[index]['Price']
            flight_url = pricing_options[index]['DeeplinkUrl']

            entry = {'price': flight_price, 'url': flight_url}
            result.append(entry)

    # Get the top 3 results
    return result[:3]
