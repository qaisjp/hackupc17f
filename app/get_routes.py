import urllib.request
import json
import requests
from pprint import pprint
import time
import pdb

f = open('key.txt')
API_KEY = f.read()
f.close()

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
    link = response.headers['Location'] + "?apiKey=" + API_KEY
    print(link)
    time.sleep(2)

    request_params = {
        'sortType': 'price',
        'sortOrder':'asc',
        'apiKey': API_KEY
    }
    flights = requests.get(link, params=session_params, headers={'Cache-Control': 'no-cache',
                                    'accept': 'application/json'})

    json_response = json.loads(flights.text)
    itineraries = json_response['Itineraries']

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
